
import json
from pathlib import Path

from soc_agent.alert_analyzer import analyze_alert


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALERTS_FILE = PROJECT_ROOT / "data" / "sample_alerts.json"


def main():
    with ALERTS_FILE.open("r", encoding="utf-8") as file:
        alerts = json.load(file)

    print("\n=== AI SOC Analyst Agent ===")
    print(f"Loaded {len(alerts)} sample alerts.\n")

    for alert in alerts:
        result = analyze_alert(alert)

        print(f"Alert ID: {result['alert_id']}")
        print(f"Event: {result['event_type']}")
        print(f"Severity: {result['severity']}")
        print(f"Reason: {result['analysis_reason']}")
        print(
            "Needs investigation:",
            result["requires_investigation"],
        )
        print("-" * 45)


if __name__ == "__main__":
    main()
