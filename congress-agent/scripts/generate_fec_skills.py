"""Generate fec_skills/<group>/SKILL.md from the OpenFEC OpenAPI (swagger) spec.

The OpenFEC API (https://api.open.fec.gov/developers/) groups its endpoints with
swagger "tags" — candidate, committee, receipts, disbursements, etc. This script
fetches the spec, buckets every operation by its tag, and writes one SKILL.md per
group in the same shape as the Congress.gov skills: YAML frontmatter (name +
description) for orchestrator selection, then a body documenting the base URL,
auth, common params, and each endpoint with its path/query parameters.

Run from anywhere:  python scripts/generate_fec_skills.py
Offline:            FEC_SWAGGER_FILE=/tmp/fec_swagger.json python scripts/generate_fec_skills.py
"""

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "skills" / "fec"

SWAGGER_URL = "https://api.open.fec.gov/swagger/"
BASE_URL = "https://api.open.fec.gov/v1"

# Pagination / sorting params that appear on nearly every list endpoint. We
# document them once in each skill's header and omit them from per-endpoint
# parameter lists to keep the references readable.
COMMON_PARAMS = {
    "api_key",
    "page",
    "per_page",
    "sort",
    "sort_hide_null",
    "sort_null_only",
    "sort_nulls_last",
}


def load_spec() -> dict:
    cached = os.environ.get("FEC_SWAGGER_FILE")
    if cached and Path(cached).exists():
        return json.loads(Path(cached).read_text())
    with urllib.request.urlopen(SWAGGER_URL, timeout=60) as resp:
        return json.loads(resp.read().decode())


def clean(text: str | None, limit: int | None = None) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def one_line_description(tag_desc: str) -> str:
    """Frontmatter description: the tag's first sentence, capped."""
    desc = clean(tag_desc)
    # First sentence (avoid splitting on common abbreviations is overkill here).
    match = re.match(r"(.+?\.)(\s|$)", desc)
    sentence = match.group(1) if match else desc
    return clean(sentence, 200)


def param_type(p: dict) -> str:
    t = p.get("type")
    if t == "array":
        item_t = (p.get("items") or {}).get("type", "string")
        return f"array<{item_t}>"
    return t or "string"


def param_enum(p: dict) -> list:
    raw = p.get("enum") or (p.get("items") or {}).get("enum") or []
    # FEC includes an empty-string option in many enums; drop it for clarity.
    return [e for e in raw if e != "" and e is not None]


def format_param(p: dict) -> str:
    name = p["name"]
    bits = [param_type(p)]
    if p.get("required"):
        bits.append("required")
    enum = param_enum(p)
    if enum and len(enum) <= 12:
        bits.append("one of: " + ", ".join(str(e) for e in enum))
    head = f"`{name}` ({', '.join(bits)})"
    desc = clean(p.get("description"), 140)
    return f"{head}: {desc}" if desc else head


def render_endpoint(path: str, method: str, op: dict) -> str:
    # Strip the /v1 base prefix so paths are relative to BASE_URL.
    rel = path[len("/v1"):] if path.startswith("/v1") else path
    lines = [f"### {method.upper()} {rel}"]
    desc = clean(op.get("summary") or op.get("description"), 400)
    if desc:
        lines.append(desc)

    params = op.get("parameters", [])
    path_params = [p for p in params if p.get("in") == "path"]
    query_params = [
        p for p in params if p.get("in") == "query" and p["name"] not in COMMON_PARAMS
    ]

    if path_params:
        lines.append("")
        lines.append("**Path parameters:**")
        for p in sorted(path_params, key=lambda x: x["name"]):
            lines.append(f"- {format_param(p)}")
    if query_params:
        lines.append("")
        lines.append("**Query parameters:**")
        for p in sorted(query_params, key=lambda x: (not x.get("required"), x["name"])):
            lines.append(f"- {format_param(p)}")
    return "\n".join(lines)


def render_skill(tag: str, tag_desc: str, endpoints: list[tuple[str, str, dict]]) -> str:
    title = tag.title().replace("Of", "of") + " API"
    description = one_line_description(tag_desc)

    header = [
        f"---\nname: {tag.replace(' ', '-')}\ndescription: {description}\n---",
        "",
        f"# {title}",
        "",
        clean(tag_desc) or f"OpenFEC `{tag}` endpoints.",
        "",
        f"- **Base URL:** `{BASE_URL}`",
        "- **Auth:** every request requires an API key, sent either as the "
        "`?api_key=YOUR_KEY` query parameter or the `X-Api-Key` header. A free key: "
        "https://api.open.fec.gov/developers/ (use `DEMO_KEY` for light testing).",
        "- **Common query params (most list endpoints):** `page`, `per_page` (max "
        "100), `sort`, `sort_hide_null`, `sort_null_only`, `sort_nulls_last`. Responses "
        "are JSON with `results` plus a `pagination` block.",
        "",
        "## Endpoints",
    ]

    # Stable ordering: by path, then method.
    body = [
        render_endpoint(path, method, op)
        for path, method, op in sorted(endpoints, key=lambda e: (e[0], e[1]))
    ]
    return "\n".join(header) + "\n\n" + "\n\n".join(body) + "\n"


def main() -> None:
    spec = load_spec()
    tag_descriptions = {t["name"]: t.get("description", "") for t in spec.get("tags", [])}

    # Bucket every GET/POST operation by tag.
    by_tag: dict[str, list[tuple[str, str, dict]]] = {}
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            if not isinstance(op, dict) or "tags" not in op:
                continue
            for tag in op["tags"]:
                by_tag.setdefault(tag, []).append((path, method, op))

    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for tag in sorted(by_tag):
        slug = tag.replace(" ", "-")
        skill_dir = OUT / slug
        skill_dir.mkdir(exist_ok=True)
        content = render_skill(tag, tag_descriptions.get(tag, ""), by_tag[tag])
        (skill_dir / "SKILL.md").write_text(content)
        written += 1
        print(f"wrote {skill_dir / 'SKILL.md'}  ({len(by_tag[tag])} endpoints)")
    print(f"\n{written} FEC skills generated in {OUT}")


if __name__ == "__main__":
    main()
