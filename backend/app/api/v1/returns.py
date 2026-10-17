import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Return, Order, Product, Location, InventoryBalance, StockMovement, Outcome, Workspace
from app.schemas import Envelope, ReturnSchema, ReturnCreateRequest, ReturnTransitionRequest
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Returns"])

@router.post("/returns", response_model=Envelope[ReturnSchema])
def create_return(req: ReturnCreateRequest, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    order = db.query(Order).filter(Order.workspace_id == ws.id, Order.id == req.order_id).first()
    if not order or order.status not in ["FULFILLED", "DELIVERED"]:
        raise HTTPException(status_code=400, detail="Only fulfilled orders can be returned")

    ret_id = uuid.uuid4()
    refund = order.unit_price_minor * req.quantity
    ret = Return(
        id=ret_id,
        workspace_id=ws.id,
        order_id=order.id,
        product_id=order.product_id,
        location_id=req.location_id,
        quantity=req.quantity,
        refund_minor=refund,
        status="REQUESTED",
        reason=req.reason,
        version=1
    )
    db.add(ret)
    db.commit()
    db.refresh(ret)

    return Envelope(
        data=ReturnSchema(
            id=ret.id,
            order_id=ret.order_id,
            product_id=ret.product_id,
            location_id=ret.location_id,
            quantity=ret.quantity,
            refund_minor=ret.refund_minor,
            status=ret.status,
            reason=ret.reason,
            version=ret.version
        )
    )

@router.post("/returns/{return_id}/transition", response_model=Envelope[ReturnSchema])
def transition_return(
    return_id: uuid.UUID,
    req: ReturnTransitionRequest,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    ret = db.query(Return).filter(Return.workspace_id == ws.id, Return.id == return_id).with_for_update().first()
    if not ret:
        raise HTTPException(status_code=404, detail="Return not found")

    bal = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == ws.id,
        InventoryBalance.product_id == ret.product_id,
        InventoryBalance.location_id == ret.location_id
    ).with_for_update().first()

    if req.action == "RECEIVE":
        if bal:
            bal.on_hand += ret.quantity
            bal.blocked += ret.quantity
            bal.version += 1
        ret.status = "RECEIVED"

    elif req.action == "RESTOCK":
        if bal:
            bal.blocked = max(0, bal.blocked - ret.quantity)
            bal.version += 1
        ret.status = "RESTOCKED"

    elif req.action == "DAMAGE":
        if bal:
            bal.on_hand = max(0, bal.on_hand - ret.quantity)
            bal.blocked = max(0, bal.blocked - ret.quantity)
            bal.version += 1
        ret.status = "DAMAGED"

    ret.version += 1
    db.commit()
    db.refresh(ret)

    return Envelope(
        data=ReturnSchema(
            id=ret.id,
            order_id=ret.order_id,
            product_id=ret.product_id,
            location_id=ret.location_id,
            quantity=ret.quantity,
            refund_minor=ret.refund_minor,
            status=ret.status,
            reason=ret.reason,
            version=ret.version
        )
    )
