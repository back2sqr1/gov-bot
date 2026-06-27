"""Skill registry: loads skills/<name>/SKILL.md and exposes them as tools.

A "skill" is one Congress.gov API group (bill, member, treaty, ...). Each is a
markdown file with YAML-ish frontmatter (name + description) and a body that
documents every endpoint in that group.
"""

from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


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
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        meta, body = _parse_frontmatter(skill_md.read_text())
        name = meta.get("name", skill_md.parent.name)
        registry[name] = {
            "name": name,
            "description": meta.get("description", ""),
            "body": body,
            "path": str(skill_md),
        }
    return registry


SKILLS: dict[str, dict] = _load_skills()


# --- Tools (plain functions; ADK wraps them automatically) ---------------------

def list_skills() -> str:
    """List every available Congress.gov skill and its description.

    Use this first to decide which skills are relevant to the user's question.

    Returns:
        A newline-delimited list of "skill_name: description" entries.
    """
    if not SKILLS:
        return "No skills found."
    return "\n".join(f"- {s['name']}: {s['description']}" for s in SKILLS.values())


def get_skill(name: str) -> str:
    """Return the full endpoint reference for one skill.

    Args:
        name: The skill name, e.g. 'bill', 'member', 'treaty'.

    Returns:
        Markdown documenting the base URL, parameters, and every endpoint for
        that skill, or an error message listing valid skill names.
    """
    skill = SKILLS.get(name)
    if not skill:
        return f"Unknown skill '{name}'. Available skills: {', '.join(SKILLS)}"
    return skill["body"]
