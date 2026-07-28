from langgraph.graph import StateGraph, END
from graph.state import AgentState

from agents.data_agent import data_agent
from agents.decision_agent import decision_agent
from agents.ticket_agent import ticket_agent
from agents.report_agent import report_agent


def should_make_decision(state: AgentState):
    if state["intent"] == "reorder":
        return "decision"

    return "report"


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("data", data_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("ticket", ticket_agent)
    graph.add_node("report", report_agent)

    graph.set_entry_point("data")

    graph.add_conditional_edges(
        "data",
        should_make_decision,
    )

    graph.add_edge("decision", "ticket")
    graph.add_edge("ticket", "report")
    graph.add_edge("report", END)

    return graph.compile()