
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from soc_agent.graph import build_soc_graph


app = FastAPI(
    title="AI SOC Analyst API",
    description=(
        "API for preliminary security alert analysis "
        "and AI-assisted investigation."
    ),
    version="1.0.0",
)


class AlertRequest(BaseModel):
    alert_id: str = Field(min_length=1)
    source_ip: str = Field(min_length=1)
    destination_ip: str = Field(min_length=1)
    event_type: Literal[
        "failed_login",
        "port_scan",
        "normal_traffic",
    ]
    failed_attempts: int = Field(default=0, ge=0)
    description: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "AI SOC Analyst API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_alert_endpoint(alert: AlertRequest):
    try:
        workflow = build_soc_graph()

        result = workflow.invoke({
            "alert": alert.model_dump(),
            "analysis": {},
            "related_alerts": [],
            "security_knowledge": [],
            "investigation_report": "",
        })

        return {
            "alert_id": result["analysis"]["alert_id"],
            "severity": result["analysis"]["severity"],
            "requires_investigation": result["analysis"][
                "requires_investigation"
            ],
            "related_alerts": result["related_alerts"],
            "security_knowledge": result["security_knowledge"],
            "investigation_report": result["investigation_report"],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Alert analysis failed: {exc}",
        ) from exc
