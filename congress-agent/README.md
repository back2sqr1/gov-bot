# Congress.gov Agent

A chat agent over the [Congress.gov API](https://api.congress.gov/), built with
[Google ADK](https://google.github.io/adk-docs/) (Python). You ask a question;
the orchestrator picks the relevant API "skills", fans out a researcher per
skill to plan and run fetches, then synthesizes a single cited answer.

## Architecture

```
You ──▶ congress_orchestrator (root)
          │  1. list_skills  → see all 20 API skills + descriptions
          │  2. select skills, document the Plan
          │  3. for each chosen skill ▼ (one researcher per skill)
          │
          ├──▶ skill_researcher  (AgentTool, spawned per skill)
          │       │  a. fetch_planner ▼  → JSON list of fetches to run
          │       │
          │       ├──▶ fetch_planner (AgentTool)
          │       │       └─ get_skill(name) → reads skills/<name>/SKILL.md
          │       │
          │       b. congress_fetch(path, params) for each planned fetch
          │       c. structure the results
          │
          └─ 4. synthesize all researchers' findings → final Analysis
```

- **Skills** live in `skills/<name>/SKILL.md` — one per Congress.gov API group
  (bill, member, treaty, ...), with frontmatter (`name`, `description`) used for
  selection and a body documenting every endpoint. They are generated from the
  raw references in `apis/` by `scripts/generate_skills.py`.
- All agents share one model: **Claude Opus 4.8** via ADK's LiteLLM integration
  (`CONGRESS_AGENT_MODEL`, default `anthropic/claude-opus-4-8`).

## Setup

```bash
cd congress-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp congress_agent/.env.example congress_agent/.env
# edit congress_agent/.env: set ANTHROPIC_API_KEY and CONGRESS_API_KEY
```

- Anthropic key: https://console.anthropic.com/settings/keys
- Congress.gov key (free): https://api.congress.gov/sign-up/

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

## Model

Every agent runs **Claude Opus 4.8** through ADK's LiteLLM integration
(`congress_agent/config.py`). LiteLLM reads `ANTHROPIC_API_KEY` from the
environment. To switch model, set `CONGRESS_AGENT_MODEL` (e.g.
`anthropic/claude-sonnet-4-6`) in `.env`.

## Regenerating skills

Edit `apis/*.md` (or the descriptions in `scripts/generate_skills.py`), then:

```bash
python scripts/generate_skills.py
```
