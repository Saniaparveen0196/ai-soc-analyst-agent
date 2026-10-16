
from soc_agent import graph as soc_graph


# Replace external services with test functions.
# This test will not call Groq or download the embedding model.
soc_graph.search_security_knowledge_semantic = (
    lambda query, k=2: [
        {
            "topic": "Test security guidance",
            "content": "Review authentication logs.",
        }
    ]
)

soc_graph.investigate_alert = (
    lambda evidence: "Mock investigation report"
)


def run_graph(alert):
    app = soc_graph.build_soc_graph()

    return app.invoke({
        "alert": alert,
        "analysis": {},
        "related_alerts": [],
        "security_knowledge": [],
        "investigation_report": "",
    })


if __name__ == "__main__":
    # Test 1: HIGH severity should trigger investigation.
    high_alert = {
        "alert_id": "TEST-HIGH",
        "source_ip": "192.168.1.25",
        "destination_ip": "10.0.0.5",
        "event_type": "failed_login",
        "failed_attempts": 18,
        "description": "Multiple failed login attempts",
    }

    high_result = run_graph(high_alert)

    assert high_result["analysis"]["severity"] == "HIGH"
    assert (
        high_result["investigation_report"]
        == "Mock investigation report"
    )

    print("PASS: HIGH alert follows investigation path.")

    # Test 2: LOW severity should skip investigation.
    low_alert = {
        "alert_id": "TEST-LOW",
        "source_ip": "192.168.1.12",
        "destination_ip": "10.0.0.20",
        "event_type": "normal_traffic",
        "failed_attempts": 0,
        "description": "Routine internal network communication",
    }

    low_result = run_graph(low_alert)

    assert low_result["analysis"]["severity"] == "LOW"
    assert "No LLM investigation was performed" in (
        low_result["investigation_report"]
    )
    assert low_result["security_knowledge"] == []

    print("PASS: LOW alert skips investigation.")
    print("\nAll routing tests passed!")
