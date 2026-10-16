
from soc_agent.graph import build_soc_graph

sample_alert = {
    "alert_id": "SOC-001",
    "source_ip": "192.168.1.25",
    "destination_ip": "10.0.0.5",
    "event_type": "failed_login",
    "failed_attempts": 18,
    "description": "Multiple failed login attempts",
}

if __name__ == "__main__":
    app = build_soc_graph()

    result = app.invoke({
        "alert": sample_alert,
        "analysis": {},
        "related_alerts": [],
        "security_knowledge": [],
        "investigation_report": "",
    })

    print("\n=== SOC AGENT RESULT ===")
    print("Severity:", result["analysis"]["severity"])

    print("\n=== RELATED ALERTS ===")
    print(result["related_alerts"])

    print("\n=== RETRIEVED SECURITY KNOWLEDGE ===")
    print(result["security_knowledge"])

    print("\n=== INVESTIGATION REPORT ===")
    print(result["investigation_report"])
