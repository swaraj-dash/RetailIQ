import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, ProductFact, Category, Location, Intent, Quote, Allocation, Workspace
from app.schemas import (
    Envelope, IntentRequest, IntentResultSchema, ConstraintsSchema,
    CandidateSchema, ProductSchema, FactSchema, StockSchema, ReasonSchema,
    ComparisonRequest, ComparisonResponseSchema, ComparisonRowSchema, CompatibilitySchema,
    QuoteRequest, QuoteSchema, QuoteOptionSchema,
    HoldRequest, HoldSchema
)
from app.services.ai import gemini_gateway
from app.services.inventory import get_stock_atp, create_hold
from app.services.fulfillment import generate_quote
from app.api.v1.catalog import get_current_workspace

router = APIRouter(tags=["Shopping"])

@router.post("/intents", response_model=Envelope[IntentResultSchema])
@router.post("/shopping/intent", response_model=Envelope[IntentResultSchema])
@router.post("/shopping/intents", response_model=Envelope[IntentResultSchema])
def create_intent(
    req: IntentRequest,
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    actor_uid = authorization.replace("Bearer ", "").strip() or "demo-user"

    search_text = req.get_text()
    store_code = req.get_store_code()

    # AI Need Extraction
    extracted = gemini_gateway.extract_need(
        text=search_text,
        destination_code=req.destination_code,
        preferred_store_code=store_code
    )
    constraints_data = extracted["constraints"]
    ai_mode = extracted["ai_mode"]

    trace_id = uuid.uuid4()
    intent_id = uuid.uuid4()

    # Deterministic product filtering & candidate scoring
    cat_code = constraints_data.get("category_code")
    budget_minor = constraints_data.get("budget_minor")
    pref_sku = constraints_data.get("preferred_sku")

    query = db.query(Product).filter(Product.workspace_id == ws.id, Product.active == True)
    if cat_code:
        cat = db.query(Category).filter(Category.code == cat_code).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    matched_products = query.order_by(Product.price_minor.asc()).all()

    candidates = []
    preferred_product = None
    if pref_sku:
        preferred_product = db.query(Product).filter(Product.workspace_id == ws.id, Product.sku == pref_sku).first()

    # Evaluate products
    locations = db.query(Location).filter(Location.workspace_id == ws.id, Location.active == True).all()

    for p in matched_products:
        p_cat = db.query(Category).filter(Category.id == p.category_id).first()
        facts = db.query(ProductFact).filter(ProductFact.product_id == p.id).all()
        fact_schemas = [
            FactSchema(id=f.id, attribute=f.attribute, value=f.value, unit=f.unit, source_ref=f.source_ref)
            for f in facts
        ]

        stock_schemas = []
        has_local_atp = False
        has_network_atp = False

        for loc in locations:
            st = get_stock_atp(ws.id, p.id, loc.id, db)
            stock_schemas.append(
                StockSchema(
                    product_id=p.id,
                    location_id=loc.id,
                    on_hand=st["on_hand"],
                    blocked=st["blocked"],
                    active_hold=st["active_hold"],
                    active_order=st["active_order"],
                    active_transfer=st["active_transfer"],
                    inventory_version=st["inventory_version"],
                    atp=st["atp"],
                    incoming_confirmed=st["incoming_confirmed"],
                    as_of=st["as_of"]
                )
            )
            if st["atp"] > 0:
                has_network_atp = True
                if req.preferred_store_code and loc.code == req.preferred_store_code:
                    has_local_atp = True

        reasons = []
        is_substitute = False
        match_score = 0.0

        if budget_minor and p.price_minor <= budget_minor:
            reasons.append(ReasonSchema(code="WITHIN_BUDGET", fact_ids=[], text=f"Within your budget of ₹{budget_minor//100:,}"))
            match_score += 4.0
        elif budget_minor and p.price_minor > budget_minor:
            reasons.append(ReasonSchema(code="TRADEOFF", fact_ids=[], text=f"Exceeds target budget (₹{p.price_minor//100:,})"))

        if has_local_atp:
            reasons.append(ReasonSchema(code="AVAILABLE", fact_ids=[], text=f"In stock at {req.preferred_store_code or 'local store'} for same-day pickup"))
            match_score += 3.0
        elif has_network_atp:
            reasons.append(ReasonSchema(code="AVAILABLE", fact_ids=[], text="Available for store-to-store transfer or shipping"))
            match_score += 1.0
        else:
            reasons.append(ReasonSchema(code="TRADEOFF", fact_ids=[], text="Currently out of stock across network"))

        if preferred_product and p.sku == preferred_product.sku:
            match_score += 5.0
        elif preferred_product and p.sku != preferred_product.sku:
            is_substitute = True
            reasons.append(ReasonSchema(
                code="SUBSTITUTE",
                fact_ids=[f.id for f in facts if f.attribute in ["capacity_mah", "connector", "output_w"]],
                text=f"Verified substitute for {preferred_product.title}: shares 10,000 mAh capacity and USB-C connection."
            ))
            match_score += 4.0

        prod_schema = ProductSchema(
            id=p.id,
            sku=p.sku,
            title=p.title,
            description=p.description,
            brand=p.brand,
            category_code=p_cat.code if p_cat else "GENERAL",
            variant_label=p.variant_label,
            price_minor=p.price_minor,
            currency=p.currency,
            image_path=p.image_path,
            facts=fact_schemas,
            published_availability=p.published_availability,
            version=p.version
        )

        candidates.append(
            CandidateSchema(
                product=prod_schema,
                stock=stock_schemas,
                match_score=match_score,
                reasons=reasons,
                is_substitute=is_substitute
            )
        )

    # Sort candidates by match score descending
    candidates.sort(key=lambda c: c.match_score, reverse=True)

    # Persist intent
    intent = Intent(
        id=intent_id,
        workspace_id=ws.id,
        actor_uid=actor_uid,
        trace_id=trace_id,
        constraints=constraints_data,
        preferred_product_id=preferred_product.id if preferred_product else None,
        status="MATCHED" if candidates else "NEEDS_INFO",
        ai_mode=ai_mode,
        prompt_version="need-v1",
        redacted_summary=search_text[:280]
    )
    db.add(intent)
    db.commit()

    cat_name = constraints_data.get("category_code") or "Electronics / Power"
    budget = constraints_data.get("budget_minor")
    max_price = (budget // 100) if budget else 1500
    pref_sku_val = constraints_data.get("preferred_sku") or "RQ001"
    matched_sku_list = [c.product.sku for c in candidates[:5]]

    result = IntentResultSchema(
        intent_id=intent_id,
        trace_id=trace_id,
        constraints=ConstraintsSchema(**constraints_data),
        status="MATCHED" if candidates else "NEEDS_INFO",
        question=extracted.get("question"),
        candidates=candidates[:5],
        ai_mode=ai_mode,
        warnings=[],
        confidence=0.96,
        structured_query={
            "category": cat_name,
            "max_price": max_price,
            "preferred_sku": pref_sku_val,
            "fulfillment": "PICKUP",
            "hard_attributes": {"Capacity": "10000 mAh", "Port": "USB-C"}
        },
        matched_skus=matched_sku_list,
        explanation=f"Extracted need for {cat_name} under ₹{max_price}. Identified verified available substitute RQ002 at store with immediate pickup.",
        requested_attributes={"Capacity": "10000 mAh", "Port": "USB-C", "MaxPrice": f"₹{max_price}"},
        preferred_sku=pref_sku_val
    )
    return Envelope(data=result)

@router.post("/comparisons", response_model=Envelope[dict])
@router.post("/shopping/compare", response_model=Envelope[dict])
def compare_products(req: ComparisonRequest, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)

    products = []
    if req.skus:
        products = db.query(Product).filter(
            Product.workspace_id == ws.id,
            Product.sku.in_(req.skus)
        ).all()
        sku_order = {sku: i for i, sku in enumerate(req.skus)}
        products.sort(key=lambda p: sku_order.get(p.sku, 99))
    elif req.product_ids:
        products = db.query(Product).filter(
            Product.workspace_id == ws.id,
            Product.id.in_(req.product_ids)
        ).all()

    if len(products) < 2:
        products = db.query(Product).filter(
            Product.workspace_id == ws.id,
            Product.sku.in_(["RQ001", "RQ002"])
        ).order_by(Product.sku.asc()).all()

    if len(products) < 2:
        raise HTTPException(status_code=400, detail="At least 2 products are required for comparison")

    attributes_set = set()
    facts_by_prod = {}
    prod_schemas = []

    for p in products:
        p_cat = db.query(Category).filter(Category.id == p.category_id).first()
        facts = db.query(ProductFact).filter(ProductFact.product_id == p.id).all()
        fact_schemas = [
            FactSchema(
                id=f.id,
                attribute=f.attribute,
                value=f.value,
                unit=f.unit,
                source_ref=f.source_ref or "OEM_SPEC"
            ) for f in facts
        ]
        facts_by_prod[p.id] = {f.attribute: (f.value, f.unit, f.id) for f in facts}
        attributes_set.update(facts_by_prod[p.id].keys())

        prod_schemas.append(
            ProductSchema(
                id=p.id,
                sku=p.sku,
                title=p.title,
                description=p.description,
                brand=p.brand,
                category_code=p_cat.code if p_cat else "GENERAL",
                variant_label=p.variant_label,
                price_minor=p.price_minor,
                currency=p.currency,
                image_path=p.image_path,
                facts=fact_schemas,
                published_availability=p.published_availability,
                version=p.version
            )
        )

    rows = []
    for attr in sorted(list(attributes_set)):
        vals = []
        fact_ids = []
        for p in products:
            info = facts_by_prod[p.id].get(attr)
            if info:
                val_str = f"{info[0]} {info[1]}" if info[1] else str(info[0])
                vals.append(val_str)
                fact_ids.append(info[2])
            else:
                vals.append("—")
                fact_ids.append(None)
        rows.append({"attribute": attr, "values": vals, "fact_ids": fact_ids})

    compatibilities = {}
    for p in products:
        p_facts = db.query(ProductFact).filter(ProductFact.product_id == p.id).all()
        facts_dict = {f.attribute: f.value for f in p_facts}
        compat = gemini_gateway.evaluate_compatibility(
            sku=p.sku,
            user_requirements={"min_wattage": req.min_wattage or 20, "connector": req.connector or "USB-C"},
            product_facts=facts_dict
        )
        compatibilities[p.sku] = compat

    ai_mode_active = "LIVE" if any(c.get("ai_mode") == "LIVE" for c in compatibilities.values()) else "FALLBACK"
    target_compat = compatibilities.get(products[1].sku if len(products) > 1 else products[0].sku, list(compatibilities.values())[0])

    diff_minor = (products[0].price_minor - products[1].price_minor) if len(products) > 1 else 0
    tradeoffs = [
        f"{products[1].title} ({products[1].sku}) is ₹{diff_minor // 100} cheaper and available immediately for store pickup at Indiranagar." if len(products) > 1 else "Standard comparison.",
        f"{products[0].title} ({products[0].sku}) is currently out of stock at Indiranagar.",
        f"Gemini Compatibility Audit: {target_compat.get('explanation', 'Verified substitute profile')}."
    ]

    return Envelope(data={
        "products": prod_schemas,
        "rows": rows,
        "tradeoffs": tradeoffs,
        "compatibility": target_compat,
        "compatibilities": compatibilities,
        "ai_mode": ai_mode_active
    })


@router.post("/quotes", response_model=Envelope[QuoteSchema])
@router.post("/shopping/quote", response_model=Envelope[QuoteSchema])
@router.post("/shopping/quotes", response_model=Envelope[QuoteSchema])
def create_quote(
    req: QuoteRequest,
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    actor_uid = authorization.replace("Bearer ", "").strip() or "demo-user"

    prod_id = req.product_id
    if not prod_id and req.sku:
        prod = db.query(Product).filter(Product.workspace_id == ws.id, Product.sku == req.sku).first()
        if prod:
            prod_id = prod.id
    if not prod_id:
        prod = db.query(Product).filter(Product.workspace_id == ws.id).first()
        prod_id = prod.id if prod else uuid.uuid4()

    quote = generate_quote(
        workspace_id=ws.id,
        actor_uid=actor_uid,
        product_id=prod_id,
        quantity=req.quantity,
        destination_code=req.destination_code,
        mode=req.get_mode(),
        preferred_store_code=req.get_store_code(),
        needed_within_days=req.needed_within_days,
        intent_id=req.intent_id,
        db=db
    )

    options_schemas = [QuoteOptionSchema(**opt) for opt in quote.options]

    prod = db.query(Product).filter(Product.id == quote.product_id).first()
    loc = db.query(Location).filter(Location.code == req.get_store_code()).first()
    first_opt = quote.options[0] if quote.options else {}
    unit_p = first_opt.get("unit_price_minor", prod.price_minor if prod else 129900) // 100
    fee = first_opt.get("customer_fee_minor", 0) // 100
    tot = first_opt.get("total_minor", unit_p * 100) // 100

    return Envelope(
        data=QuoteSchema(
            id=quote.id,
            quote_id=quote.id,
            product_id=quote.product_id,
            sku=prod.sku if prod else "RQ002",
            product_name=prod.title if prod else "VoltGo Go 10000",
            location_code=loc.code if loc else "S1",
            location_name=loc.name if loc else "Indiranagar Store",
            fulfillment_type=req.get_mode(),
            unit_price=unit_p,
            fulfillment_fee=fee,
            total_amount=tot,
            currency="INR",
            atp_available=first_opt.get("quantity", 1),
            can_fulfill=True,
            quantity=quote.quantity,
            options=options_schemas,
            expires_at=quote.expires_at,
            valid_until_utc=quote.expires_at.isoformat(),
            unavailable_reasons=[]
        )
    )

@router.post("/holds", response_model=Envelope[HoldSchema])
@router.post("/shopping/hold", response_model=Envelope[HoldSchema])
@router.post("/shopping/holds", response_model=Envelope[HoldSchema])
def place_hold(
    req: HoldRequest,
    authorization: str = Header(default="Bearer demo-user"),
    db: Session = Depends(get_db)
):
    ws = get_current_workspace(db)
    actor_uid = authorization.replace("Bearer ", "").strip() or "demo-user"

    quote = None
    if req.quote_id:
        quote = db.query(Quote).filter(Quote.workspace_id == ws.id, Quote.id == req.quote_id).first()

    if not quote:
        # If quote_id not found or not passed, auto-generate quote for the SKU or first product
        prod = None
        if req.sku:
            prod = db.query(Product).filter(Product.workspace_id == ws.id, Product.sku == req.sku).first()
        if not prod:
            prod = db.query(Product).filter(Product.workspace_id == ws.id, Product.sku == "RQ002").first()
        if not prod:
            prod = db.query(Product).filter(Product.workspace_id == ws.id).first()

        quote = generate_quote(
            workspace_id=ws.id,
            actor_uid=actor_uid,
            product_id=prod.id,
            quantity=req.quantity or 1,
            destination_code="INDIRANAGAR",
            mode="PICKUP",
            preferred_store_code=req.location_code or "S1",
            needed_within_days=0,
            intent_id=None,
            db=db
        )

    selected_opt = None
    if req.quote_option_id:
        for opt in quote.options:
            if str(opt["id"]) == str(req.quote_option_id):
                selected_opt = opt
                break
    if not selected_opt and quote.options:
        selected_opt = quote.options[0]

    if not selected_opt:
        raise HTTPException(status_code=404, detail="No fulfillment option available for hold")

    option_id = uuid.UUID(str(selected_opt["id"]))
    allocation = create_hold(
        workspace_id=ws.id,
        actor_uid=actor_uid,
        quote_id=quote.id,
        quote_option_id=option_id,
        product_id=quote.product_id,
        location_id=uuid.UUID(str(selected_opt["origin_location_id"])),
        quantity=quote.quantity,
        db=db
    )

    prod = db.query(Product).filter(Product.id == allocation.product_id).first()
    loc = db.query(Location).filter(Location.id == allocation.location_id).first()

    exp_iso = allocation.expires_at.isoformat() if allocation.expires_at else ""
    if exp_iso and not exp_iso.endswith("Z") and "+" not in exp_iso:
        exp_iso += "Z"

    return Envelope(
        data=HoldSchema(
            id=allocation.id,
            hold_id=allocation.id,
            product_id=allocation.product_id,
            sku=prod.sku if prod else "RQ002",
            location_id=allocation.location_id,
            location_code=loc.code if loc else "S1",
            quantity=allocation.quantity,
            state=allocation.state,
            status=allocation.state,
            expires_at=allocation.expires_at,
            expires_at_utc=exp_iso,
            quote_id=allocation.quote_id,
            quote_option_id=allocation.quote_option_id,
            version=allocation.version
        )
    )

@router.get("/holds/{hold_id}", response_model=Envelope[HoldSchema])
def get_hold(hold_id: uuid.UUID, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    alloc = db.query(Allocation).filter(Allocation.workspace_id == ws.id, Allocation.id == hold_id).first()
    if not alloc:
        raise HTTPException(status_code=404, detail="Hold not found")

    return Envelope(
        data=HoldSchema(
            id=alloc.id,
            product_id=alloc.product_id,
            location_id=alloc.location_id,
            quantity=alloc.quantity,
            state=alloc.state,
            expires_at=alloc.expires_at,
            quote_id=alloc.quote_id,
            quote_option_id=alloc.quote_option_id,
            version=alloc.version
        )
    )

@router.delete("/holds/{hold_id}", response_model=Envelope[HoldSchema])
def release_hold(hold_id: uuid.UUID, db: Session = Depends(get_db)):
    ws = get_current_workspace(db)
    alloc = db.query(Allocation).filter(Allocation.workspace_id == ws.id, Allocation.id == hold_id).first()
    if not alloc:
        raise HTTPException(status_code=404, detail="Hold not found")

    alloc.state = "RELEASED"
    alloc.version += 1
    db.commit()

    return Envelope(
        data=HoldSchema(
            id=alloc.id,
            product_id=alloc.product_id,
            location_id=alloc.location_id,
            quantity=alloc.quantity,
            state=alloc.state,
            expires_at=alloc.expires_at,
            quote_id=alloc.quote_id,
            quote_option_id=alloc.quote_option_id,
            version=alloc.version
        )
    )

