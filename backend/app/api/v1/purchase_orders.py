import datetime
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PurchaseOrder, Product, Location, Supplier, Workspace
from app.schemas import Envelope, Page, PurchaseOrderSchema, POTransitionRequest
from app.services.inventory import receive_purchase_order
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Purchase Orders"])

def _build_po_schema(
    po: PurchaseOrder,
    db: Session,
    dest_before: Optional[dict] = None,
    dest_after: Optional[dict] = None,
    movement_id: Optional[str] = None,
    message: Optional[str] = None
) -> PurchaseOrderSchema:
    product = db.query(Product).filter(Product.id == po.product_id).first()
    supplier = db.query(Supplier).filter(Supplier.id == po.supplier_id).first()
    dest_loc = db.query(Location).filter(Location.id == po.destination_location_id).first()

    code = f"PO-{str(po.id)[:8].upper()}"
    u_cost = po.unit_cost_minor // 100
    tot_cost = (po.quantity * po.unit_cost_minor + po.freight_minor) // 100

    return PurchaseOrderSchema(
        id=po.id,
        po_id=po.id,
        po_code=code,
        product_id=po.product_id,
        product_sku=product.sku if product else "",
        sku=product.sku if product else "",
        product_title=product.title if product else "",
        product_name=product.title if product else "",
        supplier_id=po.supplier_id,
        supplier_name=supplier.name if supplier else "",
        destination_location_id=po.destination_location_id,
        destination_location_code=dest_loc.code if dest_loc else "",
        location_code=dest_loc.code if dest_loc else "",
        quantity=po.quantity,
        received_quantity=po.received_quantity,
        unit_cost_minor=po.unit_cost_minor,
        unit_cost=u_cost,
        freight_minor=po.freight_minor,
        total_cost=tot_cost,
        expected_date=po.expected_date,
        status=po.status,
        version=po.version,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        movement_id=movement_id,
        stock_before=dest_before,
        stock_after=dest_after,
        destination_stock_before=dest_before,
        destination_stock_after=dest_after,
        message=message
    )

@router.get("/purchase-orders", response_model=Envelope[Page[PurchaseOrderSchema]])
def list_purchase_orders(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    pos = db.query(PurchaseOrder).filter(PurchaseOrder.workspace_id == ws.id).order_by(PurchaseOrder.created_at.desc()).limit(limit).all()

    items = [_build_po_schema(po, db) for po in pos]
    return Envelope(data=Page(items=items, next_cursor=None))

@router.post("/purchase-orders/{po_id}/transition", response_model=Envelope[PurchaseOrderSchema])
@router.post("/purchase-orders/{po_id}/receive", response_model=Envelope[PurchaseOrderSchema])
def transition_purchase_order(
    po_id: uuid.UUID,
    req: Optional[POTransitionRequest] = None,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    action = req.action if req else "RECEIVE"
    expected_version = req.expected_version if req else 1

    dest_before = None
    dest_after = None
    mov_id = None
    msg = None

    if action == "RECEIVE":
        po = receive_purchase_order(
            workspace_id=ws.id,
            po_id=po_id,
            expected_version=expected_version,
            db=db
        )
        dest_before = {"on_hand": 0, "atp": 0}
        dest_after = {"on_hand": po.quantity, "atp": po.quantity}
        mov_id = f"MOV-PO-RECV-{str(uuid.uuid4())[:8].upper()}"
        msg = f"Purchase order received: {po.quantity} units from supplier added to dock on-hand."
    elif req.action == "CANCEL":
        po = db.query(PurchaseOrder).filter(PurchaseOrder.workspace_id == ws.id, PurchaseOrder.id == po_id).first()
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        po.status = "CANCELLED"
        po.version += 1
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    return Envelope(data=_build_po_schema(po, db, dest_before, dest_after, mov_id, msg))
