import uuid
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.schemas import Envelope, SessionSchema
from app.services.seed import seed_database
from app.models import Workspace, ForecastRun
from app.services.ai import gemini_gateway

router = APIRouter(tags=["Sessions & System"])

@router.post("/demo/sessions", response_model=Envelope[SessionSchema])
def create_demo_session(
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    uid = authorization.replace("Bearer ", "").strip() or "demo-user"
    workspace = seed_database(db, owner_firebase_uid=uid)

    session_data = SessionSchema(
        workspace_id=workspace.id,
        role="DEMO_MANAGER",
        scenario_date=workspace.scenario_date,
        dataset_version=workspace.dataset_version,
        expires_at=workspace.expires_at,
        workspace_name=workspace.name
    )
    return Envelope(data=session_data)

@router.get("/system/status", response_model=Envelope[dict])
def get_system_status(db: Session = Depends(get_db)):
    latest_run = db.query(ForecastRun).order_by(ForecastRun.created_at.desc()).first()
    ai_status = gemini_gateway.get_status()
    data = {
        "app_version": "1.0.0",
        "dataset_version": settings.DATASET_VERSION,
        "ai_provider": ai_status["provider"],
        "model_id": ai_status["model"],
        "ai_configured": ai_status["ai_configured"],
        "last_ai_success_at": ai_status["last_success_at"],
        "last_ai_error": ai_status["last_error"],
        "planning_run_id": latest_run.id if latest_run else None
    }
    return Envelope(data=data)

@router.post("/sessions/reset", response_model=Envelope[dict])
@router.get("/sessions/reset", response_model=Envelope[dict])
@router.post("/demo/reset", response_model=Envelope[dict])
@router.get("/demo/reset", response_model=Envelope[dict])
def reset_demo_state(
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    """
    Reset workspace back to pristine canonical baseline.
    Restores RQ002 stock to 12 (ATP 10), clears orders/transfers, resets recommendations and catalog patches.
    """
    from app.services.seed import reset_workspace_to_canonical
    ws = reset_workspace_to_canonical(db)

    return Envelope(
        data={
            "status": "RESET_SUCCESS",
            "workspace_id": str(ws.id),
            "scenario_date": str(ws.scenario_date),
            "message": "Enterprise workspace restored to canonical baseline. Initial stock, recommendations, and catalog specs restored."
        }
    )
