from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.models import ReconciliationRequest
from app.security import demo_login
from app.services import demo_dashboard_metrics, demo_disputes, demo_audit_events, run_reconciliation

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
STATIC_DIR = WEB_DIR / "static"

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}


@app.post("/api/v1/auth/demo-login")
def auth_demo_login():
    return demo_login()


@app.get("/api/v1/dashboard")
def dashboard() -> dict[str, object]:
    return {
        "tenant_id": settings.demo_tenant_id,
        "metrics": demo_dashboard_metrics(),
        "risk_regions": ["OTA commission drift", "Delayed VCC settlement", "Manual dispute aging"],
        "disputes": demo_disputes(),
        "audit_events": demo_audit_events(),
    }


@app.post("/api/v1/reconciliation/run")
def reconcile(payload: ReconciliationRequest):
    return run_reconciliation(payload)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
