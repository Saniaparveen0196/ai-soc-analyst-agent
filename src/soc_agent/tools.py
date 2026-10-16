
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def search_related_alerts(source_ip: str) -> list[dict]:
    """Find sample alerts that share a source IP."""

    alerts_file = DATA_DIR / "sample_alerts.json"

    with alerts_file.open("r", encoding="utf-8") as file:
        alerts = json.load(file)

    return [
        alert
        for alert in alerts
        if alert.get("source_ip") == source_ip
    ]


def search_security_knowledge(query: str) -> list[dict]:
    """Find security guidance using simple keyword matching."""

    knowledge_file = DATA_DIR / "security_knowledge.json"

    with knowledge_file.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    query_terms = set(query.lower().replace("_", " ").split())
    results = []

    for item in knowledge:
        searchable_text = " ".join(
            [item["topic"], *item["keywords"], item["guidance"]]
        ).lower().replace("_", " ")

        if any(term in searchable_text for term in query_terms):
            results.append(item)

    return results
