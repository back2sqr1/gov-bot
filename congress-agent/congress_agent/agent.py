"""Congress.gov multi-agent orchestrator built on Google ADK.

Flow:
  1. orchestrator        -- picks the relevant skills for the user's prompt and
                            documents the plan, then fans out one skill_researcher
                            call per chosen skill, then synthesizes a final answer.
  2. skill_researcher    -- (spawned per skill) asks fetch_planner for a set of
                            fetches, performs them, and structures the results.
  3. fetch_planner       -- reads the skill's endpoint reference and proposes the
                            most useful API fetches for the sub-question.
  4. visualization_agent -- (on demand) extracts entities/relationships from the
                            conversation and opens an interactive knowledge graph.

Sub-agents are wired as AgentTools so the orchestrator can fan out dynamically
(one researcher per selected skill) rather than with a fixed-width parallel step.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .config import MODEL
from .congress_api import congress_fetch
from .skills import get_skill, list_skills
from .visualization import generate_visualization, generate_knowledge_graph


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


# --- Layer 3 (optional): interactive multi-mode visualization -----------------
visualization_agent = LlmAgent(
    name="visualization_agent",
    model=MODEL,
    description=(
        "Extracts entities, relationships, events, and flows from a research "
        "summary and opens a rich interactive multi-mode visualization."
    ),
    instruction=(
        "You create dynamic visualizations that illustrate the COMPLEXITY of "
        "government research findings.\n\n"
        "Your input is a natural language summary (bills, members, committees, "
        "votes, topics, legislative history, funding flows, etc.).\n\n"
        "Steps:\n"
        "1. Choose viz_type:\n"
        "   - 'graph': best when there are many cross-connected entities\n"
        "   - 'timeline': best when there is a clear sequence of dated events\n"
        "   - 'sankey': best when data has flows (votes, funds, referrals)\n"
        "   - 'dashboard': best for rich data with multiple dimensions\n"
        "   - 'auto': let the system decide\n"
        "2. Extract nodes (entities):\n"
        "   - id: snake_case (e.g. 'hr3076', 'pelosi', 'commerce_cmte')\n"
        "   - label: 1-4 words\n"
        "   - type: bill | member | committee | topic | vote | other\n"
        "   - weight: 1-5 (importance — affects node size)\n"
        "3. Extract edges (relationships):\n"
        "   - source/target: node ids\n"
        "   - label: short verb phrase ('sponsored', 'chairs', 'voted for')\n"
        "   - weight: 1-3\n"
        "4. Extract events (for timeline):\n"
        "   - id, label, date (YYYY-MM-DD), type (bill|vote|action|hearing|other)\n"
        "5. Extract flows (for sankey):\n"
        "   - source, target (names), value (numeric), label\n"
        "6. Write a complexity_note: one sentence describing what makes this "
        "   discussion structurally complex (many actors, layered processes, etc.).\n"
        "7. Call generate_visualization with a JSON string containing all of the above.\n"
        "8. Reply with one sentence confirming what was visualized.\n\n"
        "Include as many real entities as you can extract. More detail = better graph."
    ),
    tools=[generate_visualization, generate_knowledge_graph],
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
        "   When you cross sources, carry identifiers across (e.g. use a member's\n"
        "   name from congress to find their fec candidate/committee, or vice\n"
        "   versa).\n"
        "4. After all researchers return, write an '**Analysis**' section that\n"
        "   synthesizes their structured findings into one coherent answer. Cite\n"
        "   the skills/endpoints the facts came from, include relevant ids and\n"
        "   source URLs, and explicitly call out any gaps, errors, or missing data.\n\n"
        "Only use skills returned by list_skills. Never invent endpoints or values.\n\n"
        "If the user directly supplies a document URL (e.g. a PDF link) and asks\n"
        "you to read or summarize it, you may skip the skill flow and call the\n"
        "document_analyst tool yourself with:\n"
        "    URL: <the document url>\n"
        "    QUESTION: <what the user wants from it>\n"
        "5. After all researchers return, write a '**Analysis**' section that\n"
        "   synthesizes their structured findings into one coherent answer. Cite the\n"
        "   skills/endpoints the facts came from, include relevant ids and Congress.gov\n"
        "   URLs, and explicitly call out any gaps, errors, or missing data.\n"
        "6. Visualization: if the user asks to 'show a graph', 'visualize',\n"
        "   or 'map the relationships', call the visualization_agent tool, passing the\n"
        "   full **Analysis** text as the input. Do NOT call it automatically on every\n"
        "   response — only when the user requests it or the response has rich\n"
        "   multi-entity relationships that would clearly benefit from a graph.\n\n"
        "Only use skills returned by list_skills. Never invent endpoints or values."
    ),
    tools=[list_skills, AgentTool(agent=skill_researcher), AgentTool(agent=document_analyst), AgentTool(agent=visualization_agent)],
)
