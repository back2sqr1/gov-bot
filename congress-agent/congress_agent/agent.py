"""Government-data multi-agent orchestrator built on Google ADK.

Answers questions over two APIs — Congress.gov (legislation, members, votes,
committees, ...) and OpenFEC (candidates, committees, receipts, disbursements,
campaign finance, ...) — and can mix both in a single answer.

Flow:
  1. orchestrator        -- picks the relevant skills (from either source) for
                            the user's prompt and documents the plan, then fans
                            out one skill_researcher call per chosen skill, then
                            synthesizes a final answer.
  2. skill_researcher    -- (spawned per skill) asks fetch_planner for a set of
                            fetches, performs them, and structures the results.
  3. fetch_planner       -- reads the skill's endpoint reference and proposes the
                            most useful API fetches for the sub-question.

Skills are namespaced "<source>/<group>" (e.g. "congress/bill", "fec/candidate");
the source routes each fetch to the right API via api_fetch. Sub-agents are wired
as AgentTools so the orchestrator can fan out dynamically (one researcher per
selected skill) rather than with a fixed-width parallel step.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .config import MODEL
from .congress_api import api_fetch
from .documents import download_document, read_document
from .skills import get_skill, list_skills


# --- Layer 3: plan a set of fetches for one skill ------------------------------
fetch_planner = LlmAgent(
    name="fetch_planner",
    model=MODEL,
    description="Given a skill and a sub-question, proposes the best API fetches for it.",
    instruction=(
        "You plan API calls for ONE skill of a government data API.\n"
        "Your input has the form:\n"
        "  SKILL: <source>/<group>   (e.g. 'congress/bill' or 'fec/candidate')\n"
        "  QUESTION: <focused sub-question>\n\n"
        "Steps:\n"
        "1. Call get_skill(<skill_name>) with the full namespaced name to load that\n"
        "   skill's endpoint reference (it documents the API's base URL and params).\n"
        "2. Choose up to 4 high-value fetches that would best answer the question.\n"
        "   Use only paths documented in the reference, written relative to that\n"
        "   API's base URL. Substitute concrete path parameters from the question\n"
        "   (congress numbers, bill type, candidate/committee ids, cycle, etc.).\n"
        "   Prefer list endpoints with filters when you need discovery, and\n"
        "   item/sub-resource endpoints when you already have ids.\n\n"
        "Output ONLY a JSON array, each element:\n"
        '  {"path": "/candidate/P00009423/totals/", "params": {"cycle": "2024"}, "reason": "..."}\n'
        "No prose, no markdown fences."
    ),
    tools=[get_skill],
)


# --- Cross-cutting: read a document (PDF/HTML/text) and extract its content ----
# Congress.gov often exposes the real content only as a file URL (bill text,
# committee/CRS reports, prints, hearings, the Congressional Record). This
# sub-agent downloads one such document and extracts what's needed, OCR-ing
# scanned PDFs. It is available both to each skill_researcher (to dig into a URL
# a fetch returned) and to the orchestrator (for a PDF URL the user supplies).
document_analyst = LlmAgent(
    name="document_analyst",
    model=MODEL,
    description=(
        "Downloads one government document (a bill-text/report/hearing PDF, HTML, "
        "or text URL) and extracts the information needed to answer a focused "
        "question, using OCR when the PDF is scanned."
    ),
    instruction=(
        "You extract information from a SINGLE government document.\n"
        "Your input has the form:\n"
        "  URL: <direct link to a PDF, HTML, or text document>\n"
        "  QUESTION: <what to find in the document>\n\n"
        "Steps:\n"
        "1. Call read_document(url, pages='', force_ocr=False) to pull the text.\n"
        "   - 'pages' may be '' (all, capped), a range like '1-10', or a list\n"
        "     '1,3,5' (1-based). The result starts with a header noting the page\n"
        "     count, how many pages were read, and the extraction method.\n"
        "   - For a long PDF, read the first few pages (e.g. '1-5') to find the\n"
        "     relevant section, then re-read just those pages.\n"
        "   - If the header reports little/no embedded text (a scanned PDF) and\n"
        "     you still need the content, retry with force_ocr=True. If it warns\n"
        "     that OCR is unavailable, report that limitation.\n"
        "2. Answer the QUESTION strictly from the extracted text. Quote short,\n"
        "   exact passages for key facts and cite their page numbers when shown.\n"
        "3. If the document could not be read (download error, empty, OCR missing),\n"
        "   say so plainly. Never fabricate document contents.\n"
        "Start your reply with the line: '#### Document: <url>'."
    ),
    tools=[read_document, download_document],
)


# --- Layer 2: execute the plan and structure the data (one per skill) ----------
skill_researcher = LlmAgent(
    name="skill_researcher",
    model=MODEL,
    description=(
        "Researches one skill (Congress.gov or OpenFEC) end to end: gets a fetch "
        "plan, performs the fetches, and returns structured findings."
    ),
    instruction=(
        "You research ONE skill to help answer the user's question.\n"
        "Your input has the form:\n"
        "  SKILL: <source>/<group>   (e.g. 'congress/bill' or 'fec/receipts')\n"
        "  QUESTION: <focused sub-question>\n\n"
        "The SOURCE is the part of the skill name before the '/': 'congress' for\n"
        "Congress.gov, 'fec' for OpenFEC. You pass it to api_fetch.\n\n"
        "Steps:\n"
        "1. Call the fetch_planner tool, passing your input verbatim, to get a JSON\n"
        "   array of planned fetches.\n"
        "2. For each planned fetch, call api_fetch(source, path, params_json) where\n"
        "   source is the skill's source, and params_json is the fetch's params as a\n"
        "   JSON string (use '{}' if none). If a result implies a useful follow-up\n"
        "   fetch (e.g. an id you now have), you may make one or two more fetches\n"
        "   against the same source.\n"
        "2b. If a result returns a DOCUMENT URL (e.g. a PDF or 'Formatted Text' link\n"
        "    for bill text, a committee/CRS report, a hearing, an FEC filing) AND the\n"
        "    question needs detail the JSON does not contain, call the\n"
        "    document_analyst tool with input:\n"
        "        URL: <the document url>\n"
        "        QUESTION: <what you need from that document>\n"
        "    Use document_analyst only when the document's own contents are needed —\n"
        "    not for metadata the JSON already provides.\n"
        "3. Return a concise, structured markdown summary of the key findings:\n"
        "   include identifiers, titles, dates, amounts, vote/action outcomes, and\n"
        "   source URLs returned by the API. Note any fetch that errored or returned\n"
        "   no data. Do NOT fabricate values that were not in the responses.\n"
        "Start your reply with the line: '### Skill: <source>/<group>'."
    ),
    tools=[
        AgentTool(agent=fetch_planner),
        api_fetch,
        AgentTool(agent=document_analyst),
    ],
)


# --- Layer 1: orchestrator (root) ----------------------------------------------
root_agent = LlmAgent(
    name="gov_orchestrator",
    model=MODEL,
    description=(
        "Answers questions about U.S. Congress and federal campaign finance by "
        "routing to Congress.gov and OpenFEC skills, mixing both as needed."
    ),
    instruction=(
        "You are the orchestrator for a research assistant over two government "
        "APIs:\n"
        "  - congress (Congress.gov): federal legislation, members, votes,\n"
        "    committees, nominations, treaties, the Congressional Record.\n"
        "  - fec (OpenFEC): candidates, committees/PACs, and campaign finance —\n"
        "    receipts, disbursements, independent expenditures, filings, etc.\n"
        "Skills are namespaced '<source>/<group>'. Many questions span both (a\n"
        "lawmaker's bills AND their campaign fundraising) — mix skills from both\n"
        "sources whenever that produces a fuller answer.\n\n"
        "Process for every user request:\n"
        "1. Call list_skills to see the available skills (grouped by source) and\n"
        "   their descriptions.\n"
        "2. Select the skills relevant to the question — from either or both\n"
        "   sources. Then, before fetching, write a short '**Plan**' section that\n"
        "   lists each chosen skill (by its full '<source>/<group>' name) and one\n"
        "   line on why you picked it. If no skill fits, say so and stop.\n"
        "3. For EACH chosen skill, call the skill_researcher tool with input:\n"
        "       SKILL: <source>/<group>\n"
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
    ),
    tools=[
        list_skills,
        AgentTool(agent=skill_researcher),
        AgentTool(agent=document_analyst),
    ],
)
