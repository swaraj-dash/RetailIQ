import datetime
import uuid
from typing import Generic, TypeVar, Optional, Any, Union
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")

class MetaInfo(BaseModel):
    request_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    server_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_synthetic: bool = True

class Envelope(BaseModel, Generic[T]):
    data: T
    meta: MetaInfo = Field(default_factory=MetaInfo)

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    retryable: bool = False

class ErrorEnvelope(BaseModel):
    error: ErrorDetail
    meta: MetaInfo = Field(default_factory=MetaInfo)

class Page(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: Optional[str] = None

# Core Domain Schemas
class SessionSchema(BaseModel):
    workspace_id: uuid.UUID
    role: str = "DEMO_MANAGER"
    scenario_date: datetime.date
    dataset_version: str = "retailiq-demo-v1"
    expires_at: Optional[datetime.datetime] = None
    workspace_name: str = "RetailIQ Demo Retailer"

class FactSchema(BaseModel):
    id: uuid.UUID
    attribute: str
    value: Union[str, int, float, bool, list[str]]
    unit: Optional[str] = None
    source_ref: str

class ProductSchema(BaseModel):
    id: uuid.UUID
    sku: str
    title: str
    description: str
    brand: str
    category_code: str
    variant_label: str
    price_minor: int
    currency: str = "INR"
    image_path: Optional[str] = None
    facts: list[FactSchema] = Field(default_factory=list)
    published_availability: str # IN_STOCK, OUT_OF_STOCK
    version: int = 1

class LocationSchema(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    kind: str # STORE, DC
    locality_code: str
    pickup_enabled: bool
    ship_enabled: bool

class StockSchema(BaseModel):
    product_id: uuid.UUID
    location_id: uuid.UUID
    on_hand: int
    blocked: int
    active_hold: int
    active_order: int
    active_transfer: int
    inventory_version: int
    atp: int
    incoming_confirmed: int
    as_of: datetime.datetime

class AttributeConstraint(BaseModel):
    attribute: str
    operator: str # EQ, GTE, LTE, CONTAINS
    value: Union[str, int, float, bool]

class ConstraintsSchema(BaseModel):
    category_code: Optional[str] = None
    budget_minor: Optional[int] = None
    preferred_sku: Optional[str] = None
    destination_code: str = "INDIRANAGAR"
    preferred_store_code: Optional[str] = "S1"
    mode: str = "ANY" # ANY, PICKUP, SHIP
    needed_within_days: Optional[int] = None
    required_attributes: list[AttributeConstraint] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)

class ReasonSchema(BaseModel):
    code: str # WITHIN_BUDGET, FACT_MATCH, AVAILABLE, SUBSTITUTE, TRADEOFF
    fact_ids: list[uuid.UUID] = Field(default_factory=list)
    text: str

class CandidateSchema(BaseModel):
    product: ProductSchema
    stock: list[StockSchema] = Field(default_factory=list)
    match_score: float
    reasons: list[ReasonSchema] = Field(default_factory=list)
    is_substitute: bool = False

class IntentResultSchema(BaseModel):
    intent_id: uuid.UUID
    trace_id: uuid.UUID
    constraints: ConstraintsSchema
    status: str # NEEDS_INFO, MATCHED, NO_MATCH
    question: Optional[str] = None
    candidates: list[CandidateSchema] = Field(default_factory=list)
    ai_mode: str = "FALLBACK" # LIVE, FALLBACK
    warnings: list[str] = Field(default_factory=list)
    confidence: float = 0.95
    structured_query: Optional[dict[str, Any]] = None
    matched_skus: list[str] = Field(default_factory=list)
    explanation: str = ""
    requested_attributes: dict[str, Any] = Field(default_factory=dict)
    preferred_sku: Optional[str] = None

class QuoteOptionSchema(BaseModel):
    id: uuid.UUID
    origin_location_id: uuid.UUID
    origin_location_code: str
    origin_location_name: str
    mode: str # PICKUP, SHIP
    quantity: int
    unit_price_minor: int
    customer_fee_minor: int
    fulfillment_cost_minor: int
    total_minor: int
    lead_days: int
    promise_kind: str = "SIMULATED_ESTIMATE"
    inventory_version: int
    recommendation_reason: str

class QuoteSchema(BaseModel):
    id: uuid.UUID
    quote_id: Optional[uuid.UUID] = None
    product_id: uuid.UUID
    sku: Optional[str] = None
    product_name: Optional[str] = None
    location_code: Optional[str] = None
    location_name: Optional[str] = None
    fulfillment_type: Optional[str] = "PICKUP"
    unit_price: Optional[int] = None
    fulfillment_fee: Optional[int] = 0
    total_amount: Optional[int] = None
    currency: str = "INR"
    atp_available: int = 1
    can_fulfill: bool = True
    quantity: int
    options: list[QuoteOptionSchema] = Field(default_factory=list)
    expires_at: datetime.datetime
    valid_until_utc: Optional[str] = None
    unavailable_reasons: list[str] = Field(default_factory=list)

class HoldSchema(BaseModel):
    id: uuid.UUID
    hold_id: Optional[uuid.UUID] = None
    product_id: uuid.UUID
    sku: Optional[str] = None
    location_id: uuid.UUID
    location_code: Optional[str] = None
    quantity: int
    state: str # ACTIVE, CONSUMED, RELEASED, EXPIRED
    status: Optional[str] = None
    expires_at: datetime.datetime
    expires_at_utc: Optional[str] = None
    quote_id: Optional[uuid.UUID] = None
    quote_option_id: Optional[uuid.UUID] = None
    version: int = 1

class OrderSchema(BaseModel):
    id: uuid.UUID
    order_id: Optional[uuid.UUID] = None
    code: str
    order_code: Optional[str] = None
    intent_id: Optional[uuid.UUID] = None
    product_id: uuid.UUID
    product_title: Optional[str] = None
    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    sku: Optional[str] = None
    quantity: int
    origin_location_id: uuid.UUID
    origin_location_name: Optional[str] = None
    demand_location_id: uuid.UUID
    demand_location_name: Optional[str] = None
    destination_code: str
    location_code: Optional[str] = None
    mode: str # PICKUP, SHIP
    fulfillment_type: Optional[str] = "PICKUP"
    unit_price_minor: int
    unit_price: Optional[int] = None
    customer_fee_minor: int
    fulfillment_fee: Optional[int] = 0
    total_minor: int
    total_amount: Optional[int] = None
    currency: str = "INR"
    status: str # CONFIRMED, FULFILLED, SHIPPED, DELIVERED, CANCELLED
    version: int = 1
    created_at: Optional[datetime.datetime] = None
    created_at_utc: Optional[str] = None
    movement_id: Optional[str] = None
    allocation_id: Optional[Union[uuid.UUID, str]] = None
    stock_before: Optional[dict[str, Any]] = None
    stock_after: Optional[dict[str, Any]] = None
    message: Optional[str] = None

class TransferSchema(BaseModel):
    id: uuid.UUID
    transfer_id: Optional[uuid.UUID] = None
    transfer_code: Optional[str] = None
    product_id: uuid.UUID
    product_sku: Optional[str] = None
    sku: Optional[str] = None
    product_title: Optional[str] = None
    product_name: Optional[str] = None
    source_location_id: uuid.UUID
    source_location_code: Optional[str] = None
    origin_code: Optional[str] = None
    source_location_name: Optional[str] = None
    origin_name: Optional[str] = None
    destination_location_id: uuid.UUID
    destination_location_code: Optional[str] = None
    destination_code: Optional[str] = None
    destination_location_name: Optional[str] = None
    destination_name: Optional[str] = None
    quantity: int
    received_quantity: int = 0
    cost_minor: int
    expected_date: datetime.date
    eta_hours: int = 24
    status: str # APPROVED, IN_TRANSIT, RECEIVED, CANCELLED
    version: int = 1
    created_at_utc: Optional[str] = None
    movement_id: Optional[str] = None
    stock_before: Optional[dict[str, Any]] = None
    stock_after: Optional[dict[str, Any]] = None
    origin_stock_before: Optional[dict[str, Any]] = None
    origin_stock_after: Optional[dict[str, Any]] = None
    destination_stock_before: Optional[dict[str, Any]] = None
    destination_stock_after: Optional[dict[str, Any]] = None
    message: Optional[str] = None

class PurchaseOrderSchema(BaseModel):
    id: uuid.UUID
    po_id: Optional[uuid.UUID] = None
    po_code: Optional[str] = None
    product_id: uuid.UUID
    product_sku: Optional[str] = None
    sku: Optional[str] = None
    product_title: Optional[str] = None
    product_name: Optional[str] = None
    supplier_id: uuid.UUID
    supplier_name: Optional[str] = None
    destination_location_id: uuid.UUID
    destination_location_code: Optional[str] = None
    location_code: Optional[str] = None
    quantity: int
    received_quantity: int = 0
    unit_cost_minor: int
    unit_cost: Optional[int] = None
    freight_minor: int
    total_cost: Optional[int] = None
    expected_date: datetime.date
    status: str # APPROVED, RECEIVED, CANCELLED
    version: int = 1
    created_at_utc: Optional[str] = None
    movement_id: Optional[str] = None
    stock_before: Optional[dict[str, Any]] = None
    stock_after: Optional[dict[str, Any]] = None
    destination_stock_before: Optional[dict[str, Any]] = None
    destination_stock_after: Optional[dict[str, Any]] = None
    message: Optional[str] = None

class ReturnSchema(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    product_id: uuid.UUID
    location_id: uuid.UUID
    quantity: int
    refund_minor: int
    status: str # REQUESTED, RECEIVED, RESTOCKED, DAMAGED
    reason: str
    version: int = 1

# Intelligence and Analytics Schemas
class EvidenceSchema(BaseModel):
    source_id: Optional[uuid.UUID] = None
    source_ref: str
    source_kind: str
    is_synthetic: bool = True
    period_start: datetime.date
    period_end: datetime.date
    reliability: float
    summary: str

class ForecastPointSchema(BaseModel):
    date: datetime.date
    mean_units: float
    lower_units: float
    upper_units: float

class ForecastSchema(BaseModel):
    run_id: uuid.UUID
    product_id: uuid.UUID
    location_id: uuid.UUID
    as_of_date: datetime.date
    model: str # MA28, SNAIVE7, COLD
    points: list[ForecastPointSchema]
    wape: Optional[float] = None
    baseline_wape: Optional[float] = None
    mae: Optional[float] = None
    confidence: str = "HIGH" # LOW, MEDIUM, HIGH
    band_label: str = "Scenario range, not calibrated probability"
    evidence: list[EvidenceSchema] = Field(default_factory=list)
    sku: Optional[str] = "RQ002"
    location_code: Optional[str] = "S1"
    horizon_days: int = 14
    backtest_metrics: Optional[dict[str, Any]] = None
    daily_forecast: list[dict[str, Any]] = Field(default_factory=list)

class AlternativeSchema(BaseModel):
    action: str # TRANSFER, PURCHASE, TEST_ORDER, MONITOR, NO_ACTION
    source_location_id: Optional[uuid.UUID] = None
    source_location_code: Optional[str] = None
    supplier_id: Optional[uuid.UUID] = None
    supplier_name: Optional[str] = None
    quantity: int
    arrival_day: Optional[int] = None
    feasible: bool = True
    rejection_reasons: list[str] = Field(default_factory=list)
    lost_units: float
    recovered_units: float
    action_cost_minor: int
    holding_cost_minor: int
    unsold_risk_minor: int
    working_capital_minor: int
    margin_opportunity_minor: int

class DecisionSchema(BaseModel):
    horizon_days: int = 14
    atp: int
    incoming: list[dict[str, Any]] = Field(default_factory=list)
    forecast_units: float
    safety_units: float
    stockout_days: Optional[int] = None
    excess_units: float = 0.0
    historical_summary: str
    evidence: list[EvidenceSchema] = Field(default_factory=list)
    alternatives: list[AlternativeSchema] = Field(default_factory=list)
    expected_upside_minor: int
    downside_risk_minor: int
    working_capital_minor: int
    margin_opportunity_minor: int
    confidence: str = "HIGH"
    confidence_score: float = 0.85
    assumptions: list[str] = Field(default_factory=list)
    explanation: str
    algorithm_version: str = "retailiq-v1"
    source_event_ids: list[uuid.UUID] = Field(default_factory=list)

class RecommendationSchema(BaseModel):
    id: uuid.UUID
    run_id: uuid.UUID
    product_id: uuid.UUID
    product_sku: Optional[str] = None
    product_title: Optional[str] = None
    location_id: uuid.UUID
    location_code: Optional[str] = None
    intent_id: Optional[uuid.UUID] = None
    action: str # TRANSFER, PURCHASE, TEST_ORDER, MONITOR, NO_ACTION
    quantity: int
    source_location_id: Optional[uuid.UUID] = None
    source_location_code: Optional[str] = None
    supplier_id: Optional[uuid.UUID] = None
    priority_score: float = 0.0
    status: str = "PROPOSED" # PROPOSED, APPROVED, REJECTED, STALE, EXECUTED
    decision: DecisionSchema
    expires_at: datetime.datetime
    version: int = 1

class AuditIssueSchema(BaseModel):
    rule_id: str
    severity: str # HIGH, MEDIUM, LOW
    field: str
    message: str
    fact_ids: list[uuid.UUID] = Field(default_factory=list)
    weight: int

class CatalogAuditSchema(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_sku: Optional[str] = None
    product_title: Optional[str] = None
    product_version: int
    score_before: float
    issues: list[AuditIssueSchema] = Field(default_factory=list)

class CatalogPatchChange(BaseModel):
    field: str # title, description
    before: str
    after: str

class CatalogPatchSchema(BaseModel):
    id: uuid.UUID
    audit_id: uuid.UUID
    product_id: uuid.UUID
    product_sku: Optional[str] = None
    base_product_version: int
    changes: list[CatalogPatchChange] = Field(default_factory=list)
    fact_refs: list[uuid.UUID] = Field(default_factory=list)
    status: str = "PROPOSED" # PROPOSED, APPROVED, REJECTED, STALE
    ai_mode: str = "FALLBACK"
    version: int = 1

class DashboardDataSchema(BaseModel):
    run_id: Optional[uuid.UUID] = None
    as_of_date: datetime.date
    stale: bool = False
    stockout_sku_locations: int = 0
    excess_units: int = 0
    excess_value_minor: int = 0
    estimated_margin_opportunity_minor: int = 0
    pending_proposals: int = 0
    catalog_score: Optional[float] = None
    observed_orders: int = 0
    observed_contribution_minor: int = 0
    segment_label: str = "Autonomous Retail Intelligence"
    kpi_cards: Optional[dict[str, Any]] = None
    top_recommendations: list[dict[str, Any]] = Field(default_factory=list)
    scenario_date: Optional[str] = None
    last_refreshed_at_utc: Optional[str] = None

class TrendItemSchema(BaseModel):
    signal_id: uuid.UUID
    category_code: str
    region_code: str
    current_index: float
    previous_index: float
    reliability: float
    is_synthetic: bool = True
    internal_sessions_current: int
    internal_sessions_previous: int
    decision: str # ACT, MONITOR, NO_ACTION
    reason: str
    recommendation_ids: list[uuid.UUID] = Field(default_factory=list)

class OutcomeItemSchema(BaseModel):
    id: uuid.UUID
    intent_id: Optional[uuid.UUID] = None
    order_id: Optional[uuid.UUID] = None
    recommendation_id: Optional[uuid.UUID] = None
    event_type: str
    observed_units: int
    observed_contribution_minor: int
    observed_at: datetime.datetime
    is_synthetic: bool = True
    reference_id: uuid.UUID

class TraceNode(BaseModel):
    type: str # INTENT, QUOTE, ORDER, EVENT, RECOMMENDATION, OUTCOME
    id: uuid.UUID
    label: str
    time: datetime.datetime

class TraceEdge(BaseModel):
    from_id: uuid.UUID
    to_id: uuid.UUID
    relation: str

class TraceGraphSchema(BaseModel):
    intent_id: uuid.UUID
    trace_id: uuid.UUID
    nodes: list[TraceNode] = Field(default_factory=list)
    edges: list[TraceEdge] = Field(default_factory=list)

# Request Payloads
class IntentRequest(BaseModel):
    text: Optional[str] = None
    query: Optional[str] = None
    destination_code: str = "INDIRANAGAR"
    preferred_store_code: Optional[str] = "S1"
    location_code: Optional[str] = None
    channel: Optional[str] = None
    previous_intent_id: Optional[uuid.UUID] = None

    def get_text(self) -> str:
        return (self.text or self.query or "").strip()

    def get_store_code(self) -> str:
        return self.preferred_store_code or self.location_code or "S1"

class ComparisonRequest(BaseModel):
    product_ids: Optional[list[uuid.UUID]] = None
    skus: Optional[list[str]] = None
    intent_id: Optional[uuid.UUID] = None
    min_wattage: Optional[int] = 20
    connector: Optional[str] = "USB-C"

class ComparisonRowSchema(BaseModel):
    attribute: str
    values: list[Any]
    fact_ids: Optional[list[Any]] = None

class CompatibilitySchema(BaseModel):
    sku: str
    is_compatible: bool
    confidence: float
    product_wattage: int
    required_wattage: int
    warning: Optional[str] = None
    explanation: Optional[str] = None
    ai_mode: str

class ComparisonResponseSchema(BaseModel):
    products: list[ProductSchema]
    rows: list[ComparisonRowSchema]
    tradeoffs: list[str]
    compatibility: CompatibilitySchema
    ai_mode: str

class QuoteRequest(BaseModel):
    product_id: Optional[uuid.UUID] = None
    sku: Optional[str] = None
    quantity: int = Field(default=1, ge=1, le=5)
    destination_code: str = "INDIRANAGAR"
    mode: str = "ANY"
    fulfillment_type: Optional[str] = None
    preferred_store_code: Optional[str] = "S1"
    location_code: Optional[str] = None
    needed_within_days: Optional[int] = None
    intent_id: Optional[uuid.UUID] = None

    def get_mode(self) -> str:
        return self.fulfillment_type or self.mode or "ANY"

    def get_store_code(self) -> str:
        return self.preferred_store_code or self.location_code or "S1"

class HoldRequest(BaseModel):
    quote_id: Optional[uuid.UUID] = None
    quote_option_id: Optional[uuid.UUID] = None
    sku: Optional[str] = None
    location_code: Optional[str] = None
    quantity: int = 1

class OrderCreateRequest(BaseModel):
    hold_id: uuid.UUID
    expected_version: int = 1
    shopper_name: Optional[str] = "Rahul Sharma"
    shopper_email: Optional[str] = None
    shipping_address: Optional[str] = None

class OrderTransitionRequest(BaseModel):
    action: Optional[str] = "FULFILL_PICKUP"
    expected_version: int = 1
    note: Optional[str] = None

class TransferTransitionRequest(BaseModel):
    action: Optional[str] = "DISPATCH"
    expected_version: int = 1
    note: Optional[str] = None

class POTransitionRequest(BaseModel):
    action: Optional[str] = "RECEIVE"
    expected_version: int = 1
    note: Optional[str] = None

class ReturnCreateRequest(BaseModel):
    order_id: uuid.UUID
    quantity: int = Field(default=1, ge=1, le=5)
    location_id: uuid.UUID
    reason: str = Field(min_length=1, max_length=120)

class ReturnTransitionRequest(BaseModel):
    action: str # RECEIVE, RESTOCK, DAMAGE
    expected_version: int = 1

class EventCreateRequest(BaseModel):
    intent_id: Optional[uuid.UUID] = None
    product_id: Optional[uuid.UUID] = None
    category_code: Optional[str] = None
    location_id: uuid.UUID
    event_type: str # VIEW, COMPARE, CART, CHECKOUT
    session_key: str = Field(min_length=1, max_length=64)

class PlanningRefreshRequest(BaseModel):
    as_of_date: datetime.date = datetime.date(2026, 10, 17)

class RecommendationReviewRequest(BaseModel):
    decision: str # APPROVE, REJECT
    expected_version: int = 1
    note: Optional[str] = Field(default="", max_length=300)

class CatalogAuditRequest(BaseModel):
    product_ids: Optional[list[uuid.UUID]] = None

class CatalogPatchRequest(BaseModel):
    audit_id: uuid.UUID

class CatalogPatchReviewRequest(BaseModel):
    decision: Optional[str] = "APPROVE" # APPROVE, REJECT
    expected_version: Optional[int] = 1
    expected_product_version: Optional[int] = None
