# Gov Agent (Congress.gov + OpenFEC)

A chat agent over two U.S. government APIs — the
[Congress.gov API](https://api.congress.gov/) (legislation, members, votes,
committees, ...) and the [OpenFEC API](https://api.open.fec.gov/developers/)
(candidates, committees, campaign finance) — built with
[Google ADK](https://google.github.io/adk-docs/) (Python). You ask a question;
the orchestrator picks the relevant API "skills" from **either or both** sources,
fans out a researcher per skill to plan and run fetches, then synthesizes a
single cited answer.

## Architecture

```
You ──▶ gov_orchestrator (root)
          │  1. list_skills  → 40 API skills, grouped by source (congress, fec)
          │  2. select skills (mixing sources as needed), document the Plan
          │  3. for each chosen skill ▼ (one researcher per skill)
          │
          ├──▶ skill_researcher  (AgentTool, spawned per skill)
          │       │  a. fetch_planner ▼  → JSON list of fetches to run
          │       │
          │       ├──▶ fetch_planner (AgentTool)
          │       │       └─ get_skill("<source>/<group>")
          │       │            → reads skills/<source>/<group>/SKILL.md
          │       │
          │       b. api_fetch(source, path, params) for each planned fetch
          │          (source routes to Congress.gov or OpenFEC)
          │       c. if a fetch returns a PDF/text URL whose contents are
          │          needed ▼
          │       │
          │       ├──▶ document_analyst (AgentTool)  ◀── also callable by root
          │       │       └─ read_document(url) → pypdf text, OCR fallback
          │       │          for scanned PDFs (pdf2image + pytesseract)
          │       │
          │       d. structure the results
          │
          └─ 4. synthesize all researchers' findings → final Analysis
```

- **Skills** are organized by source, one folder per API:
  - `skills/congress/<group>/SKILL.md` — 20 Congress.gov groups (bill, member,
    treaty, ...), generated from `apis/` by `scripts/generate_skills.py`.
  - `skills/fec/<group>/SKILL.md` — 20 OpenFEC groups (candidate, committee,
    receipts, ...), generated from the live OpenFEC spec by
    `scripts/generate_fec_skills.py`.

  Each has frontmatter (`name`, `description`) plus a body documenting every
  endpoint. The registry keys api skills as `"<source>/<group>"` (e.g.
  `congress/bill`, `fec/candidate`) so groups that share a name across sources
  (both have a `committee`) don't collide, and the orchestrator can mix sources
  in one answer. A skill's source routes its fetches to the right API
  (`api_fetch`). Frontmatter `type: api` (the default for `skills/<source>/...`)
  marks a selectable endpoint group; `type: tool` marks a capability doc, hidden
  from selection but loadable via `get_skill` (e.g.
  `skills/document-extraction/`).
- **Document extraction** (`document_analyst` + `congress_agent/documents.py`):
  Congress.gov often exposes a resource's real content only as a file URL (bill
  text, committee/CRS reports, prints, hearings, the Congressional Record).
  Researchers (and the orchestrator, for a user-supplied link) can hand a URL to
  the `document_analyst`, which downloads the PDF/HTML/text and extracts what's
  needed. PDFs use `pypdf` for embedded text and fall back to OCR
  (`pdf2image` + `pytesseract`) for scanned pages. See
  `skills/document-extraction/SKILL.md`. OCR needs the `poppler` and `tesseract`
  system binaries (`brew install poppler tesseract`); without them digital PDFs
  still work and scanned ones report the limitation.
- All agents share one model: **Claude Opus 4.8** via ADK's LiteLLM integration
  (`CONGRESS_AGENT_MODEL`, default `anthropic/claude-opus-4-8`).

## Setup

```bash
cd congress-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp congress_agent/.env.example congress_agent/.env
# edit congress_agent/.env: set ANTHROPIC_API_KEY, CONGRESS_API_KEY, FEC_API_KEY
```

- Anthropic key: https://console.anthropic.com/settings/keys
- Congress.gov key (free): https://api.congress.gov/sign-up/
- OpenFEC key (free): https://api.open.fec.gov/developers/ (falls back to
  `DEMO_KEY`, 40 calls/hour, if `FEC_API_KEY` is unset)

## Run (chat)

Three equivalent chat interfaces:

```bash
adk web                    # browser UI; pick "congress_agent" (run from this dir)
adk run congress_agent     # terminal chat
python chat.py             # terminal chat (minimal custom runner)
```

Example prompts:
- "What did H.R. 3076 in the 117th Congress do, and what were its latest actions?"
- "How did the House vote on roll call 100 in the 118th Congress, 1st session?"
- "Show recent treaties and any committee activity on them."
- "Who are the top donors to Elizabeth Warren's 2024 campaign committee?" (FEC)
- "Summarize Senator X's recent bills AND their campaign fundraising totals."
  (mixes `congress` + `fec` skills in one answer)

## Model

Every agent runs **Claude Opus 4.8** through ADK's LiteLLM integration
(`congress_agent/config.py`). LiteLLM reads `ANTHROPIC_API_KEY` from the
environment. To switch model, set `CONGRESS_AGENT_MODEL` (e.g.
`anthropic/claude-sonnet-4-6`) in `.env`.

## Regenerating skills

Congress.gov — edit `apis/*.md` (or the descriptions in
`scripts/generate_skills.py`), then regenerate into `skills/congress/`:

```bash
python scripts/generate_skills.py
```

OpenFEC — regenerate `skills/fec/` from the live OpenFEC spec:

```bash
python scripts/generate_fec_skills.py
# offline, from a saved spec:
FEC_SWAGGER_FILE=/path/to/swagger.json python scripts/generate_fec_skills.py
```
