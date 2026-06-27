"""Minimal terminal chat interface for the Congress.gov orchestrator.

Usage: python chat.py
(Alternatively use the ADK CLI: `adk run congress_agent` or `adk web`.)
"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv("congress_agent/.env")

from congress_agent.agent import root_agent  # noqa: E402  (after load_dotenv)

APP_NAME = "congress_agent"
USER_ID = "local-user"
SESSION_ID = "chat"


async def main() -> None:
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print("Congress.gov agent — ask about bills, members, votes, etc. ('exit' to quit)\n")
    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break

        message = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"\nAgent: {event.content.parts[0].text}\n")


if __name__ == "__main__":
    asyncio.run(main())
