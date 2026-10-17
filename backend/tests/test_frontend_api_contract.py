import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.services.seed import seed_database

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

def test_frontend_full_browser_contract():
    # 1. Health check
    res = client.get("/health/ready")
    assert res.status_code == 200
    data = res.json()
    status_val = data.get("data", {}).get("status") if "data" in data else data.get("status")
    assert status_val == "ready"

    # 2. Catalog products
    res = client.get("/api/v1/catalog/products")
    assert res.status_code == 200
    prod_data = res.json()["data"]
    items = prod_data["items"] if isinstance(prod_data, dict) and "items" in prod_data else prod_data
    assert len(items) > 0

    # 3. Product stock summary for RQ002
    res = client.get("/api/v1/inventory/stock/RQ002")
    assert res.status_code == 200
    st_data = res.json()["data"]
    assert st_data["product"]["sku"] == "RQ002"
    assert "atp_total" in st_data
    assert len(st_data["locations"]) == 4

    # 4. Shopping Intent (The endpoint the user tested!)
    res = client.post("/api/v1/shopping/intent", json={
        "query": "10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today",
        "location_code": "S1"
    })
    assert res.status_code == 200, f"Failed: {res.text}"
    intent_data = res.json()["data"]
    assert "confidence" in intent_data
    assert intent_data["confidence"] >= 0.9
    assert "structured_query" in intent_data
    assert "matched_skus" in intent_data
    assert "explanation" in intent_data

    # 5. Shopping Quote
    res = client.post("/api/v1/shopping/quote", json={
        "sku": "RQ002",
        "location_code": "S1",
        "fulfillment_type": "PICKUP",
        "quantity": 1
    })
    assert res.status_code == 200
    q_data = res.json()["data"]
    assert q_data["product_name"] != ""
    assert q_data["unit_price"] > 0
    assert q_data["total_amount"] > 0
    assert q_data["quote_id"] is not None
    quote_id = q_data["quote_id"]

    # 6. Shopping Hold (15-min reservation)
    res = client.post("/api/v1/shopping/hold", json={
        "quote_id": quote_id,
        "sku": "RQ002",
        "location_code": "S1",
        "quantity": 1
    })
    assert res.status_code == 200
    h_data = res.json()["data"]
    assert h_data["hold_id"] is not None
    assert h_data["expires_at_utc"] != ""
    hold_id = h_data["hold_id"]

    # 7. Order from Hold
    res = client.post("/api/v1/orders/from-hold", json={
        "hold_id": hold_id,
        "shopper_name": "Rahul Sharma",
        "shopper_email": "rahul.sharma@example.com"
    })
    assert res.status_code == 200
    o_data = res.json()["data"]
    assert o_data["order_id"] is not None
    assert o_data["order_code"] != ""
    assert o_data["status"] in ["CREATED", "CONFIRMED"]
    order_id = o_data["order_id"]

    # 8. List Orders
    res = client.get("/api/v1/orders")
    assert res.status_code == 200
    orders_data = res.json()["data"]
    orders_list = orders_data["items"] if isinstance(orders_data, dict) and "items" in orders_data else orders_data
    assert any(o.get("order_id") == order_id or o.get("id") == order_id for o in orders_list)

    # 9. Fulfill Pickup Order
    res = client.post(f"/api/v1/orders/{order_id}/fulfill-pickup", json={
        "note": "Customer verified with photo ID"
    })
    assert res.status_code == 200
    f_data = res.json()["data"]
    assert f_data["status"] == "FULFILLED"
    assert f_data["movement_id"] is not None
    assert f_data["stock_before"]["on_hand"] == 12
    assert f_data["stock_after"]["on_hand"] == 11

    # 10. Planning Dashboard Summary
    res = client.get("/api/v1/planning/dashboard")
    assert res.status_code == 200
    dash_data = res.json()["data"]
    assert "kpi_cards" in dash_data
    assert dash_data["kpi_cards"]["stockout_pairs"] >= 1
    assert dash_data["kpi_cards"]["margin_opportunity"] > 0
    assert "top_recommendations" in dash_data
    assert len(dash_data["top_recommendations"]) > 0
    old_rec = dash_data["top_recommendations"][0]
    old_rec_id = old_rec["recommendation_id"]
    assert old_rec["action_type"] in ["TRANSFER", "PURCHASE"]
    assert old_rec["working_capital_required"] == 0

    # 11. Refresh Intelligence
    res = client.post("/api/v1/planning/refresh-intelligence")
    assert res.status_code == 200

    # 11b. Verify stale proposal rejection (409 PROPOSAL_STALE)
    stale_res = client.post(f"/api/v1/planning/proposals/{old_rec_id}/approve")
    assert stale_res.status_code == 409
    assert "PROPOSAL_STALE" in stale_res.text

    # 11c. Re-fetch dashboard after refresh to get active proposal
    res = client.get("/api/v1/planning/dashboard")
    assert res.status_code == 200
    fresh_dash_data = res.json()["data"]
    fresh_rec = fresh_dash_data["top_recommendations"][0]
    fresh_rec_id = fresh_rec["recommendation_id"]

    # 12. 14-Day Demand Forecast
    res = client.get("/api/v1/planning/forecast?sku=RQ002&location_code=S1&horizon_days=14")
    assert res.status_code == 200
    fc_data = res.json()["data"]
    assert "backtest_metrics" in fc_data
    assert fc_data["backtest_metrics"]["wape"] > 0
    assert len(fc_data["daily_forecast"]) == 14
    assert any(d["is_stockout"] for d in fc_data["daily_forecast"])

    # 13. Trends Analysis
    res = client.get("/api/v1/planning/trends")
    assert res.status_code == 200
    tr_data = res.json()["data"]
    assert "signals" in tr_data
    assert len(tr_data["signals"]) > 0

    # 14. Approve Proposal (creates Transfer in DB!)
    res = client.post(f"/api/v1/planning/proposals/{fresh_rec_id}/approve")
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "APPROVED"

    # 15. List Transfers (Associate Queue)
    res = client.get("/api/v1/transfers")
    assert res.status_code == 200
    trans_data = res.json()["data"]
    trans_list = trans_data["items"] if isinstance(trans_data, dict) and "items" in trans_data else trans_data
    assert len(trans_list) > 0
    target_tr = trans_list[0]
    target_tr_id = target_tr.get("transfer_id") or target_tr.get("id")

    # 16. Dispatch Transfer
    res = client.post(f"/api/v1/transfers/{target_tr_id}/dispatch", json={})
    assert res.status_code == 200
    disp_data = res.json()["data"]
    assert disp_data["status"] == "IN_TRANSIT"
    assert disp_data["movement_id"] is not None

    # 17. Receive Transfer
    res = client.post(f"/api/v1/transfers/{target_tr_id}/receive", json={})
    assert res.status_code == 200
    recv_data = res.json()["data"]
    assert recv_data["status"] == "RECEIVED"
    assert recv_data["movement_id"] is not None

    # 18. List Purchase Orders
    res = client.get("/api/v1/purchase-orders")
    assert res.status_code == 200
    pos_data = res.json()["data"]
    pos_list = pos_data["items"] if isinstance(pos_data, dict) and "items" in pos_data else pos_data
    assert len(pos_list) > 0
    target_po = pos_list[0]
    target_po_id = target_po.get("po_id") or target_po.get("id")

    # 19. Receive Purchase Order
    res = client.post(f"/api/v1/purchase-orders/{target_po_id}/receive", json={})
    assert res.status_code == 200
    po_recv = res.json()["data"]
    assert po_recv["status"] == "RECEIVED"
    assert po_recv["movement_id"] is not None

    # 20. Catalog Audit
    res = client.get("/api/v1/catalog-ops/audit")
    assert res.status_code == 200
    cat_data = res.json()["data"]
    assert cat_data["overall_score"] > 70
    assert len(cat_data["rules"]) > 0
    assert len(cat_data["pending_patches"]) > 0
    patch_id = cat_data["pending_patches"][0]["patch_id"]

    # 21. Approve Catalog Patch
    res = client.post(f"/api/v1/catalog-ops/patches/{patch_id}/approve")
    assert res.status_code == 200
    patch_res = res.json()["data"]
    assert patch_res["status"] == "APPROVED"

    # 22. Immutable Event & Trace Log
    res = client.get("/api/v1/events/trace?limit=50")
    assert res.status_code == 200
    trace_list = res.json()["data"]
    assert len(trace_list) > 0
    first_ev = trace_list[0]
    assert "id" in first_ev
    assert "timestamp" in first_ev
    assert "entity_type" in first_ev
