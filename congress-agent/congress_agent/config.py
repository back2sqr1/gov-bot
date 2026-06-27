"""Runtime configuration, read from environment / .env."""

import os

from google.adk.models.lite_llm import LiteLlm

# Model used by every agent in the system. We run Claude (Opus 4.8) via ADK's
# LiteLLM integration, which reads ANTHROPIC_API_KEY from the environment.
# Override the model id with CONGRESS_AGENT_MODEL if needed.
MODEL_NAME = os.environ.get("CONGRESS_AGENT_MODEL", "anthropic/claude-opus-4-8")
MODEL = LiteLlm(model=MODEL_NAME)

# Congress.gov API key — get one free at https://api.congress.gov/sign-up/
CONGRESS_API_KEY = os.environ.get("CONGRESS_API_KEY", "")

# Base URL for the Congress.gov REST API.
CONGRESS_API_BASE = "https://api.congress.gov/v3"
