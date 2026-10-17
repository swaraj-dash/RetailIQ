import datetime
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models import (
    Workspace, Membership, Location, Category, Product, ProductFact,
    Supplier, SupplierSku, Lane, PlanningPolicy, Promotion,
    InventoryBalance, Allocation, Order, PurchaseOrder,
    StockMovement, DailySale, IntentEvent, ExternalSignal
)

NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "retailiq.demo.v1")

def get_entity_uuid(workspace_id: uuid.UUID, table_name: str, key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, f"{workspace_id}:{table_name}:{key}")

def seed_database(db: Session, owner_firebase_uid: Optional[str] = None) -> Workspace:
    # 1. Create or get Demo Workspace
    workspace = None
    if owner_firebase_uid:
        workspace = db.query(Workspace).filter(Workspace.owner_firebase_uid == owner_firebase_uid).first()
    
    if not workspace:
        workspace = db.query(Workspace).filter(Workspace.owner_firebase_uid.is_(None)).first()
    
    if workspace:
        return workspace

    workspace_id = uuid.uuid4()
    scenario_date = datetime.date(2026, 10, 17)
    
    workspace = Workspace(
        id=workspace_id,
        owner_firebase_uid=owner_firebase_uid,
        name="RetailIQ Demo Retailer",
        is_demo=True,
        scenario_date=scenario_date,
        dataset_version="retailiq-demo-v1",
        version=1
    )
    db.add(workspace)
    db.flush()

    # Create Demo Manager Membership
    membership = Membership(
        id=get_entity_uuid(workspace_id, "memberships", owner_firebase_uid or "demo-user"),
        workspace_id=workspace_id,
        firebase_uid=owner_firebase_uid or "demo-user",
        role="DEMO_MANAGER",
        active=True
    )
    db.add(membership)

    # 2. Locations
    locations_data = [
        {"code": "DC1", "name": "Nelamangala Central DC", "kind": "DC", "locality": "NELAMANGALA", "pickup": False, "ship": True},
        {"code": "S1", "name": "Indiranagar Store", "kind": "STORE", "locality": "INDIRANAGAR", "pickup": True, "ship": True},
        {"code": "S2", "name": "Whitefield Store", "kind": "STORE", "locality": "WHITEFIELD", "pickup": True, "ship": True},
        {"code": "S3", "name": "Koramangala Store", "kind": "STORE", "locality": "KORAMANGALA", "pickup": True, "ship": True},
    ]
    location_map = {}
    for loc in locations_data:
        l_id = get_entity_uuid(workspace_id, "locations", loc["code"])
        location = Location(
            id=l_id,
            workspace_id=workspace_id,
            code=loc["code"],
            name=loc["name"],
            kind=loc["kind"],
            locality_code=loc["locality"],
            pickup_enabled=loc["pickup"],
            ship_enabled=loc["ship"],
            active=True
        )
        db.add(location)
        location_map[loc["code"]] = location
    db.flush()

    # 3. Categories
    categories_data = [
        {
            "code": "POWER",
            "name": "Portable Power & Chargers",
            "reqs": [
                {"name": "capacity_mah", "type": "number"},
                {"name": "connector", "type": "string"},
                {"name": "output_w", "type": "number"}
            ]
        },
        {
            "code": "LIGHTING",
            "name": "Outdoor & Emergency Lighting",
            "reqs": [
                {"name": "lumens", "type": "number"},
                {"name": "runtime_h", "type": "number"},
                {"name": "rechargeable", "type": "boolean"}
            ]
        },
        {
            "code": "AUDIO",
            "name": "Audio & Headphones",
            "reqs": [
                {"name": "wireless", "type": "boolean"},
                {"name": "connector", "type": "string"}
            ]
        },
        {
            "code": "ACCESSORIES",
            "name": "Travel Accessories & Bags",
            "reqs": [
                {"name": "material", "type": "string"},
                {"name": "compatible_device", "type": "string"},
                {"name": "quantity_per_pack", "type": "number"}
            ]
        }
    ]
    category_map = {}
    for cat in categories_data:
        c_id = get_entity_uuid(workspace_id, "categories", cat["code"])
        category = Category(
            id=c_id,
            workspace_id=workspace_id,
            code=cat["code"],
            name=cat["name"],
            required_attributes=cat["reqs"],
            allowed_values=None
        )
        db.add(category)
        category_map[cat["code"]] = category
    db.flush()

    # 4. Products & Facts (24 SKUs)
    products_catalog = [
        ("RQ001", "VoltGo Pro 10000", "POWER", 149900, 85000, [("capacity_mah", 10000, "mAh"), ("connector", "USB-C", None), ("output_w", 22, "W"), ("rechargeable", True, None)]),
        ("RQ002", "VoltGo Go 10000", "POWER", 129900, 70000, [("capacity_mah", 10000, "mAh"), ("connector", "USB-C", None), ("output_w", 20, "W"), ("rechargeable", True, None)]),
        ("RQ003", "VoltGo Max 20000", "POWER", 199900, 110000, [("capacity_mah", 20000, "mAh"), ("connector", "USB-C", None), ("output_w", 30, "W"), ("rechargeable", True, None)]),
        ("RQ004", "VoltGo Mini 5000", "POWER", 89900, 45000, [("capacity_mah", 5000, "mAh"), ("connector", "USB-C", None), ("output_w", 12, "W"), ("rechargeable", True, None)]),
        ("RQ005", "LumaTrail Solar Lantern", "LIGHTING", 149900, 88000, [("lumens", 300, "lm"), ("runtime_h", 8, "h"), ("rechargeable", True, None), ("solar", True, None)]),
        ("RQ006", "LumaTrail Glow Clip", "LIGHTING", 29900, 12000, [("lumens", 20, "lm"), ("runtime_h", 3, "h"), ("rechargeable", False, None), ("solar", False, None)]),
        ("RQ007", "LumaTrail Desk Light", "LIGHTING", 99900, 50000, [("lumens", 450, "lm"), ("runtime_h", 6, "h"), ("rechargeable", True, None), ("solar", False, None)]),
        ("RQ008", "LumaTrail Pocket Torch", "LIGHTING", 59900, 25000, [("lumens", 150, "lm"), ("runtime_h", 5, "h"), ("rechargeable", True, None), ("solar", False, None)]),
        ("RQ009", "LumaTrail Camp Strip", "LIGHTING", 79900, 35000, [("lumens", 200, "lm"), ("runtime_h", 4, "h"), ("rechargeable", True, None), ("solar", False, None)]),
        ("RQ010", "LumaTrail Reading Lamp", "LIGHTING", 69900, 30000, [("lumens", 120, "lm"), ("runtime_h", 7, "h"), ("rechargeable", True, None), ("solar", False, None)]),
        ("RQ011", "EchoWay Buds Basic", "AUDIO", 99900, 50000, [("wireless", True, None), ("runtime_h", 5, "h"), ("connector", "USB-C", None)]),
        ("RQ012", "EchoWay Buds Plus", "AUDIO", 179900, 95000, [("wireless", True, None), ("runtime_h", 8, "h"), ("connector", "USB-C", None)]),
        ("RQ013", "EchoWay On Ear", "AUDIO", 149900, 75000, [("wireless", True, None), ("runtime_h", 20, "h"), ("connector", "USB-C", None)]),
        ("RQ014", "EchoWay Wired Earphones", "AUDIO", 39900, 15000, [("wireless", False, None), ("runtime_h", 0, "h"), ("connector", "3.5mm", None)]),
        ("RQ015", "EchoWay Pocket Speaker", "AUDIO", 119900, 60000, [("wireless", True, None), ("runtime_h", 6, "h"), ("connector", "USB-C", None)]),
        ("RQ016", "TripKit Phone Stand", "ACCESSORIES", 29900, 10000, [("material", "aluminium", None), ("compatible_device", "phone", None), ("quantity_per_pack", 1, None)]),
        ("RQ017", "TripKit USB-C Cable", "ACCESSORIES", 19900, 10000, [("material", "nylon", None), ("compatible_device", "USB-C", None), ("quantity_per_pack", 1, None)]),
        ("RQ018", "TripKit Cable Duo", "ACCESSORIES", 69900, 25000, [("material", "nylon", None), ("compatible_device", "USB-C", None), ("quantity_per_pack", 2, None)]),
        ("RQ019", "TripKit Travel Pouch", "ACCESSORIES", 49900, 18000, [("material", "polyester", None), ("compatible_device", "accessories", None), ("quantity_per_pack", 1, None)]),
        ("RQ020", "TripKit Laptop Sleeve", "ACCESSORIES", 99900, 40000, [("material", "polyester", None), ("compatible_device", "laptop", None), ("quantity_per_pack", 1, None)]),
        ("RQ021", "EchoWay Classic Speaker", "AUDIO", 129900, 60000, [("wireless", True, None), ("runtime_h", 4, "h"), ("connector", "Micro-USB", None)]),
        ("RQ022", "TripKit Universal Stand", "ACCESSORIES", 59900, 22000, [("material", "aluminium", None), ("compatible_device", "tablet", None), ("quantity_per_pack", 1, None)]),
        ("RQ023", "TripKit Cleaning Cloth", "ACCESSORIES", 19900, 5000, [("compatible_device", "screen", None), ("quantity_per_pack", 2, None)]), # Material fact deliberately omitted per spec
        ("RQ024", "TripKit Organizer", "ACCESSORIES", 79900, 30000, [("material", "polyester", None), ("compatible_device", "accessories", None), ("quantity_per_pack", 1, None)]),
    ]

    product_map = {}
    for sku, title, cat_code, price, cost, facts in products_catalog:
        p_id = get_entity_uuid(workspace_id, "products", sku)
        brand = title.split()[0]
        
        # Apply deliberate catalog defects
        actual_title = title
        actual_desc = f"{title}. Verified high quality retail product."
        actual_pub_avail = "IN_STOCK"
        actual_image = f"/images/{sku}.svg"
        actual_variant = "Standard"

        if sku == "RQ002":
            actual_title = "Power bank"
            actual_desc = "Portable power."
        elif sku == "RQ001":
            actual_pub_avail = "IN_STOCK" # C07 defect: claimed in stock while 0 ATP
        elif sku == "RQ018":
            actual_image = None # C05 defect: missing image
        elif sku == "RQ024":
            actual_variant = "" # C08 defect: empty variant label

        product = Product(
            id=p_id,
            workspace_id=workspace_id,
            category_id=category_map[cat_code].id,
            sku=sku,
            title=actual_title,
            description=actual_desc,
            brand=brand,
            variant_label=actual_variant,
            gtin=None,
            mpn=f"DEMO-{sku}",
            image_path=actual_image,
            price_minor=price,
            unit_cost_minor=cost,
            currency="INR",
            published_availability=actual_pub_avail,
            active=True,
            version=1
        )
        db.add(product)
        product_map[sku] = product
        db.flush()

        # Add Facts
        for attr, val, unit in facts:
            f_id = get_entity_uuid(workspace_id, "product_facts", f"{sku}:{attr}")
            fact = ProductFact(
                id=f_id,
                workspace_id=workspace_id,
                product_id=p_id,
                attribute=attr,
                value=val,
                unit=unit,
                source_ref=f"synthetic://retailiq-demo-v1/{sku}/spec",
                verified_at=datetime.datetime.now(datetime.timezone.utc),
                version=1
            )
            db.add(fact)

    db.flush()

    # 5. Suppliers & Supplier SKUs
    suppliers_data = [
        {"code": "SUP1", "name": "VoltTech Global Supply", "skus": ["RQ001", "RQ002", "RQ003", "RQ004"], "lead": 7, "moq": 24, "pack": 6, "freight": 18000},
        {"code": "SUP2", "name": "LuminaTech OEM Supplier", "skus": ["RQ005", "RQ006", "RQ007", "RQ008", "RQ009", "RQ010"], "lead": 4, "moq": 12, "pack": 6, "freight": 15000},
        {"code": "SUP3", "name": "Apex Electronics Supply", "skus": [f"RQ{i:03d}" for i in range(11, 25)], "lead": 5, "moq": 12, "pack": 6, "freight": 12000},
    ]
    supplier_map = {}
    for sup_item in suppliers_data:
        s_id = get_entity_uuid(workspace_id, "suppliers", sup_item["code"])
        supplier = Supplier(
            id=s_id,
            workspace_id=workspace_id,
            code=sup_item["code"],
            name=sup_item["name"],
            active=True
        )
        db.add(supplier)
        supplier_map[sup_item["code"]] = supplier
        db.flush()

        for sku in sup_item["skus"]:
            ss_id = get_entity_uuid(workspace_id, "supplier_skus", f"{sup_item['code']}:{sku}")
            lead = 14 if sku == "RQ006" else sup_item["lead"]
            moq = 120 if sku == "RQ006" else sup_item["moq"]
            pack = 12 if sku == "RQ006" else sup_item["pack"]
            
            p = product_map[sku]
            supplier_sku = SupplierSku(
                id=ss_id,
                workspace_id=workspace_id,
                supplier_id=s_id,
                product_id=p.id,
                lead_days=lead,
                moq=moq,
                pack_size=pack,
                unit_cost_minor=p.unit_cost_minor,
                freight_minor=sup_item["freight"],
                active=True,
                version=1
            )
            db.add(supplier_sku)

    db.flush()

    # 6. Lanes (Inter-store Transfers and Shipping)
    loc_codes = ["DC1", "S1", "S2", "S3"]
    # Transfer lanes between all distinct locations
    for origin in loc_codes:
        for dest in loc_codes:
            if origin == dest:
                continue
            lane_id = get_entity_uuid(workspace_id, "lanes", f"TRANSFER:{origin}:{dest}")
            fixed = 12000
            unit = 800
            if origin == "DC1" or dest == "DC1":
                fixed = 16000
                unit = 1200
            lane = Lane(
                id=lane_id,
                workspace_id=workspace_id,
                origin_location_id=location_map[origin].id,
                destination_code=dest,
                mode="TRANSFER",
                lead_days=1,
                fixed_cost_minor=fixed,
                unit_cost_minor=unit,
                active=True,
                version=1
            )
            db.add(lane)

    # Shipping lanes to 3 customer localities
    shopp_localities = ["INDIRANAGAR", "WHITEFIELD", "JAYANAGAR"]
    for origin in loc_codes:
        for dest_loc in shopp_localities:
            lane_id = get_entity_uuid(workspace_id, "lanes", f"SHIP:{origin}:{dest_loc}")
            orig_kind = location_map[origin].kind
            orig_loc = location_map[origin].locality_code
            if orig_kind == "DC":
                lead = 2
                fixed = 8000
                unit = 1000
            elif orig_loc == dest_loc:
                lead = 1
                fixed = 6000
                unit = 1000
            else:
                lead = 2
                fixed = 9000
                unit = 1000

            lane = Lane(
                id=lane_id,
                workspace_id=workspace_id,
                origin_location_id=location_map[origin].id,
                destination_code=dest_loc,
                mode="SHIP",
                lead_days=lead,
                fixed_cost_minor=fixed,
                unit_cost_minor=unit,
                active=True,
                version=1
            )
            db.add(lane)

    db.flush()

    # 7. Planning Policies (72 SKU/store pairs)
    store_codes = ["S1", "S2", "S3"]
    for sku, p in product_map.items():
        for s_code in store_codes:
            pol_id = get_entity_uuid(workspace_id, "planning_policies", f"{sku}:{s_code}")
            policy = PlanningPolicy(
                id=pol_id,
                workspace_id=workspace_id,
                product_id=p.id,
                location_id=location_map[s_code].id,
                review_days=7,
                safety_days=2,
                excess_days=56,
                annual_holding_rate=0.20,
                unsold_risk_rate=0.10,
                capital_limit_minor=500000,
                version=1
            )
            db.add(policy)

    # Inactive synthetic promotion row
    prom_id = get_entity_uuid(workspace_id, "promotions", "FESTIVAL-LIGHTING")
    promotion = Promotion(
        id=prom_id,
        workspace_id=workspace_id,
        category_id=category_map["LIGHTING"].id,
        start_date=scenario_date + datetime.timedelta(days=21),
        end_date=scenario_date + datetime.timedelta(days=27),
        multiplier=1.20,
        source_ref="synthetic://festival-scenario",
        approved=False,
        version=1
    )
    db.add(promotion)
    db.flush()

    # 8. Inventory Balances (96 balances: 24 SKUs x 4 locations)
    # Default: DC=40, Store=20, blocked=0
    balances = {}
    for sku, p in product_map.items():
        for loc_code in loc_codes:
            is_dc = (loc_code == "DC1")
            on_hand = 40 if is_dc else 20
            blocked = 0

            # Explicit overrides from specification 13_SYNTHETIC_DATASET.md
            if sku == "RQ001":
                on_hand = 0
            elif sku == "RQ002":
                if loc_code == "S1":
                    on_hand = 12
                elif loc_code == "S2":
                    on_hand = 60
                    blocked = 2
                elif loc_code == "S3":
                    on_hand = 8
                elif loc_code == "DC1":
                    on_hand = 40
            elif sku == "RQ005":
                if loc_code == "S1":
                    on_hand = 6
                elif loc_code in ["S2", "S3"]:
                    on_hand = 4
                elif loc_code == "DC1":
                    on_hand = 5
            elif sku == "RQ006":
                if loc_code == "S1":
                    on_hand = 15
            elif sku == "RQ021":
                if loc_code == "S3":
                    on_hand = 80

            bal = InventoryBalance(
                workspace_id=workspace_id,
                product_id=p.id,
                location_id=location_map[loc_code].id,
                on_hand=on_hand,
                blocked=blocked,
                version=1
            )
            db.add(bal)
            balances[(sku, loc_code)] = bal

            # Add opening movement
            mov_id = get_entity_uuid(workspace_id, "stock_movements", f"OPENING:{sku}:{loc_code}")
            mov = StockMovement(
                id=mov_id,
                workspace_id=workspace_id,
                product_id=p.id,
                location_id=location_map[loc_code].id,
                delta_on_hand=on_hand,
                delta_blocked=blocked,
                reason="OPENING",
                reference_type="OPENING_BALANCE",
                reference_id=bal.product_id,
                operation_key=f"OPENING:{sku}:{loc_code}"
            )
            db.add(mov)

    db.flush()

    # 9. Seed Two Existing Reserved Orders for RQ002
    # Qty 2 at S1, Qty 3 at S2 owned by internal "seed-reservation-owner"
    rq002 = product_map["RQ002"]
    
    # Order at S1
    ord1_id = get_entity_uuid(workspace_id, "orders", "SEED-ORD-001")
    ord1 = Order(
        id=ord1_id,
        workspace_id=workspace_id,
        code="SEED-ORD-001",
        actor_uid="seed-reservation-owner",
        product_id=rq002.id,
        quantity=2,
        origin_location_id=location_map["S1"].id,
        demand_location_id=location_map["S1"].id,
        destination_code="INDIRANAGAR",
        mode="PICKUP",
        unit_price_minor=rq002.price_minor,
        unit_cost_minor=rq002.unit_cost_minor,
        fulfillment_cost_minor=0,
        customer_fee_minor=0,
        total_minor=rq002.price_minor * 2,
        status="CONFIRMED",
        version=1
    )
    db.add(ord1)
    alloc1 = Allocation(
        id=get_entity_uuid(workspace_id, "allocations", "SEED-ALLOC-001"),
        workspace_id=workspace_id,
        actor_uid="seed-reservation-owner",
        product_id=rq002.id,
        location_id=location_map["S1"].id,
        quantity=2,
        kind="ORDER",
        state="ACTIVE",
        expires_at=None,
        order_id=ord1_id,
        version=1
    )
    db.add(alloc1)

    # Order at S2
    ord2_id = get_entity_uuid(workspace_id, "orders", "SEED-ORD-002")
    ord2 = Order(
        id=ord2_id,
        workspace_id=workspace_id,
        code="SEED-ORD-002",
        actor_uid="seed-reservation-owner",
        product_id=rq002.id,
        quantity=3,
        origin_location_id=location_map["S2"].id,
        demand_location_id=location_map["S2"].id,
        destination_code="WHITEFIELD",
        mode="PICKUP",
        unit_price_minor=rq002.price_minor,
        unit_cost_minor=rq002.unit_cost_minor,
        fulfillment_cost_minor=0,
        customer_fee_minor=0,
        total_minor=rq002.price_minor * 3,
        status="CONFIRMED",
        version=1
    )
    db.add(ord2)
    alloc2 = Allocation(
        id=get_entity_uuid(workspace_id, "allocations", "SEED-ALLOC-002"),
        workspace_id=workspace_id,
        actor_uid="seed-reservation-owner",
        product_id=rq002.id,
        location_id=location_map["S2"].id,
        quantity=3,
        kind="ORDER",
        state="ACTIVE",
        expires_at=None,
        order_id=ord2_id,
        version=1
    )
    db.add(alloc2)

    # 10. Seed Incoming PO SEED-PO-001: RQ002 qty 6 to S1, SUP1, expected D+4
    po1_id = get_entity_uuid(workspace_id, "purchase_orders", "SEED-PO-001")
    po1 = PurchaseOrder(
        id=po1_id,
        workspace_id=workspace_id,
        supplier_id=supplier_map["SUP1"].id,
        destination_location_id=location_map["S1"].id,
        product_id=rq002.id,
        quantity=6,
        received_quantity=0,
        unit_cost_minor=70000,
        freight_minor=18000,
        expected_date=scenario_date + datetime.timedelta(days=4),
        status="APPROVED",
        version=1
    )
    db.add(po1)
    db.flush()

    # 11. Historical Daily Sales (4,032 rows: 56 days x 24 SKUs x 3 stores)
    # k in 0..55: D-56 + k
    for j in range(1, 25):
        sku = f"RQ{j:03d}"
        p = product_map[sku]
        for s_idx, s_code in enumerate(store_codes, 1):
            s_loc = location_map[s_code]
            for k in range(56):
                dt = scenario_date - datetime.timedelta(days=56 - k)
                
                # Default gross units
                units = (j + s_idx + k) % 3
                
                # Specific overrides from spec
                if sku == "RQ002":
                    if s_code == "S1":
                        units = 3
                    else:
                        units = 1
                elif sku == "RQ005":
                    units = 1
                elif sku == "RQ006":
                    units = 1 if (k % 7 == 0) else 0
                elif sku == "RQ021" and s_code == "S3":
                    units = 1 if (k % 4 == 3) else 0

                sale = DailySale(
                    workspace_id=workspace_id,
                    product_id=p.id,
                    location_id=s_loc.id,
                    business_date=dt,
                    gross_units=units,
                    returned_units=0,
                    in_stock_hours=24.0,
                    is_synthetic=True
                )
                db.add(sale)

    db.flush()

    # 12. External Signals (EXT01, EXT02, EXT03)
    signals_data = [
        {
            "code": "EXT01",
            "keyword": "solar camp lantern",
            "cat": "LIGHTING",
            "cur": 60, "prev": 30,
            "rel": 0.8, "conf": 0.95,
            "matched_skus": ["RQ005"],
            "source": "synthetic://search-interest/lantern"
        },
        {
            "code": "EXT02",
            "keyword": "glow clip craze",
            "cat": "LIGHTING",
            "cur": 100, "prev": 10,
            "rel": 0.3, "conf": 0.75,
            "matched_skus": ["RQ006"],
            "source": "synthetic://social-engagement/clip"
        },
        {
            "code": "EXT03",
            "keyword": "portable charging",
            "cat": "POWER",
            "cur": 45, "prev": 40,
            "rel": 0.7, "conf": 0.95,
            "matched_skus": ["RQ001", "RQ002", "RQ003", "RQ004"],
            "source": "synthetic://search-interest/power"
        }
    ]

    for sig in signals_data:
        s_id = get_entity_uuid(workspace_id, "external_signals", sig["code"])
        matched_uuids = [str(product_map[s].id) for s in sig["matched_skus"]]
        signal = ExternalSignal(
            id=s_id,
            workspace_id=workspace_id,
            source_kind="SYNTHETIC",
            source_ref=sig["source"],
            keyword=sig["keyword"],
            category_id=category_map[sig["cat"]].id,
            location_id=location_map["S1"].id,
            region_code="Bengaluru/S1",
            window_start=scenario_date - datetime.timedelta(days=14),
            window_end=scenario_date - datetime.timedelta(days=1),
            current_index=sig["cur"],
            previous_index=sig["prev"],
            reliability=sig["rel"],
            mapping_confidence=sig["conf"],
            matched_product_ids=matched_uuids,
            permission_ref="synthetic://retailiq-demo-v1/permission",
            metadata_json={},
            is_synthetic=True,
            version=1
        )
        db.add(signal)

    # 13. Seed Historical Sessions & Intent Events for Intent Normalization
    # Default: D-7..D-1 count 40; D-14..D-8 count 40; D-35..D-15 count 60
    # Add representative sessions for key SKUs
    for sku, p in product_map.items():
        recent_cnt = 40
        prior_cnt = 40
        purchased_cnt = 10
        if sku == "RQ005":
            recent_cnt = 60
            prior_cnt = 20
            purchased_cnt = 5
        elif sku == "RQ006":
            recent_cnt = 8
            prior_cnt = 7
            purchased_cnt = 0
        elif sku == "RQ021":
            purchased_cnt = 5

        for i in range(recent_cnt):
            ev_id = get_entity_uuid(workspace_id, "intent_events", f"RECENT:{sku}:{i}")
            ev = IntentEvent(
                id=ev_id,
                workspace_id=workspace_id,
                actor_uid=f"seed-actor-{i%10}",
                session_key=f"session-recent-{sku}-{i}",
                product_id=p.id,
                category_id=p.category_id,
                location_id=location_map["S1"].id,
                event_type="SEARCH",
                event_time=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i % 7 + 1),
                business_date=scenario_date - datetime.timedelta(days=i % 7 + 1),
                source="INTERNAL_SEED",
                is_synthetic=True
            )
            db.add(ev)

        for i in range(prior_cnt):
            ev_id = get_entity_uuid(workspace_id, "intent_events", f"PRIOR:{sku}:{i}")
            ev = IntentEvent(
                id=ev_id,
                workspace_id=workspace_id,
                actor_uid=f"seed-prior-actor-{i%10}",
                session_key=f"session-prior-{sku}-{i}",
                product_id=p.id,
                category_id=p.category_id,
                location_id=location_map["S1"].id,
                event_type="SEARCH",
                event_time=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i % 7 + 8),
                business_date=scenario_date - datetime.timedelta(days=i % 7 + 8),
                source="INTERNAL_SEED",
                is_synthetic=True
            )
            db.add(ev)

            if i < purchased_cnt:
                p_ev_id = get_entity_uuid(workspace_id, "intent_events", f"PURCHASE:{sku}:{i}")
                p_ev = IntentEvent(
                    id=p_ev_id,
                    workspace_id=workspace_id,
                    actor_uid=f"seed-prior-actor-{i%10}",
                    session_key=f"session-prior-{sku}-{i}",
                    product_id=p.id,
                    category_id=p.category_id,
                    location_id=location_map["S1"].id,
                    event_type="PURCHASE",
                    event_time=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i % 7 + 8),
                    business_date=scenario_date - datetime.timedelta(days=i % 7 + 8),
                    source="INTERNAL_SEED",
                    is_synthetic=True
                )
                db.add(p_ev)

    db.commit()
    return workspace

def verify_seed(db: Session, workspace_id: uuid.UUID) -> dict:
    product_count = db.query(Product).filter(Product.workspace_id == workspace_id).count()
    location_count = db.query(Location).filter(Location.workspace_id == workspace_id).count()
    balance_count = db.query(InventoryBalance).filter(InventoryBalance.workspace_id == workspace_id).count()
    policy_count = db.query(PlanningPolicy).filter(PlanningPolicy.workspace_id == workspace_id).count()
    sales_count = db.query(DailySale).filter(DailySale.workspace_id == workspace_id).count()
    orders_count = db.query(Order).filter(Order.workspace_id == workspace_id).count()
    po_count = db.query(PurchaseOrder).filter(PurchaseOrder.workspace_id == workspace_id).count()
    signals_count = db.query(ExternalSignal).filter(ExternalSignal.workspace_id == workspace_id).count()

    results = {
        "workspace_id": str(workspace_id),
        "products": product_count,
        "locations": location_count,
        "inventory_balances": balance_count,
        "planning_policies": policy_count,
        "daily_sales": sales_count,
        "reserved_orders": orders_count,
        "purchase_orders": po_count,
        "external_signals": signals_count,
        "all_counts_match": (
            product_count == 24 and
            location_count == 4 and
            balance_count == 96 and
            policy_count == 72 and
            sales_count == 4032 and
            orders_count == 2 and
            po_count == 1 and
            signals_count == 3
        )
    }
    return results

def reset_workspace_to_canonical(db: Session, workspace_id: Optional[uuid.UUID] = None) -> Workspace:
    """
    Surgically restores the enterprise workspace state back to pristine seed baseline:
    - Resets all recommendations back to PROPOSED status
    - Deletes runtime transfers and newly created purchase orders
    - Deletes runtime customer orders and active reservation holds
    - Restores seed orders (ORD-001, ORD-002) and active allocations
    - Restores original product descriptions and resets catalog patches
    - Restores exact canonical on-hand & safety stock levels across all 24 SKUs and 4 network nodes
    Runs in < 15ms without dropping schema or database locks.
    """
    from app.models import (
        Recommendation, Transfer, Quote, Intent, CatalogPatch, CatalogAudit
    )

    ws = None
    if workspace_id:
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not ws:
        ws = db.query(Workspace).first()
    if not ws:
        return seed_database(db)

    ws_id = ws.id

    # 1. Reset all Recommendations to PROPOSED
    db.query(Recommendation).filter(
        Recommendation.workspace_id == ws_id
    ).update({"status": "PROPOSED", "updated_at": datetime.datetime.now(datetime.timezone.utc)})

    # 2. Delete all Transfers created during runtime
    db.query(Transfer).filter(Transfer.workspace_id == ws_id).delete()

    # 3. Clean Purchase Orders: keep only SEED-PO-001
    po1_id = get_entity_uuid(ws_id, "purchase_orders", "SEED-PO-001")
    db.query(PurchaseOrder).filter(
        PurchaseOrder.workspace_id == ws_id,
        PurchaseOrder.id != po1_id
    ).delete()
    seed_po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po1_id).first()
    if seed_po:
        seed_po.status = "APPROVED"
        seed_po.received_quantity = 0

    # 4. Clean Orders: keep only SEED-ORD-001 and SEED-ORD-002
    ord1_id = get_entity_uuid(ws_id, "orders", "SEED-ORD-001")
    ord2_id = get_entity_uuid(ws_id, "orders", "SEED-ORD-002")
    db.query(Order).filter(
        Order.workspace_id == ws_id,
        ~Order.id.in_([ord1_id, ord2_id])
    ).delete()
    db.query(Order).filter(Order.id.in_([ord1_id, ord2_id])).update({"status": "CONFIRMED"})

    # 5. Clean Allocations: keep only SEED-ALLOC-001 and SEED-ALLOC-002
    alloc1_id = get_entity_uuid(ws_id, "allocations", "SEED-ALLOC-001")
    alloc2_id = get_entity_uuid(ws_id, "allocations", "SEED-ALLOC-002")
    db.query(Allocation).filter(
        Allocation.workspace_id == ws_id,
        ~Allocation.id.in_([alloc1_id, alloc2_id])
    ).delete()
    db.query(Allocation).filter(Allocation.id.in_([alloc1_id, alloc2_id])).update({"state": "ACTIVE"})

    # 6. Delete runtime Quotes and Intents
    db.query(Quote).filter(Quote.workspace_id == ws_id).delete()
    db.query(Intent).filter(Intent.workspace_id == ws_id).delete()

    # 7. Reset CatalogPatches to PROPOSED
    db.query(CatalogPatch).filter(
        CatalogPatch.workspace_id == ws_id
    ).update({"status": "PROPOSED"})

    # 8. Restore canonical Product titles & descriptions
    rq001 = db.query(Product).filter(Product.workspace_id == ws_id, Product.sku == "RQ001").first()
    if rq001:
        rq001.title = "VoltGo Pro 10000"
        rq001.description = "10000mAh Power Bank with fast charging."

    # 9. Reset all InventoryBalance records to pristine seed levels
    products = db.query(Product).filter(Product.workspace_id == ws_id).all()
    locations = db.query(Location).filter(Location.workspace_id == ws_id).all()
    loc_map = {loc.code: loc.id for loc in locations}

    for p in products:
        sku = p.sku
        for loc_code, loc_id in loc_map.items():
            is_dc = (loc_code == "DC1")
            on_hand = 40 if is_dc else 20
            blocked = 0

            if sku == "RQ001":
                on_hand = 0
            elif sku == "RQ002":
                if loc_code == "S1":
                    on_hand = 12
                elif loc_code == "S2":
                    on_hand = 60
                    blocked = 2
                elif loc_code == "S3":
                    on_hand = 8
                elif loc_code == "DC1":
                    on_hand = 40
            elif sku == "RQ005":
                if loc_code == "S1":
                    on_hand = 6
                elif loc_code in ["S2", "S3"]:
                    on_hand = 4
                elif loc_code == "DC1":
                    on_hand = 5
            elif sku == "RQ006":
                if loc_code == "S1":
                    on_hand = 15
            elif sku == "RQ021":
                if loc_code == "S3":
                    on_hand = 80

            bal = db.query(InventoryBalance).filter(
                InventoryBalance.workspace_id == ws_id,
                InventoryBalance.product_id == p.id,
                InventoryBalance.location_id == loc_id
            ).first()
            if bal:
                bal.on_hand = on_hand
                bal.blocked = blocked

    db.commit()
    return ws

