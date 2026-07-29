from langchain_google_genai import ChatGoogleGenerativeAI

from graph.state import AgentState
from utils.logger import log_llm_request, log_llm_response



llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
)


def report_agent(state: AgentState):

    intent = state["intent"]

    # --------------------------------------------------
    # REORDER REPORT
    # --------------------------------------------------

    if intent == "reorder":

        prompt = f"""
Generate a professional inventory report.

Inventory
----------
{state["inventory_data"]}

Vendor
------
{state["vendor_data"]}

Weather
-------
{state["weather_data"]}

Decision
--------
{state["decision"]}

Ticket
------
{state.get("ticket")}

The report should contain:

1. Inventory Summary

2. Vendor Summary

3. Weather Impact

4. AI Decision

5. Recommendation

6. Ticket Status

Keep it concise and professional.
"""

    # --------------------------------------------------
    # LOW STOCK
    # --------------------------------------------------

    elif intent == "low_stock":

        prompt = f"""
Generate a professional report for the following low stock inventory.

Inventory

{state["inventory_data"]}

Summarize:

- Total low stock products
- Critical products
- Recommended action
"""

    # --------------------------------------------------
    # INVENTORY LOOKUP
    # --------------------------------------------------

    elif intent == "inventory_lookup":

        prompt = f"""
Generate a concise inventory summary.

Inventory

{state["inventory_data"]}
"""

    # --------------------------------------------------
    # CATEGORY LOOKUP
    # --------------------------------------------------

    elif intent == "category_lookup":

        prompt = f"""
Summarize this product category.

Inventory

{state["inventory_data"]}
"""

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    elif intent == "weather_lookup":

        prompt = f"""
Summarize the weather information.

Weather

{state["weather_data"]}

Mention possible inventory implications if any.
"""



    else:

        prompt = f"""
Summarize the following information.

{state}
"""

    log_llm_request("Report Agent", prompt)
    report = llm.invoke(prompt)
    report_text = report.content if isinstance(report.content, str) else "\n".join([c.get("text", "") for c in report.content if isinstance(c, dict) and "text" in c])
    log_llm_response("Report Agent", report_text[:300] + ("..." if len(report_text) > 300 else ""))


    return {
        **state,
        "report": report_text,
    }