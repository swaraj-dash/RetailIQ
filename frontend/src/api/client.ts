/**
 * RetailIQ API Client
 * Typed contracts matching FastAPI schemas in backend/app/schemas/contracts.py
 */

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
    details?: any;
    request_id?: string;
  };
  timestamp: string;
}

export interface HealthStatus {
  status: string;
  database: string;
  demo_mode: boolean;
  scenario_date: string;
  dataset_version: string;
}

export interface ProductFact {
  [key: string]: string | number | boolean;
}

export interface Product {
  id: string;
  sku: string;
  name: string;
  brand: string;
  category: string;
  description: string;
  price: number;
  msrp: number;
  cost: number;
  weight_kg: number;
  status: string;
  facts: ProductFact;
  image_url: string;
}

export interface LocationStockSummary {
  location_id: string;
  location_name: string;
  location_code: string;
  on_hand: number;
  blocked: number;
  holds: number;
  reserved_orders: number;
  outbound_transfers: number;
  inbound_transfers: number;
  atp: number;
}

export interface ProductStockSummary {
  product: Product;
  atp_total: number;
  locations: LocationStockSummary[];
}

export interface IntentExtractResponse {
  intent_id: string;
  confidence: number;
  structured_query: {
    category?: string;
    brand?: string;
    max_price?: number;
    preferred_sku?: string;
    fulfillment?: string;
    hard_attributes?: Record<string, any>;
  };
  matched_skus: string[];
  explanation: string;
  requested_attributes: Record<string, any>;
  preferred_sku?: string;
}

export interface Quote {
  quote_id: string;
  sku: string;
  product_name: string;
  location_code: string;
  location_name: string;
  fulfillment_type: string;
  unit_price: number;
  fulfillment_fee: number;
  total_amount: number;
  currency: string;
  atp_available: number;
  estimated_availability_utc: string;
  valid_until_utc: string;
  can_fulfill: boolean;
  reason?: string;
}

export interface ReservationHold {
  hold_id: string;
  sku: string;
  location_code: string;
  quantity: number;
  expires_at_utc: string;
  expires_at?: string;
  status: string;
}

export interface Order {
  id?: string;
  order_id: string;
  code?: string;
  order_code: string;
  status: string;
  sku: string;
  product_name: string;
  location_code: string;
  fulfillment_type: string;
  total_amount: number;
  currency: string;
  allocation_id?: string;
  created_at_utc: string;
}

export interface StockChangeResult {
  order_id?: string;
  order_code?: string;
  transfer_id?: string;
  po_id?: string;
  status: string;
  stock_before?: Record<string, number>;
  stock_after?: Record<string, number>;
  origin_stock_before?: Record<string, number>;
  origin_stock_after?: Record<string, number>;
  destination_stock_before?: Record<string, number>;
  destination_stock_after?: Record<string, number>;
  movement_id: string;
  message?: string;
}

export interface Transfer {
  transfer_id: string;
  transfer_code: string;
  status: string;
  sku: string;
  product_name: string;
  origin_code: string;
  origin_name: string;
  destination_code: string;
  destination_name: string;
  quantity: number;
  eta_hours: number;
  created_at_utc: string;
  dispatched_at_utc?: string;
  received_at_utc?: string;
}

export interface PurchaseOrder {
  po_id: string;
  po_code: string;
  status: string;
  sku: string;
  product_name: string;
  supplier_name: string;
  location_code: string;
  quantity: number;
  unit_cost: number;
  total_cost: number;
  created_at_utc: string;
  received_at_utc?: string;
}

export interface KpiCards {
  stockout_pairs: number;
  excess_stock_cost: number;
  margin_opportunity: number;
  pending_proposals: number;
}

export interface Recommendation {
  recommendation_id: string;
  scenario_date: string;
  sku: string;
  product_name: string;
  location_code: string;
  location_name: string;
  action_type: 'TRANSFER' | 'PURCHASE' | 'MONITOR' | 'EXPEDITE';
  quantity: number;
  source_location_code?: string;
  source_location_name?: string;
  target_location_code?: string;
  target_location_name?: string;
  target_day: number;
  expected_lost_units_avoided: number;
  working_capital_required: number;
  logistics_cost: number;
  estimated_margin_opportunity: number;
  confidence_score: number;
  status: 'PENDING_APPROVAL' | 'APPROVED' | 'REJECTED' | 'EXECUTED';
  reasoning: string;
  alternative_purchase?: {
    action: string;
    quantity: number;
    supplier: string;
    lead_time_days: number;
    working_capital_required: number;
    estimated_margin_opportunity: number;
    reason_not_chosen: string;
  };
  alternative_no_action?: {
    action: string;
    stockout_day: number;
    lost_units: number;
    margin_lost: number;
  };
}

export interface DashboardSummary {
  kpi_cards: KpiCards;
  top_recommendations: Recommendation[];
  scenario_date: string;
  last_refreshed_at_utc: string;
}

export interface ForecastDay {
  day_index: number;
  date: string;
  baseline_ma28: number;
  challenger_snaive7: number;
  chosen_forecast: number;
  scenario_p10: number;
  scenario_p90: number;
  simulated_stock_level: number;
  is_stockout: boolean;
}

export interface ForecastData {
  sku: string;
  location_code: string;
  horizon_days: number;
  backtest_metrics: {
    wape: number;
    mae: number;
    holdout_days: number;
    baseline_model: string;
    challenger_model: string;
    selected_model: string;
  };
  daily_forecast: ForecastDay[];
  external_signal?: {
    signal_code: string;
    name: string;
    raw_lift: number;
    capped_lift: number;
    recommendation: string;
  };
}

export interface TrendSignal {
  signal_code: string;
  source_type: string;
  name: string;
  category: string;
  period: string;
  region: string;
  sample_size: number;
  raw_lift: number;
  capped_lift: number;
  confidence: number;
  recommendation: 'PURCHASE' | 'MONITOR' | 'TRANSFER';
  recommended_qty: number;
  target_sku: string;
  explanation: string;
  ai_classification?: string;
  ai_rationale?: string;
  ai_mode?: string;
}

export interface CatalogRule {
  rule_id: string;
  name: string;
  description: string;
  severity: string;
  pass_rate: number;
}

export interface CatalogDefect {
  sku: string;
  rule_id: string;
  field: string;
  message: string;
  suggested_action: string;
}

export interface CatalogPatch {
  patch_id: string;
  sku: string;
  field: string;
  current_value: string;
  proposed_value: string;
  source: string;
  verified_facts: Record<string, any>;
  status: string;
}

export interface CatalogAuditSummary {
  overall_score: number;
  total_skus: number;
  rules: CatalogRule[];
  defects: CatalogDefect[];
  pending_patches: CatalogPatch[];
  resolved_patches?: Array<{
    patch_id: string;
    sku: string;
    field: string;
    applied_value: string;
    score_improvement: string;
    status: string;
    timestamp: string;
  }>;
}

export interface TraceEvent {
  id: string;
  timestamp: string;
  event_type: string;
  actor: string;
  entity_type: string;
  entity_id: string;
  description: string;
  details?: Record<string, any>;
}

export interface ComparisonRow {
  attribute: string;
  values: (string | number | boolean | null)[];
  fact_ids?: any[];
}

export interface CompatibilityReport {
  sku: string;
  is_compatible: boolean;
  confidence: number;
  product_wattage: number;
  required_wattage: number;
  warning?: string | null;
  explanation?: string | null;
  ai_mode: string;
}

export interface ComparisonResponse {
  products: Product[];
  rows: ComparisonRow[];
  tradeoffs: string[];
  compatibility: CompatibilityReport;
  ai_mode: string;
}

// Helper fetcher
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(endpoint, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => null);
    const msg = errorBody?.error?.message || errorBody?.detail || `HTTP ${res.status}: ${res.statusText}`;
    throw new Error(msg);
  }

  const envelope: ApiResponse<T> = await res.json();
  if (envelope && typeof envelope === 'object' && 'data' in envelope) {
    const data: any = envelope.data;
    if (
      data &&
      typeof data === 'object' &&
      'items' in data &&
      Array.isArray(data.items) &&
      !('signals' in data) &&
      !('pending_patches' in data)
    ) {
      if (data.next_cursor !== undefined || ('total' in data && Object.keys(data).length <= 2)) {
        return data.items as any;
      }
    }
    return data;
  }
  return envelope as any;
}

export const api = {
  // Health
  getHealthReady: () => apiFetch<HealthStatus>('/health/ready'),

  // Catalog
  getProducts: (params?: { category?: string; search?: string }) => {
    const query = new URLSearchParams();
    if (params?.category) query.set('category', params.category);
    if (params?.search) query.set('search', params.search);
    return apiFetch<Product[]>(`/api/v1/catalog/products?${query.toString()}`);
  },
  getProductStock: (sku: string) => apiFetch<ProductStockSummary>(`/api/v1/inventory/stock/${sku}`),
  getAllStock: () => apiFetch<ProductStockSummary[]>('/api/v1/inventory/stock'),

  // Shopping / Discovery
  extractIntent: (query: string, location_code: string = 'S1') =>
    apiFetch<IntentExtractResponse>('/api/v1/shopping/intent', {
      method: 'POST',
      body: JSON.stringify({ query, location_code }),
    }),

  compareProducts: (data?: { skus?: string[]; product_ids?: string[]; min_wattage?: number; connector?: string }) =>
    apiFetch<ComparisonResponse>('/api/v1/comparisons', {
      method: 'POST',
      body: JSON.stringify(data || { skus: ['RQ001', 'RQ002'], min_wattage: 20, connector: 'USB-C' }),
    }),

  createQuote: (data: { sku: string; location_code: string; fulfillment_type: string; quantity: number }) =>
    apiFetch<Quote>('/api/v1/shopping/quote', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  createHold: (data: { quote_id: string; sku: string; location_code: string; quantity: number }) =>
    apiFetch<ReservationHold>('/api/v1/shopping/hold', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  placeOrderFromHold: (data: { hold_id: string; shopper_name: string; shopper_email?: string }) =>
    apiFetch<Order>('/api/v1/orders/from-hold', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getOrders: () => apiFetch<Order[]>('/api/v1/orders'),

  fulfillPickupOrder: (order_id: string, note?: string) =>
    apiFetch<StockChangeResult>(`/api/v1/orders/${order_id}/fulfill-pickup`, {
      method: 'POST',
      body: JSON.stringify({ note: note || 'Customer picked up at counter' }),
    }),

  // Transfers
  getTransfers: () => apiFetch<Transfer[]>('/api/v1/transfers'),
  dispatchTransfer: (transfer_id: string) =>
    apiFetch<StockChangeResult>(`/api/v1/transfers/${transfer_id}/dispatch`, {
      method: 'POST',
      body: JSON.stringify({ note: 'Dispatched via logistics truck' }),
    }),
  receiveTransfer: (transfer_id: string) =>
    apiFetch<StockChangeResult>(`/api/v1/transfers/${transfer_id}/receive`, {
      method: 'POST',
      body: JSON.stringify({ note: 'Received and verified at dock' }),
    }),

  // Purchase Orders
  getPurchaseOrders: () => apiFetch<PurchaseOrder[]>('/api/v1/purchase-orders'),
  receivePurchaseOrder: (po_id: string) =>
    apiFetch<StockChangeResult>(`/api/v1/purchase-orders/${po_id}/receive`, {
      method: 'POST',
      body: JSON.stringify({ note: 'Supplier goods received and put away' }),
    }),

  // Planning & Decisions
  getDashboardSummary: () => apiFetch<DashboardSummary>('/api/v1/planning/dashboard'),
  refreshIntelligence: () =>
    apiFetch<DashboardSummary>('/api/v1/planning/refresh-intelligence', { method: 'POST' }),

  getForecast: (sku: string, location_code: string = 'S1', horizon_days: number = 14) =>
    apiFetch<ForecastData>(`/api/v1/planning/forecast?sku=${sku}&location_code=${location_code}&horizon_days=${horizon_days}`),

  approveProposal: (recommendation_id: string) =>
    apiFetch<{ recommendation_id: string; status: string; action_type: string; created_entity_id: string; created_entity_code: string; message: string }>(
      `/api/v1/planning/proposals/${recommendation_id}/approve`,
      { method: 'POST' }
    ),

  getTrendAnalysis: () => apiFetch<{ signals: TrendSignal[] }>('/api/v1/planning/trends'),

  // Catalog Ops
  getCatalogAudit: () => apiFetch<CatalogAuditSummary>('/api/v1/catalog-ops/audit'),
  approveCatalogPatch: (patch_id: string) =>
    apiFetch<{ patch_id: string; status: string; previous_audit_score: number; new_audit_score: number; patched_fields: Record<string, any> }>(
      `/api/v1/catalog-ops/patches/${patch_id}/approve`,
      { method: 'POST' }
    ),
  getCatalogProducts: () => apiFetch<{ items: any[] }>('/api/v1/catalog/products?limit=50'),
  enrichCatalogSpecs: (sku: string) =>
    apiFetch<any>('/api/v1/catalog/enrich-specs', {
      method: 'POST',
      body: JSON.stringify({ sku }),
    }),

  // Trace & Events
  getTraceEvents: (params?: { entity_type?: string; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.entity_type) query.set('entity_type', params.entity_type);
    if (params?.limit) query.set('limit', String(params.limit));
    return apiFetch<TraceEvent[]>(`/api/v1/events/trace?${query.toString()}`);
  },

  // State Restoration
  resetSession: () =>
    apiFetch<{ status: string; workspace_id: string; message: string }>('/api/v1/sessions/reset', {
      method: 'POST',
    }),
};
