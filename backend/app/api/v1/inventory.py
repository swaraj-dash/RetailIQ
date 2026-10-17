import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Location, Workspace
from app.schemas import Envelope, StockSchema
from app.services.inventory import get_stock_atp
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Inventory"])

@router.get("/inventory", response_model=Envelope[dict])
def get_inventory(
    product_id: uuid.UUID = Query(...),
    location_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    product = db.query(Product).filter(
        Product.workspace_id == ws.id,
        Product.id == product_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    locations_query = db.query(Location).filter(Location.workspace_id == ws.id, Location.active == True)
    if location_id:
        locations_query = locations_query.filter(Location.id == location_id)
    locations = locations_query.all()

    items = []
    for loc in locations:
        stock_info = get_stock_atp(ws.id, product.id, loc.id, db)
        items.append(
            StockSchema(
                product_id=product.id,
                location_id=loc.id,
                on_hand=stock_info["on_hand"],
                blocked=stock_info["blocked"],
                active_hold=stock_info["active_hold"],
                active_order=stock_info["active_order"],
                active_transfer=stock_info["active_transfer"],
                inventory_version=stock_info["inventory_version"],
                atp=stock_info["atp"],
                incoming_confirmed=stock_info["incoming_confirmed"],
                as_of=stock_info["as_of"]
            )
        )

    return Envelope(data={"items": items})

@router.get("/inventory/stock/{sku}", response_model=Envelope[dict])
def get_inventory_stock_sku(sku: str, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    product = db.query(Product).filter(
        Product.workspace_id == ws.id,
        Product.sku == sku
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    locations = db.query(Location).filter(Location.workspace_id == ws.id, Location.active == True).order_by(Location.code.asc()).all()
    loc_items = []
    atp_total = 0
    for loc in locations:
        st = get_stock_atp(ws.id, product.id, loc.id, db)
        atp_total += st["atp"]
        loc_items.append({
            "location_id": str(loc.id),
            "location_name": loc.name,
            "location_code": loc.code,
            "on_hand": st["on_hand"],
            "blocked": st["blocked"],
            "holds": st["active_hold"],
            "reserved_orders": st["active_order"],
            "outbound_transfers": st["active_transfer"],
            "inbound_transfers": st["incoming_confirmed"],
            "atp": st["atp"]
        })

    return Envelope(data={
        "product": {
            "id": str(product.id),
            "sku": product.sku,
            "name": product.title,
            "brand": product.brand,
            "category": "Electronics",
            "price": product.price_minor // 100,
            "status": "ACTIVE",
            "image_url": f"/images/{product.sku}.svg"
        },
        "atp_total": atp_total,
        "locations": loc_items
    })

@router.get("/inventory/stock", response_model=Envelope[list[dict]])
def get_all_inventory_stock(db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    products = db.query(Product).filter(Product.workspace_id == ws.id, Product.active == True).all()
    locations = db.query(Location).filter(Location.workspace_id == ws.id, Location.active == True).all()

    result = []
    for p in products:
        loc_items = []
        atp_total = 0
        for loc in locations:
            st = get_stock_atp(ws.id, p.id, loc.id, db)
            atp_total += st["atp"]
            loc_items.append({
                "location_id": str(loc.id),
                "location_name": loc.name,
                "location_code": loc.code,
                "on_hand": st["on_hand"],
                "blocked": st["blocked"],
                "holds": st["active_hold"],
                "reserved_orders": st["active_order"],
                "outbound_transfers": st["active_transfer"],
                "inbound_transfers": st["incoming_confirmed"],
                "atp": st["atp"]
            })
        result.append({
            "product": {
                "id": str(p.id),
                "sku": p.sku,
                "name": p.title,
                "brand": p.brand,
                "category": "Electronics",
                "price": p.price_minor // 100,
                "status": "ACTIVE",
                "image_url": f"/images/{p.sku}.svg"
            },
            "atp_total": atp_total,
            "locations": loc_items
        })

    return Envelope(data=result)

