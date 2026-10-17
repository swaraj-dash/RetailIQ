import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Location, Product, ProductFact, Category, Workspace
from app.schemas import Envelope, Page, LocationSchema, ProductSchema, FactSchema

router = APIRouter(tags=["Catalog"])

def get_current_workspace(db: Session, workspace_id: Optional[uuid.UUID] = None) -> Workspace:
    if workspace_id:
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if ws:
            return ws
    ws = db.query(Workspace).order_by(Workspace.created_at.desc()).first()
    if not ws:
        from app.services.seed import seed_database
        ws = seed_database(db)
    return ws

@router.get("/locations", response_model=Envelope[dict])
def get_locations(db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    locations = db.query(Location).filter(
        Location.workspace_id == ws.id,
        Location.active == True
    ).order_by(Location.code.asc()).all()

    items = [
        LocationSchema(
            id=loc.id,
            code=loc.code,
            name=loc.name,
            kind=loc.kind,
            locality_code=loc.locality_code,
            pickup_enabled=loc.pickup_enabled,
            ship_enabled=loc.ship_enabled
        ) for loc in locations
    ]
    return Envelope(data={"items": items})

@router.get("/products", response_model=Envelope[Page[ProductSchema]])
@router.get("/catalog/products", response_model=Envelope[Page[ProductSchema]])
def get_products(
    q: Optional[str] = Query(None, max_length=120),
    category_code: Optional[str] = None,
    budget_minor: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    query = db.query(Product).filter(
        Product.workspace_id == ws.id,
        Product.active == True
    )

    if category_code:
        cat = db.query(Category).filter(Category.code == category_code).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    if budget_minor:
        query = query.filter(Product.price_minor <= budget_minor)

    if q:
        query = query.filter(Product.title.ilike(f"%{q}%") | Product.description.ilike(f"%{q}%"))

    products = query.order_by(Product.sku.asc()).limit(limit).all()

    items = []
    for p in products:
        cat = db.query(Category).filter(Category.id == p.category_id).first()
        facts = db.query(ProductFact).filter(
            ProductFact.workspace_id == ws.id,
            ProductFact.product_id == p.id
        ).all()
        fact_schemas = [
            FactSchema(
                id=f.id,
                attribute=f.attribute,
                value=f.value,
                unit=f.unit,
                source_ref=f.source_ref
            ) for f in facts
        ]
        items.append(
            ProductSchema(
                id=p.id,
                sku=p.sku,
                title=p.title,
                description=p.description,
                brand=p.brand,
                category_code=cat.code if cat else "GENERAL",
                variant_label=p.variant_label,
                price_minor=p.price_minor,
                currency=p.currency,
                image_path=p.image_path,
                facts=fact_schemas,
                published_availability=p.published_availability,
                version=p.version
            )
        )

    return Envelope(data=Page(items=items, next_cursor=None))

@router.get("/products/{product_id}", response_model=Envelope[ProductSchema])
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    p = db.query(Product).filter(
        Product.workspace_id == ws.id,
        Product.id == product_id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    cat = db.query(Category).filter(Category.id == p.category_id).first()
    facts = db.query(ProductFact).filter(
        ProductFact.workspace_id == ws.id,
        ProductFact.product_id == p.id
    ).all()
    fact_schemas = [
        FactSchema(
            id=f.id,
            attribute=f.attribute,
            value=f.value,
            unit=f.unit,
            source_ref=f.source_ref
        ) for f in facts
    ]

    return Envelope(
        data=ProductSchema(
            id=p.id,
            sku=p.sku,
            title=p.title,
            description=p.description,
            brand=p.brand,
            category_code=cat.code if cat else "GENERAL",
            variant_label=p.variant_label,
            price_minor=p.price_minor,
            currency=p.currency,
            image_path=p.image_path,
            facts=fact_schemas,
            published_availability=p.published_availability,
            version=p.version
        )
    )
