"""Document tools: download government PDFs and extract their text.

Many Congress.gov resources expose their real content only as a file URL, not
as JSON: bill text, committee/CRS reports, committee prints, hearings, and the
Congressional Record are all published as PDFs (with an HTML "Formatted Text"
alternative). The Congress.gov API hands back these URLs in its JSON (e.g. a
bill text endpoint's ``textVersions[].formats[].url``); they are public links on
``www.congress.gov`` / ``govinfo.gov`` and need no API key. These tools let an
agent fetch one and pull out the text so it can answer questions the JSON
metadata can't. (A direct ``api.congress.gov`` link, which does need the key, is
authed automatically — but those are JSON endpoints, normally hit via
``api_fetch``, not documents.)

Extraction strategy (see ``read_document``):
  1. Embedded-text extraction with ``pypdf`` — fast, works for digital PDFs.
  2. If the embedded text is sparse (a scanned / image-only PDF) or the caller
     forces it, fall back to OCR via ``pdf2image`` + ``pytesseract``.

OCR has system dependencies (``poppler`` and the ``tesseract`` binary). They are
optional: if they're missing we return a clear message instead of crashing, so
the rest of the agent keeps working on digital PDFs.
"""

import hashlib
import json
import re
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import requests

from .config import CONGRESS_API_KEY

# A descriptive UA — some government file servers reject the default
# python-requests agent.
USER_AGENT = "congress-agent/1.0 (document fetcher)"

# Bounds to keep cost and latency sane regardless of what the model asks for.
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024  # 50 MB
MAX_PAGES = 50  # cap when the caller asks for "all" pages
# At/under this many characters a page is treated as effectively empty (a
# scanned/image page) and is a candidate for OCR. Kept low: genuine digital
# pages yield hundreds of chars, scanned pages yield ~0 from pypdf, so a low
# bar avoids OCR-ing (and mislabelling) short-but-valid pages like title pages.
MIN_CHARS_PER_PAGE = 10

CACHE_DIR = Path(tempfile.gettempdir()) / "congress_agent_docs"


def _cache_path(url: str, suffix: str = ".bin") -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{digest}{suffix}"


def _suffix_for(url: str, content_type: str) -> str:
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        return ".pdf"
    if "html" in content_type or url.lower().endswith((".htm", ".html")):
        return ".html"
    return ".txt"


def _parse_pages(pages: str, total: int) -> list[int]:
    """Turn a ``pages`` spec into 0-based page indices, bounded by ``total``.

    Accepts '' (all, capped at MAX_PAGES), a range like '1-10', a list '1,3,5',
    or a single page '4'. Page numbers in the spec are 1-based.
    """
    pages = (pages or "").strip()
    if not pages:
        return list(range(min(total, MAX_PAGES)))

    wanted: set[int] = set()
    for part in pages.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, _, hi = part.partition("-")
            try:
                lo_i, hi_i = int(lo), int(hi)
            except ValueError:
                continue
            for p in range(lo_i, hi_i + 1):
                if 1 <= p <= total:
                    wanted.add(p - 1)
        else:
            try:
                p = int(part)
            except ValueError:
                continue
            if 1 <= p <= total:
                wanted.add(p - 1)
    return sorted(wanted)


def _strip_html(html: str) -> str:
    """Crudely turn an HTML document into readable plain text (no bs4 dep)."""
    html = re.sub(r"(?is)<(script|style).*?</\1>", "", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|li|tr|h[1-6])>", "\n", html)
    text = re.sub(r"(?s)<[^>]+>", "", html)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def _auth_params(url: str) -> dict:
    """Query params needed to fetch ``url``.

    The Congress.gov API returns its actual documents as public links on
    ``www.congress.gov`` / ``govinfo.gov`` (no key needed). Only direct
    ``api.congress.gov`` links require the key — append it for those so a URL
    pasted straight from an API ``url`` field still works. The key is never sent
    to any other host.
    """
    host = (urlparse(url).hostname or "").lower()
    if host == "api.congress.gov" and CONGRESS_API_KEY:
        return {"api_key": CONGRESS_API_KEY}
    return {}


def download_document(url: str) -> str:
    """Download a document (PDF/HTML/text) to a local cache and report metadata.

    Use this when an API result gives you a file URL and you want the raw file
    before reading it. ``read_document`` calls this for you, so you usually only
    need this to confirm a URL is reachable or to inspect its type/size.

    The document URLs Congress.gov returns are public ``www.congress.gov`` /
    ``govinfo.gov`` links; a direct ``api.congress.gov`` link is auto-authed with
    the Congress API key.

    Args:
        url: Direct URL to a document, e.g. a PDF link from a bill/text endpoint.

    Returns:
        A JSON string: {"path", "content_type", "bytes", "url"} on success, or
        {"error", "url"} on failure.
    """
    try:
        resp = requests.get(
            url,
            params=_auth_params(url),
            headers={"User-Agent": USER_AGENT},
            timeout=60,
            stream=True,
        )
    except requests.RequestException as exc:
        return json.dumps({"error": f"request failed: {exc}", "url": url})

    if resp.status_code != 200:
        return json.dumps({"error": f"HTTP {resp.status_code}", "url": url})

    content_type = resp.headers.get("Content-Type", "").lower()
    path = _cache_path(url, _suffix_for(url, content_type))

    size = 0
    try:
        with open(path, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=65536):
                size += len(chunk)
                if size > MAX_DOWNLOAD_BYTES:
                    fh.close()
                    path.unlink(missing_ok=True)
                    return json.dumps(
                        {"error": f"document exceeds {MAX_DOWNLOAD_BYTES} byte limit", "url": url}
                    )
                fh.write(chunk)
    except OSError as exc:
        return json.dumps({"error": f"could not save document: {exc}", "url": url})

    return json.dumps(
        {"path": str(path), "content_type": content_type, "bytes": size, "url": url}
    )


def _extract_pdf_text(path: Path, pages: str) -> tuple[dict[int, str], int]:
    """Embedded-text extraction. Returns ({page_index: text}, total_pages)."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    total = len(reader.pages)
    out: dict[int, str] = {}
    for idx in _parse_pages(pages, total):
        try:
            out[idx] = (reader.pages[idx].extract_text() or "").strip()
        except Exception:  # noqa: BLE001 - a bad page shouldn't kill the doc
            out[idx] = ""
    return out, total


def _ocr_pdf(path: Path, page_indices: list[int]) -> dict[int, str]:
    """OCR the given 0-based pages. Raises ImportError if OCR deps are missing."""
    import pytesseract
    from pdf2image import convert_from_path

    out: dict[int, str] = {}
    for idx in page_indices:
        images = convert_from_path(str(path), first_page=idx + 1, last_page=idx + 1, dpi=200)
        out[idx] = pytesseract.image_to_string(images[0]).strip() if images else ""
    return out


def read_document(url: str, pages: str = "", force_ocr: bool = False) -> str:
    """Download a document and extract its text, using OCR for scanned PDFs.

    This is the main tool: give it a file URL (typically a PDF link returned by a
    Congress.gov text/report endpoint) and it returns the document's text plus a
    short header noting how many pages were read and whether OCR was used.

    Args:
        url: Direct URL to a PDF, HTML, or plain-text document.
        pages: Which pages to read (1-based). '' = all (capped at 50); a range
            like '1-10'; or a list like '1,3,5'. Ignored for HTML/text files.
            For long PDFs, read a few early pages first to locate the relevant
            section, then re-read just those pages.
        force_ocr: Set True to OCR the pages even if embedded text exists (use
            when the embedded text looks garbled or empty).

    Returns:
        Markdown: a metadata header followed by the extracted text, or a clear
        error line if the document could not be read.
    """
    meta = json.loads(download_document(url))
    if "error" in meta:
        return f"**Could not read document** ({url}): {meta['error']}"

    path = Path(meta["path"])
    content_type = meta["content_type"]
    suffix = path.suffix.lower()

    # Non-PDF documents: decode directly.
    if suffix != ".pdf":
        try:
            raw = path.read_text(errors="replace")
        except OSError as exc:
            return f"**Could not read document** ({url}): {exc}"
        text = _strip_html(raw) if suffix == ".html" else raw.strip()
        if not text:
            return f"**Document was empty** ({url}, content-type: {content_type})."
        return f"#### Document ({content_type}, ~{len(text)} chars)\nSource: {url}\n\n{text}"

    # PDF: embedded text first, then OCR fallback where needed.
    try:
        page_text, total = _extract_pdf_text(path, "" if force_ocr else pages)
    except ImportError:
        return (
            "**PDF support is not installed.** Add `pypdf` to the environment "
            "(`pip install pypdf`) to read PDF documents."
        )
    except Exception as exc:  # noqa: BLE001
        return f"**Could not parse PDF** ({url}): {exc}"

    selected = _parse_pages(pages, total)
    if force_ocr:
        ocr_targets = selected
    else:
        ocr_targets = [
            idx for idx in selected if len(page_text.get(idx, "")) < MIN_CHARS_PER_PAGE
        ]

    ocr_used = False
    ocr_note = ""
    if ocr_targets:
        try:
            ocr_text = _ocr_pdf(path, ocr_targets)
            for idx, txt in ocr_text.items():
                if txt:
                    page_text[idx] = txt
                    ocr_used = True
        except ImportError:
            ocr_note = (
                "\n\n_Note: {n} requested page(s) had little or no embedded text "
                "(likely scanned) but OCR is unavailable. Install `pdf2image` + "
                "`pytesseract` and the `poppler` and `tesseract` system binaries to "
                "read scanned PDFs._"
            ).format(n=len(ocr_targets))
        except Exception as exc:  # noqa: BLE001
            ocr_note = f"\n\n_Note: OCR failed for {len(ocr_targets)} page(s): {exc}_"

    body_parts = []
    for idx in selected:
        txt = page_text.get(idx, "")
        if txt:
            body_parts.append(f"--- page {idx + 1} ---\n{txt}")
    body = "\n\n".join(body_parts)

    char_count = sum(len(t) for t in page_text.values())
    method = "OCR" if ocr_used else "embedded text"
    if ocr_used and any(
        len(page_text.get(i, "")) >= MIN_CHARS_PER_PAGE and i not in ocr_targets
        for i in selected
    ):
        method = "embedded text + OCR"

    header = (
        f"#### Document ({total} pages total; read {len(selected)}; "
        f"~{char_count} chars; method: {method})\nSource: {url}"
    )
    if not body:
        return (
            f"{header}\n\n**No extractable text** on the requested pages "
            f"(the PDF may be scanned/empty).{ocr_note}"
        )
    return f"{header}\n\n{body}{ocr_note}"
