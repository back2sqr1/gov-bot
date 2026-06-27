"""Congress.gov multi-agent orchestrator built on Google ADK.

Flow:
  1. orchestrator        -- picks the relevant skills for the user's prompt and
                            documents the plan, then fans out one skill_researcher
                            call per chosen skill, then synthesizes a final answer.
  2. skill_researcher    -- (spawned per skill) asks fetch_planner for a set of
                            fetches, performs them, and structures the results.
  3. fetch_planner       -- reads the skill's endpoint reference and proposes the
                            most useful API fetches for the sub-question.

Sub-agents are wired as AgentTools so the orchestrator can fan out dynamically
(one researcher per selected skill) rather than with a fixed-width parallel step.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .config import MODEL
from .congress_api import congress_fetch
from .skills import get_skill, list_skills


# --- Layer 3: plan a set of fetches for one skill ------------------------------
fetch_planner = LlmAgent(
    name="fetch_planner",
    model=MODEL,
    description="Given a skill and a sub-question, proposes the best Congress.gov API fetches.",
    instruction=(
        "You plan API calls for ONE Congress.gov skill.\n"
        "Your input has the form:\n"
        "  SKILL: <skill_name>\n"
        "  QUESTION: <focused sub-question>\n\n"
        "Steps:\n"
        "1. Call get_skill(<skill_name>) to load that skill's endpoint reference.\n"
        "2. Choose up to 4 high-value fetches that would best answer the question.\n"
        "   Use only paths documented in the reference. Substitute concrete path\n"
        "   parameters from the question (congress numbers, bill type, ids, etc.).\n"
        "   Prefer list endpoints with filters (limit, fromDateTime, sort) when you\n"
        "   need discovery, and item/sub-resource endpoints when you have ids.\n\n"
        "Output ONLY a JSON array, each element:\n"
        '  {"path": "/bill/117/hr/3076/actions", "params": {"limit": "5"}, "reason": "..."}\n'
        "No prose, no markdown fences."
    ),
    tools=[get_skill],
)


# --- Layer 2: execute the plan and structure the data (one per skill) ----------
skill_researcher = LlmAgent(
    name="skill_researcher",
    model=MODEL,
    description=(
        "Researches one Congress.gov skill end to end: gets a fetch plan, "
        "performs the fetches, and returns structured findings."
    ),
    instruction=(
        "You research ONE Congress.gov skill to help answer the user's question.\n"
        "Your input has the form:\n"
        "  SKILL: <skill_name>\n"
        "  QUESTION: <focused sub-question>\n\n"
        "Steps:\n"
        "1. Call the fetch_planner tool, passing your input verbatim, to get a JSON\n"
        "   array of planned fetches.\n"
        "2. For each planned fetch, call congress_fetch(path, params_json) where\n"
        "   params_json is the fetch's params encoded as a JSON string (use '{}' if\n"
        "   none). If a result implies a useful follow-up fetch (e.g. an id you now\n"
        "   have), you may make one or two more fetches.\n"
        "3. Return a concise, structured markdown summary of the key findings:\n"
        "   include identifiers, titles, dates, vote/action outcomes, and source\n"
        "   URLs returned by the API. Note any fetch that errored or returned no\n"
        "   data. Do NOT fabricate values that were not in the responses.\n"
        "Start your reply with the line: '### Skill: <skill_name>'."
    ),
    tools=[AgentTool(agent=fetch_planner), congress_fetch],
)


# --- Layer 1: orchestrator (root) ----------------------------------------------
root_agent = LlmAgent(
    name="congress_orchestrator",
    model=MODEL,
    description="Answers questions about the U.S. Congress by routing to Congress.gov skills.",
    instruction=(
        "You are the orchestrator for a research assistant over the Congress.gov "
        "API. You answer questions about U.S. federal legislation, members, votes, "
        "committees, nominations, treaties, and the Congressional Record.\n\n"
        "Process for every user request:\n"
        "1. Call list_skills to see the available skills and their descriptions.\n"
        "2. Select the skills relevant to the question. Then, before fetching, write\n"
        "   a short '**Plan**' section to the user that lists each chosen skill and\n"
        "   one line on why you picked it. If no skill fits, say so and stop.\n"
        "3. For EACH chosen skill, call the skill_researcher tool with input:\n"
        "       SKILL: <skill_name>\n"
        "       QUESTION: <a focused sub-question for that skill>\n"
        "   Call the skills one at a time, waiting for each result before the next.\n"
        "4. After all researchers return, write a '**Analysis**' section that\n"
        "   synthesizes their structured findings into one coherent answer. Cite the\n"
        "   skills/endpoints the facts came from, include relevant ids and Congress.gov\n"
        "   URLs, and explicitly call out any gaps, errors, or missing data.\n\n"
        "Only use skills returned by list_skills. Never invent endpoints or values."
    ),
    tools=[list_skills, AgentTool(agent=skill_researcher)],
)
