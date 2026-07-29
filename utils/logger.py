"""
utils/logger.py

Logger helper for printing LLM prompts, input payloads, and responses cleanly
to stdout/server logs for real-time inspection.
"""

from datetime import datetime


def log_llm_request(agent_name: str, prompt_text: str):
    """Print styled box showing the exact prompt payload sent to the LLM."""
    now = datetime.now().strftime("%H:%M:%S")
    border = "=" * 80
    print(f"\n{border}")
    print(f"📤 [LLM PROMPT SENT] Agent: {agent_name} | Time: {now}")
    print(f"{border}")
    print(prompt_text.strip())
    print(f"{border}\n")


def log_llm_response(agent_name: str, response_data):
    """Print styled box showing the response returned by the LLM."""
    now = datetime.now().strftime("%H:%M:%S")
    border = "-" * 80
    print(f"\n{border}")
    print(f"📥 [LLM RESPONSE RECEIVED] Agent: {agent_name} | Time: {now}")
    print(f"{border}")
    print(response_data)
    print(f"{border}\n")
