from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(tags=["Health"])

@router.get("/health/live")
def health_live():
    return {"status": "ok"}

@router.get("/health/ready")
def health_ready(db: Session = Depends(get_db)):
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "ok",
            "schema": "current"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": "error", "error": str(e)}
        )
