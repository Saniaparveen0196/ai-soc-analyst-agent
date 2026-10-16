
import json
from pathlib import Path

import requests
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ALERTS_FILE = PROJECT_ROOT / "data" / "sample_alerts.json"
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Sentinel | AI SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #080d18;
        --panel: #111a2b;
        --panel-light: #172238;
        --border: #26354d;
        --text: #edf3ff;
        --muted: #93a4bd;
        --cyan: #48d9e8;
        --green: #45dfa0;
        --red: #ff647c;
        --yellow: #ffc857;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, #132542 0%, transparent 42%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(8, 13, 24, 0.8);
    }

    [data-testid="stSidebar"] {
        background: #0c1423;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: #c4d0e2;
    }

    .hero {
        padding: 25px 28px;
        border: 1px solid #2b4260;
        border-radius: 18px;
        background: linear-gradient(120deg, #142641 0%, #101a2c 60%, #112c3b 100%);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .hero-kicker {
        color: var(--cyan);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #f4f8ff;
        font-size: clamp(25px, 3vw, 36px);
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: #a6b8d1;
        font-size: 14px;
        margin-top: 10px;
        line-height: 1.7;
    }

    .section-label {
        color: #8fa4c0;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 8px 0 14px;
    }

    .metric-card {
        background: linear-gradient(145deg, #152137, #101827);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 125px;
    }

    .metric-label {
        color: #9bacc5;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 13px;
    }

    .metric-value {
        color: #f2f6ff;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-note {
        color: #8498b4;
        font-size: 11px;
        margin-top: 10px;
    }

    .panel {
        background: #101a2a;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .panel-title {
        color: #eaf1ff;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .panel-caption {
        color: #91a3bd;
        font-size: 12px;
        margin-bottom: 17px;
    }

    .severity {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 7px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: .5px;
    }

    .severity-high {
        background: #48202e;
        color: #ff8093;
        border: 1px solid #79374a;
    }

    .severity-medium {
        background: #49391c;
        color: #ffd16a;
        border: 1px solid #78602d;
    }

    .severity-low {
        background: #14392f;
        color: #65e6b0;
        border: 1px solid #24644f;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #45dfa0;
        margin-right: 8px;
        box-shadow: 0 0 10px #45dfa0;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #25c8d8, #4d9ff5);
        color: #061321;
        border: none;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 800;
        transition: all .2s ease;
    }

    div.stButton > button:hover {
        border: none;
        color: #061321;
        filter: brightness(1.12);
        box-shadow: 0 0 20px #28cbd833;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 9px;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #111d30;
        border-color: #30415c;
        border-radius: 9px;
    }

    div[data-testid="stTabs"] button {
        color: #a9bad1;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--cyan);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .footer {
        color: #6f829f;
        font-size: 11px;
        text-align: center;
        padding: 25px 0 0;
        border-top: 1px solid #1e2b40;
        margin-top: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def severity_class(severity):
    return {
        "HIGH": "severity-high",
        "MEDIUM": "severity-medium",
        "LOW": "severity-low",
    }.get(severity, "severity-low")


def api_is_healthy():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.ok
    except requests.RequestException:
        return False


def load_alerts():
    with ALERTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 8px 0 24px;">
            <div style="font-size: 30px;">🛡️</div>
            <div style="font-size: 21px; font-weight: 800; color: #f1f6ff;">
                SENTINEL<span style="color:#48d9e8;">.AI</span>
            </div>
            <div style="font-size: 10px; letter-spacing: 2px; color:#8da3c0;">
                SECURITY OPERATIONS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("#### WORKSPACE")

    page = st.radio(
        "Navigation",
        ["Overview", "Alert Investigation", "About Project"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### SYSTEM STATUS")

    healthy = api_is_healthy()

    if healthy:
        st.markdown(
            '<span class="status-dot"></span>API connected',
            unsafe_allow_html=True,
        )
    else:
        st.warning("API unavailable")

    st.caption("Local development environment")
    st.caption("FastAPI · LangGraph · FAISS · Groq")

    st.markdown("---")
    st.caption("Prototype • Synthetic sample data")


# --------------------------------------------------
# Load sample data
# --------------------------------------------------

try:
    alerts = load_alerts()
except (OSError, json.JSONDecodeError) as exc:
    st.error(f"Could not load sample alerts: {exc}")
    st.stop()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">◆ AI-POWERED THREAT TRIAGE</div>
        <div class="hero-title">Security Operations Center</div>
        <div class="hero-subtitle">
            Investigate suspicious activity, retrieve relevant security knowledge,
            and generate evidence-aware incident summaries.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Overview page
# --------------------------------------------------

if page == "Overview":
    st.markdown('<div class="section-label">COMMAND OVERVIEW</div>',
                unsafe_allow_html=True)

    # These counts describe sample records, not live network activity.
    high_count = sum(
        1 for a in alerts
        if a.get("event_type") == "port_scan"
        or (
            a.get("event_type") == "failed_login"
            and int(a.get("failed_attempts", 0)) >= 10
        )
    )
    medium_count = sum(
        1 for a in alerts
        if a.get("event_type") == "failed_login"
        and int(a.get("failed_attempts", 0)) < 10
    )
    low_count = len(alerts) - high_count - medium_count

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "SAMPLE ALERTS", len(alerts), "Loaded from local JSON"),
        (c2, "HIGH SEVERITY", high_count, "Rule-based estimate"),
        (c3, "MEDIUM SEVERITY", medium_count, "Rule-based estimate"),
        (c4, "LOW SEVERITY", low_count, "Rule-based estimate"),
    ]

    for column, label, value, note in metrics:
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.65, 1])

    with left:
        st.markdown(
            '<div class="section-label">ALERT QUEUE</div>',
            unsafe_allow_html=True,
        )

        table_rows = []

        for alert in alerts:
            event = alert.get("event_type", "")
            attempts = int(alert.get("failed_attempts", 0))

            if event == "port_scan" or (
                event == "failed_login" and attempts >= 10
            ):
                severity = "HIGH"
            elif event == "failed_login":
                severity = "MEDIUM"
            else:
                severity = "LOW"

            table_rows.append({
                "Alert ID": alert.get("alert_id"),
                "Event": event.replace("_", " ").title(),
                "Source IP": alert.get("source_ip"),
                "Severity": severity,
            })

        st.dataframe(
            table_rows,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Alert ID": st.column_config.TextColumn("ALERT ID"),
                "Event": st.column_config.TextColumn("EVENT TYPE"),
                "Source IP": st.column_config.TextColumn("SOURCE IP"),
                "Severity": st.column_config.TextColumn("SEVERITY"),
            },
        )

        st.caption(
            "Severity shown here is estimated from the current rules. "
            "These are synthetic sample alerts."
        )

    with right:
        st.markdown(
            '<div class="section-label">INVESTIGATION WORKSPACE</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">Alert analysis pipeline</div>
                <div class="panel-caption">Current prototype architecture</div>
                <p>01 &nbsp; <b>Rule engine</b><br>
                <span style="color:#91a3bd;font-size:12px;">
                Preliminary severity classification</span></p>
                <p>02 &nbsp; <b>LangGraph</b><br>
                <span style="color:#91a3bd;font-size:12px;">
                Conditional investigation workflow</span></p>
                <p>03 &nbsp; <b>FAISS retrieval</b><br>
                <span style="color:#91a3bd;font-size:12px;">
                Semantic search over security guidance</span></p>
                <p>04 &nbsp; <b>Groq LLM</b><br>
                <span style="color:#91a3bd;font-size:12px;">
                Evidence-aware investigation report</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Open investigation workspace", use_container_width=True):
            st.session_state["selected_page"] = "Alert Investigation"
            st.rerun()

    st.markdown('<div class="section-label">QUICK INVESTIGATION</div>',
                unsafe_allow_html=True)

    labels = {
        f"{a['alert_id']} — {a['event_type'].replace('_', ' ').title()}": a
        for a in alerts
    }

    selected_label = st.selectbox(
        "Select a sample alert to investigate",
        list(labels.keys()),
        key="overview_alert",
    )

    if st.button("Analyze selected alert", key="overview_analyze",
                 use_container_width=True):
        if not healthy:
            st.error("The FastAPI service is unavailable. Start the API first.")
        else:
            with st.spinner("Running the SOC investigation workflow..."):
                try:
                    response = requests.post(
                        f"{API_URL}/analyze",
                        json=labels[selected_label],
                        timeout=180,
                    )
                    response.raise_for_status()
                    st.session_state["last_result"] = response.json()
                    st.session_state["last_alert"] = labels[selected_label]
                    st.session_state["selected_page"] = "Alert Investigation"
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Analysis failed: {exc}")


# --------------------------------------------------
# Investigation page
# --------------------------------------------------

elif page == "Alert Investigation":
    st.markdown('<div class="section-label">INVESTIGATION CONSOLE</div>',
                unsafe_allow_html=True)

    labels = {
        f"{a['alert_id']} — {a['event_type'].replace('_', ' ').title()}": a
        for a in alerts
    }

    previous_alert = st.session_state.get("last_alert")
    default_index = 0

    if previous_alert:
        for index, alert in enumerate(alerts):
            if alert.get("alert_id") == previous_alert.get("alert_id"):
                default_index = index
                break

    selected_label = st.selectbox(
        "Choose alert",
        list(labels.keys()),
        index=default_index,
        key="investigation_alert",
    )

    selected_alert = labels[selected_label]

    with st.expander("View raw alert payload"):
        st.json(selected_alert)

    if st.button("Run AI investigation", use_container_width=True):
        if not api_is_healthy():
            st.error("API unavailable. Start FastAPI in another terminal.")
        else:
            with st.spinner(
                "Analyzing alert, retrieving security knowledge, "
                "and preparing report..."
            ):
                try:
                    response = requests.post(
                        f"{API_URL}/analyze",
                        json=selected_alert,
                        timeout=180,
                    )
                    response.raise_for_status()
                    st.session_state["last_result"] = response.json()
                    st.session_state["last_alert"] = selected_alert
                except requests.RequestException as exc:
                    st.error(f"Could not complete investigation: {exc}")

    result = st.session_state.get("last_result")
    result_alert = st.session_state.get("last_alert")

    if result and result_alert:
        st.markdown("---")

        st.markdown(
            f"### Investigation results — {result.get('alert_id', '')}"
        )

        severity = result.get("severity", "UNKNOWN")
        severity_html = (
            f'<span class="severity {severity_class(severity)}">'
            f'{severity}</span>'
        )

        st.markdown(
            f"""
            <div class="panel">
                <div style="display:flex;justify-content:space-between;
                            align-items:center;gap:12px;flex-wrap:wrap;">
                    <div>
                        <div style="color:#91a3bd;font-size:11px;">
                            PRELIMINARY SEVERITY
                        </div>
                        <div style="margin-top:8px;">{severity_html}</div>
                    </div>
                    <div>
                        <div style="color:#91a3bd;font-size:11px;">
                            INVESTIGATION STATUS
                        </div>
                        <div style="color:#edf3ff;font-weight:700;margin-top:8px;">
                            {"Investigation performed" if result.get("requires_investigation") else "LLM investigation skipped"}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_report, tab_knowledge, tab_related, tab_raw = st.tabs([
            "📝 Investigation report",
            "📚 Security knowledge",
            "🔗 Related alerts",
            "📦 JSON response",
        ])

        with tab_report:
            st.markdown(
                '<div class="panel-title">Analyst briefing</div>',
                unsafe_allow_html=True,
            )
            st.markdown(result.get("investigation_report", "No report returned."))

            st.download_button(
                "Download investigation report",
                data=result.get("investigation_report", ""),
                file_name=f"{result.get('alert_id', 'alert')}_report.md",
                mime="text/markdown",
            )

        with tab_knowledge:
            knowledge = result.get("security_knowledge", [])

            if not knowledge:
                st.info("No security knowledge was retrieved for this alert.")
            else:
                for item in knowledge:
                    with st.expander(item.get("topic", "Security guidance"),
                                     expanded=True):
                        st.write(item.get("content", ""))

        with tab_related:
            related = result.get("related_alerts", [])

            if not related:
                st.info("No other matching alerts were found.")
            else:
                st.dataframe(
                    related,
                    use_container_width=True,
                    hide_index=True,
                )

        with tab_raw:
            st.json(result)

            st.download_button(
                "Download JSON response",
                data=json.dumps(result, indent=2),
                file_name=f"{result.get('alert_id', 'alert')}_result.json",
                mime="application/json",
            )


# --------------------------------------------------
# About page
# --------------------------------------------------

elif page == "About Project":
    st.markdown('<div class="section-label">PROJECT INFORMATION</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Sentinel AI — SOC Analyst Prototype</div>
            <div class="panel-caption">
                AI-assisted alert triage and investigation support
            </div>
            This project demonstrates a workflow for classifying sample
            security alerts, retrieving relevant security guidance, and
            generating investigation summaries for human review.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Technology stack")
        st.markdown("""
        - **Python** — application logic
        - **FastAPI** — REST API
        - **LangGraph** — workflow and conditional routing
        - **FAISS** — semantic vector retrieval
        - **Sentence Transformers** — local embeddings
        - **Groq / LangChain** — LLM investigation
        - **Streamlit** — dashboard interface
        """)

    with col2:
        st.markdown("#### Current limitations")
        st.markdown("""
        - Uses synthetic sample alerts, not a live IDS feed
        - Severity rules are preliminary, not a trained ML detector
        - Security knowledge is a small local JSON collection
        - No authentication or persistent incident database
        - LLM recommendations require human verification
        """)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        SENTINEL.AI &nbsp; • &nbsp; AI-ASSISTED SECURITY INVESTIGATION
        <br><br>
        Prototype for investigation support. Verify findings before taking action.
    </div>
    """,
    unsafe_allow_html=True,
)
