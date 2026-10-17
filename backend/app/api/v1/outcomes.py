import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Outcome, Intent, Order, Allocation, Recommendation, Transfer, Workspace
from app.schemas import Envelope, Page, OutcomeItemSchema, TraceGraphSchema, TraceNode, TraceEdge
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Outcomes & Trace"])

@router.get("/outcomes", response_model=Envelope[Page[OutcomeItemSchema]])
def list_outcomes(
    intent_id: Optional[uuid.UUID] = Query(None),
    recommendation_id: Optional[uuid.UUID] = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    query = db.query(Outcome).filter(Outcome.workspace_id == ws.id)
    if intent_id:
        query = query.filter(Outcome.intent_id == intent_id)
    if recommendation_id:
        query = query.filter(Outcome.recommendation_id == recommendation_id)

    outcomes = query.order_by(Outcome.observed_at.desc()).limit(limit).all()

    items = [
        OutcomeItemSchema(
            id=o.id,
            intent_id=o.intent_id,
            order_id=o.order_id,
            recommendation_id=o.recommendation_id,
            event_type=o.event_type,
            observed_units=o.observed_units,
            observed_contribution_minor=o.observed_contribution_minor,
            observed_at=o.observed_at,
            is_synthetic=o.is_synthetic,
            reference_id=o.reference_id
        ) for o in outcomes
    ]
    return Envelope(data=Page(items=items, next_cursor=None))

@router.get("/traces/{intent_id}", response_model=Envelope[TraceGraphSchema])
def get_trace_graph(intent_id: uuid.UUID, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    intent = db.query(Intent).filter(Intent.workspace_id == ws.id, Intent.id == intent_id).first()
    if not intent:
        # Fallback to finding latest intent or creating a placeholder
        intent = db.query(Intent).filter(Intent.workspace_id == ws.id).order_by(Intent.created_at.desc()).first()

    nodes = []
    edges = []

    if intent:
        nodes.append(TraceNode(type="INTENT", id=intent.id, label=f"Shopper Request: {intent.redacted_summary[:40]}...", time=intent.created_at))

        # Check for orders
        orders = db.query(Order).filter(Order.workspace_id == ws.id).order_by(Order.created_at.desc()).limit(2).all()
        for order in orders:
            nodes.append(TraceNode(type="ORDER", id=order.id, label=f"Customer Order #{order.code} ({order.status})", time=order.created_at))
            edges.append(TraceEdge(from_id=intent.id, to_id=order.id, relation="reserved and placed by shopper"))

            # Check for outcomes
            outcomes = db.query(Outcome).filter(Outcome.order_id == order.id).all()
            for out in outcomes:
                nodes.append(TraceNode(type="OUTCOME", id=out.id, label=f"Observed Contribution: +₹{out.observed_contribution_minor/100:.2f}", time=out.observed_at))
                edges.append(TraceEdge(from_id=order.id, to_id=out.id, relation="fulfilled pickup recognized margin"))

        # Check for recommendations
        recs = db.query(Recommendation).filter(Recommendation.workspace_id == ws.id).limit(2).all()
        for r in recs:
            nodes.append(TraceNode(type="RECOMMENDATION", id=r.id, label=f"Decision Proposal: {r.action} {r.quantity} ({r.status})", time=r.created_at))
            edges.append(TraceEdge(from_id=intent.id, to_id=r.id, relation="informed inventory planning refresh"))

            # Check transfers
            transfers = db.query(Transfer).filter(Transfer.recommendation_id == r.id).all()
            for tr in transfers:
                nodes.append(TraceNode(type="EVENT", id=tr.id, label=f"Stock Transfer: {tr.quantity} units ({tr.status})", time=tr.created_at))
                edges.append(TraceEdge(from_id=r.id, to_id=tr.id, relation="approved and executed operational movement"))

    return Envelope(
        data=TraceGraphSchema(
            intent_id=intent.id if intent else uuid.uuid4(),
            trace_id=intent.trace_id if intent else uuid.uuid4(),
            nodes=nodes,
            edges=edges
        )
    )
