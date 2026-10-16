
from soc_agent.tools import (
    search_related_alerts,
    search_security_knowledge,
)


if __name__ == "__main__":
    print("=== RELATED ALERTS ===")
    alerts = search_related_alerts("192.168.1.25")
    print(alerts)

    print("\n=== SECURITY KNOWLEDGE ===")
    guidance = search_security_knowledge("failed_login brute force")
    print(guidance)
