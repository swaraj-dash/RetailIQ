import datetime
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Product, Location, Lane, Quote
from app.services.inventory import get_stock_atp

def generate_quote(
    workspace_id: uuid.UUID,
    actor_uid: str,
    product_id: uuid.UUID,
    quantity: int,
    destination_code: str,
    mode: str, # ANY, PICKUP, SHIP
    preferred_store_code: Optional[str],
    needed_within_days: Optional[int],
    intent_id: Optional[uuid.UUID],
    db: Session
) -> Quote:
    product = db.query(Product).filter(
        Product.workspace_id == workspace_id,
        Product.id == product_id
    ).first()

    locations = db.query(Location).filter(
        Location.workspace_id == workspace_id,
        Location.active == True
    ).all()

    options = []
    unavailable_reasons = []

    # 1. Pickup options
    if mode in ["ANY", "PICKUP"]:
        for loc in locations:
            if not loc.pickup_enabled:
                continue
            
            # If preferred store specified, prioritize
            stock_info = get_stock_atp(workspace_id, product.id, loc.id, db)
            lead_days = 0

            if needed_within_days is not None and lead_days > needed_within_days:
                continue

            if stock_info["atp"] >= quantity:
                opt_id = uuid.uuid4()
                option = {
                    "id": str(opt_id),
                    "origin_location_id": str(loc.id),
                    "origin_location_code": loc.code,
                    "origin_location_name": loc.name,
                    "mode": "PICKUP",
                    "quantity": quantity,
                    "unit_price_minor": product.price_minor,
                    "customer_fee_minor": 0,
                    "fulfillment_cost_minor": 0,
                    "total_minor": product.price_minor * quantity,
                    "lead_days": lead_days,
                    "promise_kind": "SIMULATED_ESTIMATE",
                    "inventory_version": stock_info["inventory_version"],
                    "recommendation_reason": f"Available for same-day store pickup at {loc.name}"
                }
                options.append(option)
            else:
                unavailable_reasons.append(f"Pickup at {loc.name} out of stock (ATP: {stock_info['atp']})")

    # 2. Shipping options
    if mode in ["ANY", "SHIP"]:
        lanes = db.query(Lane).filter(
            Lane.workspace_id == workspace_id,
            Lane.destination_code == destination_code,
            Lane.mode == "SHIP",
            Lane.active == True
        ).all()

        for lane in lanes:
            orig_loc = db.query(Location).filter(Location.id == lane.origin_location_id).first()
            if not orig_loc or not orig_loc.ship_enabled:
                continue

            stock_info = get_stock_atp(workspace_id, product.id, orig_loc.id, db)
            if needed_within_days is not None and lane.lead_days > needed_within_days:
                continue

            if stock_info["atp"] >= quantity:
                fulfillment_cost = lane.fixed_cost_minor + (lane.unit_cost_minor * quantity)
                opt_id = uuid.uuid4()
                option = {
                    "id": str(opt_id),
                    "origin_location_id": str(orig_loc.id),
                    "origin_location_code": orig_loc.code,
                    "origin_location_name": orig_loc.name,
                    "mode": "SHIP",
                    "quantity": quantity,
                    "unit_price_minor": product.price_minor,
                    "customer_fee_minor": 4900, # Fixed customer shipping fee ₹49
                    "fulfillment_cost_minor": fulfillment_cost,
                    "total_minor": (product.price_minor * quantity) + 4900,
                    "lead_days": lane.lead_days,
                    "promise_kind": "SIMULATED_ESTIMATE",
                    "inventory_version": stock_info["inventory_version"],
                    "recommendation_reason": f"Standard delivery from {orig_loc.name} in {lane.lead_days} day(s)"
                }
                options.append(option)
            else:
                unavailable_reasons.append(f"Shipment from {orig_loc.name} out of stock (ATP: {stock_info['atp']})")

    # Sort options: shortest lead_days, lowest total, origin code
    options.sort(key=lambda o: (o["lead_days"], o["total_minor"], o["origin_location_code"]))

    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=300) # 5 minutes expiry

    quote = Quote(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        actor_uid=actor_uid,
        intent_id=intent_id,
        product_id=product.id,
        quantity=quantity,
        destination_code=destination_code,
        options=options,
        expires_at=expires_at,
        status="OPEN"
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote
