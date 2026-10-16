
from soc_agent.alert_analyzer import analyze_alert


def test_many_failed_logins_are_high():
    alert = {
        "event_type": "failed_login",
        "failed_attempts": 18,
    }

    result = analyze_alert(alert)

    assert result["severity"] == "HIGH"
    assert result["requires_investigation"] is True


def test_few_failed_logins_are_medium():
    alert = {
        "event_type": "failed_login",
        "failed_attempts": 3,
    }

    result = analyze_alert(alert)

    assert result["severity"] == "MEDIUM"
    assert result["requires_investigation"] is True


def test_port_scan_is_high():
    alert = {
        "event_type": "port_scan",
        "failed_attempts": 0,
    }

    result = analyze_alert(alert)

    assert result["severity"] == "HIGH"


def test_normal_traffic_is_low():
    alert = {
        "event_type": "normal_traffic",
        "failed_attempts": 0,
    }

    result = analyze_alert(alert)

    assert result["severity"] == "LOW"
    assert result["requires_investigation"] is False


def test_original_alert_fields_are_preserved():
    alert = {
        "alert_id": "TEST-001",
        "source_ip": "192.168.1.25",
        "event_type": "failed_login",
        "failed_attempts": 18,
    }

    result = analyze_alert(alert)

    assert result["alert_id"] == "TEST-001"
    assert result["source_ip"] == "192.168.1.25"
