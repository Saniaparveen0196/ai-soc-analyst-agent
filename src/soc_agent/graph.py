
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from soc_agent.alert_analyzer import analyze_alert
from soc_agent.llm_analyzer import investigate_alert
from soc_agent.tools import search_related_alerts
from soc_agent.rag import search_security_knowledge_semantic


class SOCState(TypedDict):
    alert: dict
    analysis: dict
    related_alerts: list[dict]
    security_knowledge: list[dict]
    investigation_report: str


def analyze_node(state: SOCState) -> dict:
    return {
        "analysis": analyze_alert(state["alert"])
    }


def route_after_analysis(state: SOCState) -> str:
    if state["analysis"]["requires_investigation"]:
        return "investigate_path"

    return "skip_investigation"


def gather_evidence_node(state: SOCState) -> dict:
    alert = state["analysis"]

    related = [
        item
        for item in search_related_alerts(
            alert.get("source_ip", "")
        )
        if item.get("alert_id") != alert.get("alert_id")
    ]

    query = (
        alert.get("event_type", "")
        + " "
        + alert.get("description", "")
    )

    knowledge = search_security_knowledge_semantic(
        query,
        k=2,
    )

    return {
        "related_alerts": related,
        "security_knowledge": knowledge,
    }


def investigate_node(state: SOCState) -> dict:
    evidence = {
        **state["analysis"],
        "related_alerts": state["related_alerts"],
        "security_knowledge": state["security_knowledge"],
    }

    report = investigate_alert(evidence)

    return {
        "investigation_report": report
    }


def skip_investigation_node(state: SOCState) -> dict:
    return {
        "related_alerts": [],
        "security_knowledge": [],
        "investigation_report": (
            "No LLM investigation was performed because "
            "the rule-based analyzer did not flag this alert "
            "for investigation. This does not prove the alert "
            "is harmless; review the alert if other evidence "
            "suggests suspicious activity."
        ),
    }


def build_soc_graph():
    workflow = StateGraph(SOCState)

    workflow.add_node("analyze", analyze_node)
    workflow.add_node("gather_evidence", gather_evidence_node)
    workflow.add_node("investigate", investigate_node)
    workflow.add_node("skip_investigation", skip_investigation_node)

    workflow.add_edge(START, "analyze")

    workflow.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "investigate_path": "gather_evidence",
            "skip_investigation": "skip_investigation",
        },
    )

    workflow.add_edge("gather_evidence", "investigate")
    workflow.add_edge("investigate", END)
    workflow.add_edge("skip_investigation", END)

    return workflow.compile()
