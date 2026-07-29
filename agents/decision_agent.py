from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from graph.state import AgentState


class Decision(BaseModel):
    reorder: bool
    recommended_qty: int
    reason: str


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
)

structured_llm = llm.with_structured_output(Decision)


from utils.logger import log_llm_request, log_llm_response


def decision_agent(state: AgentState):

    # Only reorder requests require a decision
    if state["intent"] != "reorder":
        return {
            **state,
            "decision": None,
        }

    inventory = state["inventory_data"]
    vendor = state["vendor_data"]
    weather = state["weather_data"]

    prompt = f"""
You are an inventory planning expert.

Analyze the following information and decide whether inventory should be reordered.

Inventory:
{inventory}

Vendor:
{vendor}

Weather:
{weather}

Consider:

- Current stock
- Reorder threshold
- Weather impact
- Vendor reliability

Return:

1. reorder (true/false)
2. recommended_qty
3. reason

Return JSON only.
"""

    log_llm_request("Decision Agent", prompt)
    decision = structured_llm.invoke(prompt)
    log_llm_response("Decision Agent", decision.model_dump())

    return {
        **state,
        "decision": decision.model_dump(),
    }