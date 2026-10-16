
from soc_agent.llm_analyzer import investigate_alert

sample_alert = {
    "alert_id": "SOC-001",
    "source_ip": "192.168.1.25",
    "destination_ip": "10.0.0.5",
    "event_type": "failed_login",
    "failed_attempts": 18,
    "severity": "HIGH",
}

if __name__ == "__main__":
    print("Investigating alert...\n")
    report = investigate_alert(sample_alert)
    print(report)
