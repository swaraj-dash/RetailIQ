import datetime
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import IntentEvent, Workspace
from app.schemas import Envelope, EventCreateRequest
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Events"])

@router.post("/events", response_model=Envelope[dict])
def record_event(
    req: EventCreateRequest,
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    actor_uid = authorization.replace("Bearer ", "").strip() or "demo-user"

    ev_id = uuid.uuid4()
    now = datetime.datetime.now(datetime.timezone.utc)
    ev = IntentEvent(
        id=ev_id,
        workspace_id=ws.id,
        actor_uid=actor_uid,
        session_key=req.session_key,
        intent_id=req.intent_id,
        product_id=req.product_id,
        location_id=req.location_id,
        event_type=req.event_type,
        event_time=now,
        business_date=ws.scenario_date,
        source="APP",
        is_synthetic=True
    )
    db.add(ev)
    db.commit()

    return Envelope(data={"event_id": str(ev_id), "deduplicated": False})

@router.get("/events", response_model=Envelope[list[dict]])
@router.get("/events/trace", response_model=Envelope[list[dict]])
def get_events(
    entity_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    from app.models import AuditEvent, Order, Transfer, Recommendation

    results = []

    # Get Audit Events
    audits = db.query(AuditEvent).filter(AuditEvent.workspace_id == ws.id).order_by(AuditEvent.created_at.desc()).limit(limit).all()
    for a in audits:
        results.append({
            "id": str(a.id),
            "timestamp": a.created_at.isoformat() if a.created_at else datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": a.action,
            "actor": a.actor_uid,
            "entity_type": a.entity_type,
            "entity_id": str(a.entity_id),
            "description": f"Audit Action: {a.action} on {a.entity_type} {str(a.entity_id)[:8]}",
            "details": a.details or {}
        })

    # Also include recent Orders
    orders = db.query(Order).filter(Order.workspace_id == ws.id).order_by(Order.created_at.desc()).limit(10).all()
    for o in orders:
        results.append({
            "id": str(o.id),
            "timestamp": o.created_at.isoformat() if o.created_at else datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": f"ORDER_{o.status}",
            "actor": o.actor_uid,
            "entity_type": "ORDER",
            "entity_id": o.code,
            "description": f"Order {o.code} for {o.quantity} unit(s) is {o.status}. Total ₹{o.total_minor // 100}.",
            "details": {"order_id": str(o.id), "status": o.status, "total_paise": o.total_minor}
        })

    # Also include recent Transfers
    transfers = db.query(Transfer).filter(Transfer.workspace_id == ws.id).order_by(Transfer.created_at.desc()).limit(10).all()
    for t in transfers:
        results.append({
            "id": str(t.id),
            "timestamp": t.created_at.isoformat() if t.created_at else datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": f"TRANSFER_{t.status}",
            "actor": "manager",
            "entity_type": "TRANSFER",
            "entity_id": f"TR-{str(t.id)[:8]}",
            "description": f"Transfer of {t.quantity} unit(s) from donor to recipient is {t.status}.",
            "details": {"transfer_id": str(t.id), "status": t.status, "quantity": t.quantity}
        })

    # Sort all events by timestamp descending
    results.sort(key=lambda x: x["timestamp"], reverse=True)

    if entity_type and entity_type != "ALL":
        results = [r for r in results if r["entity_type"] == entity_type]

    return Envelope(data=results[:limit])

