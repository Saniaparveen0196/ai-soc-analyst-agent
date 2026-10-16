
def analyze_alert(alert: dict) -> dict:
    """
    Assign a preliminary severity to a security alert
    using simple, explainable rules.
    """

    event_type = alert.get("event_type", "").lower()
    failed_attempts = int(alert.get("failed_attempts", 0))

    if event_type == "port_scan":
        severity = "HIGH"
        reason = "Port scanning behavior was reported."

    elif event_type == "failed_login" and failed_attempts >= 10:
        severity = "HIGH"
        reason = (
            f"{failed_attempts} failed login attempts were reported."
        )

    elif event_type == "failed_login":
        severity = "MEDIUM"
        reason = (
            f"{failed_attempts} failed login attempts were reported."
        )

    else:
        severity = "LOW"
        reason = "No configured high-risk pattern was detected."

    return {
        **alert,
        "severity": severity,
        "analysis_reason": reason,
        "requires_investigation": severity in {"HIGH", "MEDIUM"},
    }
