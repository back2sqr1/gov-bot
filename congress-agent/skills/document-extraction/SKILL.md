---
name: document-extraction
description: Download a government document (PDF/HTML/text) and extract its text, with OCR fallback for scanned PDFs.
type: tool
---

# Document Extraction (PDF / OCR)

A capability skill, not a Congress.gov API group. It is handled by the
`document_analyst` sub-agent (`congress_agent/agent.py`) using the tools in
`congress_agent/documents.py`. Because its `type` is `tool`, it is **not** listed
by `list_skills` and is never planned as an API fetch — but it is loadable via
`get_skill("document-extraction")`.

## When to use

Congress.gov frequently returns the substantive content of a resource only as a
**file URL**, not in the JSON. Reach for document extraction when the JSON gives
you a link but not the answer:

- **Bill / amendment text** — `/bill/{congress}/{type}/{number}/text` and
  `/amendments/.../text` return `textVersions` with `PDF` and `Formatted Text`
  (HTML) URLs.
- **Committee reports** — `/committee-report/.../text`.
- **Committee prints** — `/committee-print/.../text`.
- **Hearings, the Congressional Record, CRS reports** — published as PDFs.

Do **not** use it for metadata the JSON already contains (titles, dates, ids,
sponsors, action history). Only fetch the document when its own contents are
needed (specific statutory language, a report's findings, a hearing exchange).

## How the `document_analyst` works

Call it with:

```
URL: <direct link to a PDF, HTML, or text document>
QUESTION: <what to find in the document>
```

It uses two tools:

- `read_document(url, pages="", force_ocr=False)` — the main tool. Downloads the
  file and returns a metadata header (page count, pages read, extraction method)
  followed by the text.
  - `pages`: `''` = all (capped at 50); a range like `'1-10'`; or a list `'1,3,5'`
    (1-based). For long PDFs, read early pages first to locate the relevant
    section, then re-read just those pages.
  - `force_ocr=True`: OCR the pages even when embedded text exists (use when the
    embedded text is empty or garbled).
- `download_document(url)` — fetches the raw file to a local cache and returns
  `{"path", "content_type", "bytes"}`; `read_document` calls it internally.

### Extraction strategy

1. **Embedded text** via `pypdf` — fast, works for digital PDFs.
2. **OCR fallback** via `pdf2image` + `pytesseract` for pages with little/no
   embedded text (scanned/image PDFs).

OCR requires the `poppler` and `tesseract` system binaries plus the
`pdf2image`/`pytesseract` Python packages. These are optional: if they're
missing, `read_document` reports the limitation instead of failing, and digital
PDFs still work.

## Guardrails

- Answer strictly from the extracted text; quote short exact passages and cite
  page numbers when shown. Never fabricate document contents.
- Downloads are bounded (50 MB max, 50 pages when reading "all") to keep cost
  and latency in check.
