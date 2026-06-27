"""Skill registry: loads skills/**/SKILL.md and exposes them as tools.

Skills are organized by *source* (the upstream API), one folder per source:

    skills/congress/<group>/SKILL.md   -> Congress.gov API groups (bill, member, ...)
    skills/fec/<group>/SKILL.md        -> OpenFEC API groups (candidate, receipts, ...)

Each api skill is keyed by a namespaced name "<source>/<group>" (e.g.
"congress/bill", "fec/committee") so groups that share a name across sources
(both have a "committee") don't collide. The orchestrator can therefore mix
skills from both sources in a single answer.

A SKILL.md placed directly under skills/ (e.g. skills/document-extraction/) is a
cross-cutting *capability* skill: it has frontmatter `type: tool`, no source, and
is hidden from list_skills (loadable via get_skill).
"""

from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# Maps a source key to the API base/auth used to fetch its endpoints. The
# orchestrator/researchers route fetches by a skill's source (see gov_api).
SOURCES = {
    "congress": "Congress.gov API",
    "fec": "OpenFEC API",
}


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a SKILL.md into (metadata, body). Tolerates files with no frontmatter."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            _, raw_meta, body = parts
            meta: dict[str, str] = {}
            for line in raw_meta.strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
            return meta, body.strip()
    return {}, text.strip()


def _load_skills() -> dict[str, dict]:
    registry: dict[str, dict] = {}
    if not SKILLS_DIR.exists():
        return registry
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        dirs = skill_md.relative_to(SKILLS_DIR).parts[:-1]
        meta, body = _parse_frontmatter(skill_md.read_text())

        if len(dirs) >= 2:
            # skills/<source>/<group>/SKILL.md -> a namespaced API skill.
            source, group = dirs[0], dirs[-1]
            name = f"{source}/{meta.get('name', group)}"
            skill_type = meta.get("type", "api")
        else:
            # skills/<group>/SKILL.md -> a sourceless capability skill.
            source = None
            name = meta.get("name", dirs[-1] if dirs else skill_md.parent.name)
            skill_type = meta.get("type", "tool")

        registry[name] = {
            "name": name,
            "source": source,
            "description": meta.get("description", ""),
            # "api" skills map to an endpoint group and are selectable by the
            # orchestrator. "tool"/other types are capability docs: loadable via
            # get_skill but never planned as fetches.
            "type": skill_type,
            "body": body,
            "path": str(skill_md),
        }
    return registry


SKILLS: dict[str, dict] = _load_skills()


# --- Tools (plain functions; ADK wraps them automatically) ---------------------

def list_skills() -> str:
    """List every available API skill, grouped by source, with its description.

    Use this first to decide which skills are relevant to the user's question.
    Skill names are namespaced as "<source>/<group>" (e.g. "congress/bill",
    "fec/candidate"); pass that full name to the skill_researcher. You may mix
    skills from different sources in one plan.

    Returns:
        A markdown list grouped by source ("congress" = Congress.gov, "fec" =
        OpenFEC), each line "- <source>/<group>: description".
    """
    api_skills = [s for s in SKILLS.values() if s["type"] == "api"]
    if not api_skills:
        return "No skills found."
    lines: list[str] = []
    for source, label in SOURCES.items():
        group = sorted(
            (s for s in api_skills if s["source"] == source), key=lambda s: s["name"]
        )
        if not group:
            continue
        lines.append(f"## {source} ({label})")
        lines.extend(f"- {s['name']}: {s['description']}" for s in group)
        lines.append("")
    # Any api skills from an unconfigured source (defensive).
    other = sorted(
        (s for s in api_skills if s["source"] not in SOURCES), key=lambda s: s["name"]
    )
    if other:
        lines.append("## other")
        lines.extend(f"- {s['name']}: {s['description']}" for s in other)
    return "\n".join(lines).strip()


def get_skill(name: str) -> str:
    """Return the full endpoint reference for one skill.

    Args:
        name: The namespaced skill name, e.g. 'congress/bill', 'fec/candidate',
            or 'fec/receipts'. Capability skills (e.g. 'document-extraction') are
            looked up by their bare name.

    Returns:
        Markdown documenting the base URL, parameters, and every endpoint for
        that skill, or an error message listing valid skill names.
    """
    skill = SKILLS.get(name)
    if not skill:
        valid = ", ".join(sorted(s for s, v in SKILLS.items() if v["type"] == "api"))
        return f"Unknown skill '{name}'. Available skills: {valid}"
    return skill["body"]
