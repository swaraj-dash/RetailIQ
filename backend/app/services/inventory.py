import datetime
import uuid
from typing import Optional, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models import (
    InventoryBalance, Allocation, Order, Transfer, PurchaseOrder,
    StockMovement, DailySale, Outcome, Recommendation, Product, Location
)

def ensure_utc(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

def get_stock_atp(workspace_id: uuid.UUID, product_id: uuid.UUID, location_id: uuid.UUID, db: Session) -> dict:
    balance = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == product_id,
        InventoryBalance.location_id == location_id
    ).first()

    on_hand = balance.on_hand if balance else 0
    blocked = balance.blocked if balance else 0
    version = balance.version if balance else 1

    now = utcnow()
    allocations = db.query(Allocation).filter(
        Allocation.workspace_id == workspace_id,
        Allocation.product_id == product_id,
        Allocation.location_id == location_id,
        Allocation.state == "ACTIVE",
        or_(Allocation.expires_at.is_(None), Allocation.expires_at > now)
    ).all()

    active_hold = sum(a.quantity for a in allocations if a.kind == "HOLD")
    active_order = sum(a.quantity for a in allocations if a.kind == "ORDER")
    active_transfer = sum(a.quantity for a in allocations if a.kind == "TRANSFER")

    sellable_physical = on_hand - blocked
    atp = sellable_physical - active_hold - active_order - active_transfer

    # Check incoming POs and incoming transfers due to this location
    incoming_pos = db.query(PurchaseOrder).filter(
        PurchaseOrder.workspace_id == workspace_id,
        PurchaseOrder.product_id == product_id,
        PurchaseOrder.destination_location_id == location_id,
        PurchaseOrder.status == "APPROVED"
    ).all()
    incoming_transfers = db.query(Transfer).filter(
        Transfer.workspace_id == workspace_id,
        Transfer.product_id == product_id,
        Transfer.destination_location_id == location_id,
        Transfer.status.in_(["APPROVED", "IN_TRANSIT"])
    ).all()
    incoming_confirmed = sum(p.quantity - p.received_quantity for p in incoming_pos) + sum(t.quantity - t.received_quantity for t in incoming_transfers)

    return {
        "product_id": product_id,
        "location_id": location_id,
        "on_hand": on_hand,
        "blocked": blocked,
        "active_hold": active_hold,
        "active_order": active_order,
        "active_transfer": active_transfer,
        "inventory_version": version,
        "atp": atp,
        "incoming_confirmed": incoming_confirmed,
        "as_of": now
    }

def create_hold(
    workspace_id: uuid.UUID,
    actor_uid: str,
    quote_id: uuid.UUID,
    quote_option_id: uuid.UUID,
    product_id: uuid.UUID,
    location_id: uuid.UUID,
    quantity: int,
    db: Session
) -> Allocation:
    # Row lock on inventory balance
    balance = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == product_id,
        InventoryBalance.location_id == location_id
    ).with_for_update().first()

    if not balance:
        raise HTTPException(status_code=404, detail="Inventory balance not found")

    stock_info = get_stock_atp(workspace_id, product_id, location_id, db)
    if stock_info["atp"] < quantity:
        raise HTTPException(status_code=409, detail="INSUFFICIENT_STOCK")

    now = utcnow()
    expires_at = now + datetime.timedelta(minutes=15)

    allocation = Allocation(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        actor_uid=actor_uid,
        product_id=product_id,
        location_id=location_id,
        quantity=quantity,
        kind="HOLD",
        state="ACTIVE",
        expires_at=expires_at,
        quote_id=quote_id,
        quote_option_id=quote_option_id,
        version=1
    )
    db.add(allocation)

    balance.version += 1
    db.commit()
    db.refresh(allocation)
    return allocation

def convert_hold_to_order(
    workspace_id: uuid.UUID,
    actor_uid: str,
    hold_id: uuid.UUID,
    expected_version: int,
    db: Session
) -> Order:
    allocation = db.query(Allocation).filter(
        Allocation.workspace_id == workspace_id,
        Allocation.id == hold_id
    ).with_for_update().first()

    if not allocation:
        raise HTTPException(status_code=404, detail="Hold not found")

    if allocation.state != "ACTIVE":
        raise HTTPException(status_code=409, detail="ALREADY_CONVERTED")

    if allocation.expires_at and ensure_utc(allocation.expires_at) < utcnow():
        allocation.state = "EXPIRED"
        db.commit()
        raise HTTPException(status_code=409, detail="HOLD_EXPIRED")

    balance = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == allocation.product_id,
        InventoryBalance.location_id == allocation.location_id
    ).with_for_update().first()

    product = db.query(Product).filter(
        Product.workspace_id == workspace_id,
        Product.id == allocation.product_id
    ).first()

    location = db.query(Location).filter(
        Location.workspace_id == workspace_id,
        Location.id == allocation.location_id
    ).first()

    # Convert hold to active order allocation
    allocation.kind = "ORDER"
    allocation.expires_at = None
    allocation.version += 1

    order_code = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    order = Order(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        code=order_code,
        actor_uid=actor_uid,
        intent_id=None,
        product_id=product.id,
        quantity=allocation.quantity,
        origin_location_id=location.id,
        demand_location_id=location.id,
        destination_code=location.locality_code,
        mode="PICKUP",
        unit_price_minor=product.price_minor,
        unit_cost_minor=product.unit_cost_minor,
        fulfillment_cost_minor=0,
        customer_fee_minor=0,
        total_minor=product.price_minor * allocation.quantity,
        status="CONFIRMED",
        version=1
    )
    db.add(order)
    allocation.order_id = order.id

    if balance:
        balance.version += 1

    db.commit()
    db.refresh(order)
    return order

def fulfill_pickup(
    workspace_id: uuid.UUID,
    order_id: uuid.UUID,
    expected_version: int,
    db: Session
) -> Order:
    order = db.query(Order).filter(
        Order.workspace_id == workspace_id,
        Order.id == order_id
    ).with_for_update().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "CONFIRMED":
        raise HTTPException(status_code=409, detail="INVALID_TRANSITION")

    balance = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == order.product_id,
        InventoryBalance.location_id == order.origin_location_id
    ).with_for_update().first()

    if not balance or balance.on_hand < order.quantity:
        raise HTTPException(status_code=409, detail="INSUFFICIENT_STOCK")

    allocation = db.query(Allocation).filter(
        Allocation.workspace_id == workspace_id,
        Allocation.order_id == order.id,
        Allocation.state == "ACTIVE"
    ).with_for_update().first()

    if allocation:
        allocation.state = "CONSUMED"
        allocation.version += 1

    balance.on_hand -= order.quantity
    balance.version += 1

    order.status = "FULFILLED"
    order.fulfilled_at = utcnow()
    order.version += 1

    # Record stock movement
    movement = StockMovement(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        product_id=order.product_id,
        location_id=order.origin_location_id,
        delta_on_hand=-order.quantity,
        delta_blocked=0,
        reason="SALE",
        reference_type="ORDER_FULFILLMENT",
        reference_id=order.id,
        operation_key=f"FULFILL:{order.id}"
    )
    db.add(movement)

    # Record outcome
    contribution = order.quantity * (order.unit_price_minor - order.unit_cost_minor) + order.customer_fee_minor - order.fulfillment_cost_minor
    outcome = Outcome(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        intent_id=order.intent_id,
        order_id=order.id,
        event_type="ORDER_FULFILLED",
        observed_units=order.quantity,
        observed_contribution_minor=contribution,
        observed_at=utcnow(),
        is_synthetic=True,
        reference_id=order.id
    )
    db.add(outcome)

    db.commit()
    db.refresh(order)
    return order

def dispatch_transfer(
    workspace_id: uuid.UUID,
    transfer_id: uuid.UUID,
    expected_version: int,
    db: Session
) -> Transfer:
    transfer = db.query(Transfer).filter(
        Transfer.workspace_id == workspace_id,
        Transfer.id == transfer_id
    ).with_for_update().first()

    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")

    if transfer.status != "APPROVED":
        raise HTTPException(status_code=409, detail="INVALID_TRANSITION")

    source_bal = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == transfer.product_id,
        InventoryBalance.location_id == transfer.source_location_id
    ).with_for_update().first()

    if not source_bal or source_bal.on_hand < transfer.quantity:
        raise HTTPException(status_code=409, detail="INSUFFICIENT_STOCK")

    alloc = db.query(Allocation).filter(
        Allocation.workspace_id == workspace_id,
        Allocation.transfer_id == transfer.id,
        Allocation.state == "ACTIVE"
    ).with_for_update().first()

    if alloc:
        alloc.state = "CONSUMED"
        alloc.version += 1

    source_bal.on_hand -= transfer.quantity
    source_bal.version += 1

    transfer.status = "IN_TRANSIT"
    transfer.version += 1

    # Record stock movement at source
    mov = StockMovement(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        product_id=transfer.product_id,
        location_id=transfer.source_location_id,
        delta_on_hand=-transfer.quantity,
        delta_blocked=0,
        reason="TRANSFER_OUT",
        reference_type="TRANSFER_DISPATCH",
        reference_id=transfer.id,
        operation_key=f"TRANSFER_DISPATCH:{transfer.id}"
    )
    db.add(mov)

    db.commit()
    db.refresh(transfer)
    return transfer

def receive_transfer(
    workspace_id: uuid.UUID,
    transfer_id: uuid.UUID,
    expected_version: int,
    db: Session
) -> Transfer:
    transfer = db.query(Transfer).filter(
        Transfer.workspace_id == workspace_id,
        Transfer.id == transfer_id
    ).with_for_update().first()

    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")

    if transfer.status != "IN_TRANSIT":
        raise HTTPException(status_code=409, detail="INVALID_TRANSITION")

    dest_bal = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == transfer.product_id,
        InventoryBalance.location_id == transfer.destination_location_id
    ).with_for_update().first()

    if not dest_bal:
        dest_bal = InventoryBalance(
            workspace_id=workspace_id,
            product_id=transfer.product_id,
            location_id=transfer.destination_location_id,
            on_hand=0,
            blocked=0,
            version=1
        )
        db.add(dest_bal)

    dest_bal.on_hand += transfer.quantity
    dest_bal.version += 1

    transfer.status = "RECEIVED"
    transfer.received_quantity = transfer.quantity
    transfer.version += 1

    # Record stock movement at destination
    mov = StockMovement(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        product_id=transfer.product_id,
        location_id=transfer.destination_location_id,
        delta_on_hand=transfer.quantity,
        delta_blocked=0,
        reason="TRANSFER_IN",
        reference_type="TRANSFER_RECEIPT",
        reference_id=transfer.id,
        operation_key=f"TRANSFER_RECEIVE:{transfer.id}"
    )
    db.add(mov)

    # Record outcome
    outcome = Outcome(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        recommendation_id=transfer.recommendation_id,
        event_type="TRANSFER_RECEIVED",
        observed_units=transfer.quantity,
        observed_contribution_minor=0,
        observed_at=utcnow(),
        is_synthetic=True,
        reference_id=transfer.id
    )
    db.add(outcome)

    if transfer.recommendation_id:
        rec = db.query(Recommendation).filter(
            Recommendation.workspace_id == workspace_id,
            Recommendation.id == transfer.recommendation_id
        ).first()
        if rec:
            rec.status = "EXECUTED"
            rec.version += 1

    db.commit()
    db.refresh(transfer)
    return transfer

def receive_purchase_order(
    workspace_id: uuid.UUID,
    po_id: uuid.UUID,
    expected_version: int,
    db: Session
) -> PurchaseOrder:
    po = db.query(PurchaseOrder).filter(
        PurchaseOrder.workspace_id == workspace_id,
        PurchaseOrder.id == po_id
    ).with_for_update().first()

    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    if po.status != "APPROVED":
        raise HTTPException(status_code=409, detail="INVALID_TRANSITION")

    dest_bal = db.query(InventoryBalance).filter(
        InventoryBalance.workspace_id == workspace_id,
        InventoryBalance.product_id == po.product_id,
        InventoryBalance.location_id == po.destination_location_id
    ).with_for_update().first()

    if not dest_bal:
        dest_bal = InventoryBalance(
            workspace_id=workspace_id,
            product_id=po.product_id,
            location_id=po.destination_location_id,
            on_hand=0,
            blocked=0,
            version=1
        )
        db.add(dest_bal)

    dest_bal.on_hand += po.quantity
    dest_bal.version += 1

    po.status = "RECEIVED"
    po.received_quantity = po.quantity
    po.version += 1

    mov = StockMovement(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        product_id=po.product_id,
        location_id=po.destination_location_id,
        delta_on_hand=po.quantity,
        delta_blocked=0,
        reason="PO_RECEIPT",
        reference_type="PO_RECEIPT",
        reference_id=po.id,
        operation_key=f"PO_RECEIVE:{po.id}"
    )
    db.add(mov)

    outcome = Outcome(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        recommendation_id=po.recommendation_id,
        event_type="PO_RECEIVED",
        observed_units=po.quantity,
        observed_contribution_minor=0,
        observed_at=utcnow(),
        is_synthetic=True,
        reference_id=po.id
    )
    db.add(outcome)

    if po.recommendation_id:
        rec = db.query(Recommendation).filter(
            Recommendation.workspace_id == workspace_id,
            Recommendation.id == po.recommendation_id
        ).first()
        if rec:
            rec.status = "EXECUTED"
            rec.version += 1

    db.commit()
    db.refresh(po)
    return po
