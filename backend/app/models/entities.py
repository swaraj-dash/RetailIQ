import datetime
import uuid
from sqlalchemy import (
    Column, String, Text, Integer, BigInteger, Boolean, Date, DateTime, Numeric, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base, GUID, JSONType

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

# 1. Global Workspaces Table
class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    owner_firebase_uid = Column(String(128), unique=True, nullable=True)
    name = Column(String(80), nullable=False, default="RetailIQ Demo Retailer")
    is_demo = Column(Boolean, nullable=False, default=True)
    scenario_date = Column(Date, nullable=False, default=lambda: datetime.date(2026, 10, 17))
    dataset_version = Column(String(30), nullable=False, default="retailiq-demo-v1")
    expires_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 2. Memberships Table
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    firebase_uid = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default="DEMO_MANAGER")
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 3. Locations Table
class Location(Base):
    __tablename__ = "locations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(12), nullable=False)
    name = Column(String(80), nullable=False)
    kind = Column(String(10), nullable=False) # STORE, DC
    locality_code = Column(String(20), nullable=False)
    timezone = Column(String(40), nullable=False, default="Asia/Kolkata")
    pickup_enabled = Column(Boolean, nullable=False, default=True)
    ship_enabled = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 4. Categories Table
class Category(Base):
    __tablename__ = "categories"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(30), nullable=False)
    name = Column(String(80), nullable=False)
    required_attributes = Column(JSONType, nullable=False, default=list)
    allowed_values = Column(JSONType, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 5. Products Table
class Product(Base):
    __tablename__ = "products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(GUID, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    sku = Column(String(20), nullable=False)
    title = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    brand = Column(String(80), nullable=False)
    variant_label = Column(String(80), nullable=False, default="Standard")
    gtin = Column(String(14), nullable=True)
    mpn = Column(String(80), nullable=True)
    image_path = Column(Text, nullable=True)
    price_minor = Column(BigInteger, nullable=False)
    unit_cost_minor = Column(BigInteger, nullable=False)
    currency = Column(String(3), nullable=False, default="INR")
    published_availability = Column(String(20), nullable=False, default="IN_STOCK")
    active = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    category = relationship("Category")
    facts = relationship("ProductFact", back_populates="product", cascade="all, delete-orphan")

# 6. Product Facts Table
class ProductFact(Base):
    __tablename__ = "product_facts"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    attribute = Column(String(60), nullable=False)
    value = Column(JSONType, nullable=False)
    unit = Column(String(20), nullable=True)
    source_ref = Column(String(200), nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product", back_populates="facts")

# 7. Suppliers Table
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(80), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 8. Supplier SKUs Table
class SupplierSku(Base):
    __tablename__ = "supplier_skus"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    supplier_id = Column(GUID, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    lead_days = Column(Integer, nullable=False, default=7)
    moq = Column(Integer, nullable=False, default=24)
    pack_size = Column(Integer, nullable=False, default=6)
    unit_cost_minor = Column(BigInteger, nullable=False)
    freight_minor = Column(BigInteger, nullable=False, default=18000)
    active = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    supplier = relationship("Supplier")
    product = relationship("Product")

# 9. Lanes Table
class Lane(Base):
    __tablename__ = "lanes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    origin_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    destination_code = Column(String(20), nullable=False)
    mode = Column(String(10), nullable=False) # TRANSFER, SHIP
    lead_days = Column(Integer, nullable=False, default=1)
    fixed_cost_minor = Column(BigInteger, nullable=False)
    unit_cost_minor = Column(BigInteger, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    origin_location = relationship("Location")

# 10. Planning Policies Table
class PlanningPolicy(Base):
    __tablename__ = "planning_policies"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    review_days = Column(Integer, nullable=False, default=7)
    safety_days = Column(Integer, nullable=False, default=2)
    excess_days = Column(Integer, nullable=False, default=56)
    annual_holding_rate = Column(Numeric(18, 6), nullable=False, default=0.20)
    unsold_risk_rate = Column(Numeric(18, 6), nullable=False, default=0.10)
    capital_limit_minor = Column(BigInteger, nullable=False, default=500000)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 11. Promotions Table
class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, nullable=True)
    category_id = Column(GUID, nullable=True)
    location_id = Column(GUID, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    multiplier = Column(Numeric(18, 6), nullable=False, default=1.20)
    source_ref = Column(Text, nullable=False)
    approved = Column(Boolean, nullable=False, default=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 12. Inventory Balances Table
class InventoryBalance(Base):
    __tablename__ = "inventory_balances"
    __table_args__ = (
        PrimaryKeyConstraint("workspace_id", "product_id", "location_id"),
    )

    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    on_hand = Column(Integer, nullable=False, default=0)
    blocked = Column(Integer, nullable=False, default=0)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    location = relationship("Location")

# 13. Allocations Table
class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    kind = Column(String(20), nullable=False) # HOLD, ORDER, TRANSFER
    state = Column(String(20), nullable=False) # ACTIVE, CONSUMED, RELEASED, EXPIRED
    expires_at = Column(DateTime(timezone=True), nullable=True)
    quote_id = Column(GUID, nullable=True)
    quote_option_id = Column(GUID, nullable=True)
    order_id = Column(GUID, nullable=True)
    transfer_id = Column(GUID, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 14. Intents Table
class Intent(Base):
    __tablename__ = "intents"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    trace_id = Column(GUID, nullable=False, default=uuid.uuid4)
    constraints = Column(JSONType, nullable=False, default=dict)
    preferred_product_id = Column(GUID, nullable=True)
    status = Column(String(20), nullable=False, default="MATCHED") # NEEDS_INFO, MATCHED, NO_MATCH
    ai_mode = Column(String(10), nullable=False, default="FALLBACK") # LIVE, FALLBACK
    prompt_version = Column(String(30), nullable=False, default="need-v1")
    model_id = Column(String(60), nullable=True)
    redacted_summary = Column(String(300), nullable=False, default="")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 15. Quotes Table
class Quote(Base):
    __tablename__ = "quotes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    intent_id = Column(GUID, nullable=True)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    destination_code = Column(String(20), nullable=False)
    options = Column(JSONType, nullable=False, default=list)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(10), nullable=False, default="OPEN") # OPEN, USED, EXPIRED
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 16. Orders Table
class Order(Base):
    __tablename__ = "orders"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(30), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    intent_id = Column(GUID, nullable=True)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    origin_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    demand_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    destination_code = Column(String(20), nullable=False)
    mode = Column(String(10), nullable=False) # PICKUP, SHIP
    unit_price_minor = Column(BigInteger, nullable=False)
    unit_cost_minor = Column(BigInteger, nullable=False)
    fulfillment_cost_minor = Column(BigInteger, nullable=False, default=0)
    customer_fee_minor = Column(BigInteger, nullable=False, default=0)
    total_minor = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="CONFIRMED") # CONFIRMED, FULFILLED, SHIPPED, DELIVERED, CANCELLED
    fulfilled_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    origin_location = relationship("Location", foreign_keys=[origin_location_id])
    demand_location = relationship("Location", foreign_keys=[demand_location_id])

# 17. Transfers Table
class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    source_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    destination_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    received_quantity = Column(Integer, nullable=False, default=0)
    cost_minor = Column(BigInteger, nullable=False)
    lead_days = Column(Integer, nullable=False, default=1)
    expected_date = Column(Date, nullable=False)
    recommendation_id = Column(GUID, nullable=True)
    status = Column(String(20), nullable=False, default="APPROVED") # APPROVED, IN_TRANSIT, RECEIVED, CANCELLED
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    source_location = relationship("Location", foreign_keys=[source_location_id])
    destination_location = relationship("Location", foreign_keys=[destination_location_id])

# 18. Purchase Orders Table
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    supplier_id = Column(GUID, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    destination_location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    received_quantity = Column(Integer, nullable=False, default=0)
    unit_cost_minor = Column(BigInteger, nullable=False)
    freight_minor = Column(BigInteger, nullable=False)
    expected_date = Column(Date, nullable=False)
    recommendation_id = Column(GUID, nullable=True)
    status = Column(String(20), nullable=False, default="APPROVED") # APPROVED, RECEIVED, CANCELLED
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    supplier = relationship("Supplier")
    destination_location = relationship("Location")
    product = relationship("Product")

# 19. Returns Table
class Return(Base):
    __tablename__ = "returns"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(GUID, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    refund_minor = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="REQUESTED") # REQUESTED, RECEIVED, RESTOCKED, DAMAGED
    reason = Column(String(120), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    location = relationship("Location")
    order = relationship("Order")

# 20. Stock Movements Table (immutable)
class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    delta_on_hand = Column(Integer, nullable=False)
    delta_blocked = Column(Integer, nullable=False, default=0)
    reason = Column(String(30), nullable=False)
    reference_type = Column(String(30), nullable=False)
    reference_id = Column(GUID, nullable=False)
    operation_key = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 21. Daily Sales Table
class DailySale(Base):
    __tablename__ = "daily_sales"
    __table_args__ = (
        PrimaryKeyConstraint("workspace_id", "product_id", "location_id", "business_date"),
    )

    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    business_date = Column(Date, nullable=False)
    gross_units = Column(Integer, nullable=False, default=0)
    returned_units = Column(Integer, nullable=False, default=0)
    in_stock_hours = Column(Numeric(6, 2), nullable=False, default=24.0)
    is_synthetic = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 22. Intent Events Table (immutable)
class IntentEvent(Base):
    __tablename__ = "intent_events"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    actor_uid = Column(String(128), nullable=True)
    session_key = Column(String(128), nullable=False)
    intent_id = Column(GUID, nullable=True)
    product_id = Column(GUID, nullable=True)
    category_id = Column(GUID, nullable=True)
    location_id = Column(GUID, nullable=True)
    event_type = Column(String(20), nullable=False)
    event_time = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    business_date = Column(Date, nullable=False)
    source = Column(String(20), nullable=False, default="INTERNAL_SEED") # INTERNAL_SEED, APP
    reference_id = Column(GUID, nullable=True)
    is_synthetic = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 23. External Signals Table
class ExternalSignal(Base):
    __tablename__ = "external_signals"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    source_kind = Column(String(20), nullable=False, default="SYNTHETIC")
    source_ref = Column(Text, nullable=False)
    keyword = Column(String(120), nullable=False)
    category_id = Column(GUID, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, nullable=True)
    region_code = Column(String(30), nullable=False)
    window_start = Column(Date, nullable=False)
    window_end = Column(Date, nullable=False)
    current_index = Column(Numeric(10, 2), nullable=False)
    previous_index = Column(Numeric(10, 2), nullable=False)
    reliability = Column(Numeric(6, 4), nullable=False)
    mapping_confidence = Column(Numeric(6, 4), nullable=False)
    matched_product_ids = Column(JSONType, nullable=False, default=list)
    permission_ref = Column(Text, nullable=False)
    metadata_json = Column(JSONType, nullable=False, default=dict)
    is_synthetic = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

# 24. Forecast Runs Table (immutable)
class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    as_of_date = Column(Date, nullable=False)
    horizon_days = Column(Integer, nullable=False, default=28)
    status = Column(String(20), nullable=False, default="COMPLETED")
    dataset_version = Column(String(30), nullable=False, default="retailiq-demo-v1")
    input_hash = Column(String(64), nullable=False)
    algorithm_version = Column(String(30), nullable=False, default="retailiq-v1")
    inventory_snapshot = Column(JSONType, nullable=False, default=dict)
    source_event_ids = Column(JSONType, nullable=False, default=list)
    completed_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 25. Forecasts Table (immutable)
class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(GUID, ForeignKey("forecast_runs.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    forecast_date = Column(Date, nullable=False)
    mean_units = Column(Numeric(18, 6), nullable=False)
    lower_units = Column(Numeric(18, 6), nullable=False)
    upper_units = Column(Numeric(18, 6), nullable=False)
    baseline_wape = Column(Numeric(18, 6), nullable=True)
    model_mae = Column(Numeric(18, 6), nullable=True)
    model = Column(String(20), nullable=False, default="MA28")
    evidence = Column(JSONType, nullable=False, default=list)
    confidence = Column(String(10), nullable=False, default="HIGH")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 26. Recommendations Table
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(GUID, ForeignKey("forecast_runs.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(GUID, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    intent_id = Column(GUID, nullable=True)
    action = Column(String(20), nullable=False) # TRANSFER, PURCHASE, TEST_ORDER, MONITOR, NO_ACTION
    quantity = Column(Integer, nullable=False, default=0)
    source_location_id = Column(GUID, nullable=True)
    supplier_id = Column(GUID, nullable=True)
    horizon_days = Column(Integer, nullable=False, default=14)
    priority_score = Column(Numeric(18, 6), nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="PROPOSED") # PROPOSED, APPROVED, REJECTED, STALE, EXECUTED
    decision = Column(JSONType, nullable=False, default=dict)
    input_hash = Column(String(64), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    location = relationship("Location", foreign_keys=[location_id])

# 27. Catalog Audits Table (immutable)
class CatalogAudit(Base):
    __tablename__ = "catalog_audits"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(GUID, nullable=True)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product_version = Column(Integer, nullable=False, default=1)
    score_before = Column(Numeric(6, 2), nullable=False)
    issues = Column(JSONType, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    product = relationship("Product")

# 28. Catalog Patches Table
class CatalogPatch(Base):
    __tablename__ = "catalog_patches"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    audit_id = Column(GUID, ForeignKey("catalog_audits.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(GUID, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    base_product_version = Column(Integer, nullable=False, default=1)
    changes = Column(JSONType, nullable=False, default=list)
    fact_refs = Column(JSONType, nullable=False, default=list)
    status = Column(String(20), nullable=False, default="PROPOSED") # PROPOSED, APPROVED, REJECTED, STALE
    ai_mode = Column(String(10), nullable=False, default="FALLBACK") # LIVE, FALLBACK
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    product = relationship("Product")
    audit = relationship("CatalogAudit")

# 29. Outcomes Table (immutable)
class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    intent_id = Column(GUID, nullable=True)
    order_id = Column(GUID, nullable=True)
    recommendation_id = Column(GUID, nullable=True)
    event_type = Column(String(30), nullable=False)
    observed_units = Column(Integer, nullable=False, default=0)
    observed_contribution_minor = Column(BigInteger, nullable=False, default=0)
    observed_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    is_synthetic = Column(Boolean, nullable=False, default=True)
    reference_id = Column(GUID, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 30. Audit Events Table
class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(GUID, nullable=False)
    before_hash = Column(String(64), nullable=True)
    after_hash = Column(String(64), nullable=False)
    request_id = Column(GUID, nullable=False)
    trace_id = Column(GUID, nullable=False)
    details = Column(JSONType, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 31. Idempotency Records Table
class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"
    __table_args__ = (
        PrimaryKeyConstraint("scope_key", "actor_uid", "key"),
    )

    scope_key = Column(String(200), nullable=False)
    actor_uid = Column(String(128), nullable=False)
    key = Column(String(128), nullable=False)
    workspace_id = Column(GUID, nullable=True)
    method = Column(String(8), nullable=False)
    path = Column(Text, nullable=False)
    body_hash = Column(String(64), nullable=False)
    response_code = Column(Integer, nullable=False)
    response_body = Column(JSONType, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

# 32. Usage Buckets Table
class UsageBucket(Base):
    __tablename__ = "usage_buckets"
    __table_args__ = (
        PrimaryKeyConstraint("scope_key", "bucket_start", "kind"),
    )

    scope_key = Column(String(160), nullable=False)
    bucket_start = Column(DateTime(timezone=True), nullable=False)
    kind = Column(String(30), nullable=False)
    count = Column(Integer, nullable=False, default=0)
