# HTTP, schema and integration contracts

Implement exactly these contracts. FastAPI-generated OpenAPI is the implementation artifact; this document is its specification. Generate TypeScript types from OpenAPI during implementation and fail CI on drift. No endpoint accepts arbitrary SQL, Python, URLs, model names, actor roles or workspace IDs.

## Protocol and shared types

Prefix `/api/v1`. JSON UTF-8. All nonhealth responses use `Envelope<T> = {data:T,meta:{request_id:UUID,server_time:Timestamp,is_synthetic:boolean}}`. HTTP health responses are the explicit exception. All table names/fields are defined in [03_DATABASE_AND_DATA_MODEL.md](03_DATABASE_AND_DATA_MODEL.md).

In the schemas below `?` means nullable, not omitted; every listed response field must be returned. Request fields marked `optional` may be omitted and use the stated default. Extra request keys are rejected (`extra=forbid`). `UUID`, `Timestamp` (RFC3339 UTC), `Date` (YYYY-MM-DD), `Money` (integer paise, 0–10^12), `Qty` (integer 1–5 shopper, 1–10000 operations), `Ratio` (0–1), and `Units` (finite nonnegative decimal JSON number, ≤6 decimals) are scalar types. Monetary computed benefit fields may be signed. No NaN/Infinity. Strings are trimmed; HTML is rendered as text.

`Page<T>={items:T[],next_cursor:string?}`. `limit` defaults 20, max100; cursor is URL-safe base64 of `(created_at,id)` validated and bound to filters; ascending code pages use `code,id`. Expired/invalid cursor →422. APIs sort deterministically. ISO dates use the workspace’s scenario date for business planning, wall clock for security/TTL.

Authorization: bearer Firebase ID token on all `/api/v1` endpoints. `POST /demo/sessions` needs a verified token but no existing membership. All others derive active workspace membership from UID. `S` = signed-in customer/associate/manager; `A` = associate/manager; `M` = manager; `DEMO_MANAGER` satisfies all roles inside its own synthetic workspace. Every query and nested reference is tenant scoped. Unauthorized foreign IDs return404; do not reveal existence.

Request bounds not repeated below: destination/store/category codes must resolve to allowed seed codes; `needed_within_days` is null or integer 0–30; `required_attributes` at most10; preference strings at most80 characters; any otherwise unbounded request string max120 characters; UUID arrays max40. Unknown types/attributes/operators fail422. All relevant entity IDs must resolve in the current tenant. Expired demo workspace access returns403 `DEMO_SESSION_EXPIRED`; owner maintenance must remove it before its UID can start a replacement.

## Errors, idempotency and versions

Errors are `{error:{code:string,message:string,details:object,retryable:boolean},meta:{request_id,server_time,is_synthetic}}`, not the success envelope. Validation details contain paths and reasons, never submitted secrets.

| HTTP | Codes / meaning |
|---|---|
| 400 | `INVALID_REQUEST`, `INVALID_TRANSITION` |
| 401 / 403 | `AUTH_REQUIRED`, `TOKEN_INVALID` / `ROLE_REQUIRED`, `DEMO_ONLY`, `DEMO_SESSION_EXPIRED` |
| 404 | `NOT_FOUND` for tenant-filtered lookup |
| 409 | `INSUFFICIENT_STOCK`, `QUOTE_STALE`, `HOLD_EXPIRED`, `VERSION_CONFLICT`, `PROPOSAL_STALE`, `IDEMPOTENCY_CONFLICT`, `ALREADY_CONVERTED`, `INVALID_STATE` |
| 422 | `VALIDATION_ERROR`, `CONSTRAINT_NOT_SUPPORTED` |
| 429 | `RATE_LIMITED`, `DEMO_CAPACITY_REACHED`, `AI_BUDGET_EXCEEDED`; include `Retry-After` |
| 503 | `DEPENDENCY_UNAVAILABLE`, `PLANNING_BUSY`, `INVENTORY_INVARIANT_FAILED` |

Every POST/PATCH/DELETE below requires `Idempotency-Key` (UUID string), including AI and refresh requests. Use key=`workspace:<UUID>` for regular calls and `bootstrap:<UID>` for session creation; actor UID and full key are part of the global journal primary key. The bootstrap journal has nullable workspace_id until a workspace exists. Idempotency body hash is SHA256 of UTF-8 JSON with sorted keys, compact separators, normalized path and method. Advisory-lock hash is a fixed 64-bit prefix of SHA256(scope/key), not Python’s randomized `hash()`. Collisions only serialize unrelated requests; stored keys remain full strings. Inside a transaction, return prior completed response if method/path/body hash matches; otherwise409. Lock/recheck before any stock mutation. Persist successful response and mutations atomically. Validation/authorization failures are not cached. For long AI operations, reserve quota first and take a separate intent request lock without holding inventory locks; store the result once. Duplicate calls must not emit duplicate events even if model invocation retries.

Write requests that change an existing entity include `expected_version:int≥1`. Server locks/checks current version and returns409 with `current_version` on mismatch. Holds/orders/transfers/POs/patches/recommendations include version in responses. A quote is not a stock guarantee; creating a hold revalidates current stock, price, route and constraints. Quote expires after300 seconds; hold after900 seconds.

## Core response objects

```text
Session = {workspace_id:UUID,role:"DEMO_MANAGER",scenario_date:Date,dataset_version:string,
           expires_at:Timestamp,workspace_name:string}
Fact = {id:UUID,attribute:string,value:string|number|boolean|string[],unit:string?,
        source_ref:string}
Product = {id:UUID,sku:string,title:string,description:string,brand:string,category_code:string,
           variant_label:string,price_minor:Money,currency:"INR",image_path:string?,
           facts:Fact[],published_availability:"IN_STOCK"|"OUT_OF_STOCK",version:int}
Location = {id:UUID,code:string,name:string,kind:"STORE"|"DC",locality_code:string,
            pickup_enabled:boolean,ship_enabled:boolean}
Stock = {product_id:UUID,location_id:UUID,on_hand:int,blocked:int,active_hold:int,
         active_order:int,active_transfer:int,inventory_version:int,atp:int,
         incoming_confirmed:int,as_of:Timestamp}
Constraints = {category_code:string,budget_minor:Money,preferred_sku:string?,
               destination_code:string,preferred_store_code:string?,
               mode:"ANY"|"PICKUP"|"SHIP",needed_within_days:int?,
               required_attributes:AttributeConstraint[],preferences:string[]}
AttributeConstraint = {attribute:string,operator:"EQ"|"GTE"|"LTE"|"CONTAINS",
                       value:string|number|boolean}
Reason = {code:"WITHIN_BUDGET"|"FACT_MATCH"|"AVAILABLE"|"SUBSTITUTE"|"TRADEOFF",
          fact_ids:UUID[],text:string}
Candidate = {product:Product,stock:Stock[],match_score:number,reasons:Reason[],is_substitute:boolean}
IntentResult = {intent_id:UUID,trace_id:UUID,constraints:Constraints,
                status:"NEEDS_INFO"|"MATCHED"|"NO_MATCH",question:string?,
                candidates:Candidate[],ai_mode:"LIVE"|"FALLBACK",warnings:string[]}
QuoteOption = {id:UUID,origin_location_id:UUID,mode:"PICKUP"|"SHIP",
               quantity:int,unit_price_minor:Money,customer_fee_minor:Money,
               fulfillment_cost_minor:Money,total_minor:Money,lead_days:int,
               promise_kind:"SIMULATED_ESTIMATE",inventory_version:int,
               recommendation_reason:string}
Quote = {id:UUID,product_id:UUID,quantity:int,options:QuoteOption[],expires_at:Timestamp,
         unavailable_reasons:string[]}
Hold = {id:UUID,product_id:UUID,location_id:UUID,quantity:int,state:string,
        expires_at:Timestamp,quote_id:UUID,quote_option_id:UUID,version:int}
Order = {id:UUID,code:string,intent_id:UUID?,product_id:UUID,quantity:int,
         origin_location_id:UUID,demand_location_id:UUID,destination_code:string,
         mode:"PICKUP"|"SHIP",unit_price_minor:Money,customer_fee_minor:Money,
         total_minor:Money,status:"CONFIRMED"|"FULFILLED"|"SHIPPED"|"DELIVERED"|"CANCELLED",
         version:int}
Transfer = {id:UUID,product_id:UUID,source_location_id:UUID,destination_location_id:UUID,
            quantity:int,received_quantity:int,cost_minor:Money,expected_date:Date,
            status:"APPROVED"|"IN_TRANSIT"|"RECEIVED"|"CANCELLED",version:int}
PurchaseOrder = {id:UUID,product_id:UUID,supplier_id:UUID,destination_location_id:UUID,
                 quantity:int,received_quantity:int,unit_cost_minor:Money,freight_minor:Money,
                 expected_date:Date,status:"APPROVED"|"RECEIVED"|"CANCELLED",version:int}
Return = {id:UUID,order_id:UUID,product_id:UUID,location_id:UUID,quantity:int,
          refund_minor:Money,status:"REQUESTED"|"RECEIVED"|"RESTOCKED"|"DAMAGED",version:int}
```

Product responses deliberately omit internal cost for shopper endpoints. Business finance comes from authorized planning endpoints. `DEMO_MANAGER` can see both views in its own workspace.

## Shopping and operations endpoints

| ID | Method/path | Role; request/query | Success response |
|---|---|---|---|
| API01 | `GET /health/live` (no prefix) | public, no body | 200 `{status:"ok"}` |
| API02 | `GET /health/ready` (no prefix) | public | 200 `{status:"ready",database:"ok",schema:"current"}`; 503 otherwise |
| API03 | `POST /demo/sessions` | verified UID; `{}` | 201 Session; existing UID returns200 existing Session |
| API04 | `GET /system/status` | M | `{app_version,dataset_version,ai_provider,model_id,ai_configured:boolean,last_ai_success_at:Timestamp?,planning_run_id:UUID?}` |
| API05 | `GET /locations` | S | `{items:Location[]}` |
| API06 | `GET /products` | S; query `q` max120 optional, `category_code` optional, `budget_minor` optional, `limit,cursor` | `Page<Product>` |
| API07 | `GET /products/{product_id}` | S | Product |
| API08 | `GET /inventory` | S; required `product_id`, optional `location_id` | `{items:Stock[]}` |
| API09 | `POST /intents` | S; `{text:string(1..2000),destination_code:string,preferred_store_code:string?,previous_intent_id:UUID?}` | 201 IntentResult; previous intent must belong to actor |
| API10 | `POST /comparisons` | S; `{product_ids:UUID[2..3],intent_id:UUID?,attributes:(string|number|boolean|null)[2..10][],fact_ids:(UUID|null)[][],tradeoffs:string[]}` | 201 `{products:Product[],rows:{attribute:string,values:(string|number|boolean|null)[],fact_ids:(UUID|null)[][]}[],tradeoffs:string[],ai_mode:"LIVE"|"FALLBACK"}` |
| API11 | `POST /quotes` | S; `{product_id:UUID,quantity:Qty,destination_code:string,mode:"ANY"|"PICKUP"|"SHIP",preferred_store_code:string?,needed_within_days:int?,intent_id:UUID?}` | 201 Quote; no options is valid, no stock mutation |
| API12 | `POST /holds` | S; `{quote_id:UUID,quote_option_id:UUID}` | 201 Hold |
| API13 | `DELETE /holds/{hold_id}` | S owner; query `expected_version` | 200 Hold with RELEASED state (expiry field retained) |
| API14 | `GET /holds/{hold_id}` | S owner | Hold; effective state EXPIRED when wall-clock expiry passed, even before cleanup |
| API15 | `POST /orders` | S; `{hold_id:UUID,expected_version:int}` | 201 Order; duplicate hold conversion409 |
| API16 | `GET /orders` | S own only; A/M may query `scope=workspace`, default own; `limit,cursor` | `Page<Order>` |
| API17 | `GET /orders/{order_id}` | S owner or A/M | Order |
| API18 | `POST /orders/{order_id}/transition` | owner can CANCEL; A/M other actions; `{action:"CANCEL"|"FULFILL_PICKUP"|"DISPATCH"|"DELIVER",expected_version:int}` | 200 Order |
| API19 | `GET /transfers` | A; `limit,cursor` | `Page<Transfer>` |
| API20 | `POST /transfers/{transfer_id}/transition` | A except CANCEL=M; `{action:"DISPATCH"|"RECEIVE"|"CANCEL",expected_version:int}` | 200 Transfer |
| API21 | `GET /purchase-orders` | A; `limit,cursor` | `Page<PurchaseOrder>` |
| API22 | `POST /purchase-orders/{po_id}/transition` | A for RECEIVE, M for CANCEL; `{action:"RECEIVE"|"CANCEL",expected_version:int}` | 200 PurchaseOrder |
| API23 | `POST /returns` | S owner or A/M; `{order_id:UUID,quantity:Qty,location_id:UUID,reason:string(1..120)}` | 201 Return |
| API24 | `POST /returns/{return_id}/transition` | A; `{action:"RECEIVE"|"RESTOCK"|"DAMAGE",expected_version:int}` | 200 Return |
| API25 | `POST /events` | S; `{intent_id:UUID?,product_id:UUID?,category_code:string?,location_id:UUID,event_type:"VIEW"|"COMPARE"|"CART"|"CHECKOUT",session_key:string(1..64)}` | 201 `{event_id:UUID,deduplicated:boolean}` |

On cart reload, recover the hold ID from local session state and call API14; never trust a stored ACTIVE flag. The server expiry and current state control checkout.

Event timestamps, source and synthetic label are server-derived. SEARCH, STOCKOUT, SUBSTITUTE and PURCHASE are created by services, never trusted from arbitrary frontend events. A signed user can still click repeatedly; intelligence deduplicates by session and caps contributions as defined in [06_FORECASTING_AND_DECISION_ENGINE.md](06_FORECASTING_AND_DECISION_ENGINE.md).

## Intelligence schemas

```text
Evidence = {source_id:UUID?,source_ref:string,source_kind:string,is_synthetic:boolean,
            period_start:Date,period_end:Date,reliability:Ratio,summary:string}
ForecastPoint = {date:Date,mean_units:Units,lower_units:Units,upper_units:Units}
Forecast = {run_id:UUID,product_id:UUID,location_id:UUID,as_of_date:Date,
            model:"MA28"|"SNAIVE7"|"COLD",points:ForecastPoint[],wape:number?,
            baseline_wape:number?,mae:number,confidence:"LOW"|"MEDIUM"|"HIGH",
            band_label:"Scenario range, not calibrated probability",evidence:Evidence[]}
Alternative = {action:"TRANSFER"|"PURCHASE"|"TEST_ORDER"|"MONITOR"|"NO_ACTION",
               source_location_id:UUID?,supplier_id:UUID?,quantity:int,arrival_day:int?,
               feasible:boolean,rejection_reasons:string[],lost_units:Units,
               recovered_units:Units,action_cost_minor:Money,holding_cost_minor:Money,
               unsold_risk_minor:Money,working_capital_minor:Money,
               margin_opportunity_minor:Money}
Decision = {horizon_days:int,atp:int,incoming:{date:Date,quantity:int,reference_id:UUID}[],
            forecast_units:Units,safety_units:Units,stockout_days:int?,excess_units:Units,
            historical_summary:string,evidence:Evidence[],alternatives:Alternative[],
            expected_upside_minor:int,downside_risk_minor:Money,working_capital_minor:Money,
            margin_opportunity_minor:int,confidence:"LOW"|"MEDIUM"|"HIGH",confidence_score:Ratio,
            assumptions:string[],explanation:string,algorithm_version:string,
            source_event_ids:UUID[]}
Recommendation = {id:UUID,run_id:UUID,product_id:UUID,location_id:UUID,intent_id:UUID?,
                  action:string,quantity:int,source_location_id:UUID?,supplier_id:UUID?,
                  status:"PROPOSED"|"APPROVED"|"REJECTED"|"STALE"|"EXECUTED",
                  decision:Decision,expires_at:Timestamp,version:int}
AuditIssue = {rule_id:string,severity:"HIGH"|"MEDIUM"|"LOW",field:string,
              message:string,fact_ids:UUID[],weight:int}
CatalogAudit = {id:UUID,product_id:UUID,product_version:int,score_before:number,
                issues:AuditIssue[]}
CatalogPatch = {id:UUID,audit_id:UUID,product_id:UUID,base_product_version:int,
                changes:{field:"title"|"description",before:string,after:string}[],
                fact_refs:UUID[],status:"PROPOSED"|"APPROVED"|"REJECTED"|"STALE",
                ai_mode:"LIVE"|"FALLBACK",version:int}
```

## Business and catalog endpoints

| ID | Method/path | Role; request/query | Success response |
|---|---|---|---|
| API26 | `POST /planning/refresh` | M; `{as_of_date:Date}` exactly workspace scenario date | 201 `{run_id:UUID,forecast_count:int,recommendation_count:int,completed_at:Timestamp}` |
| API27 | `GET /forecasts` | M; required `product_id,location_id`; `horizon_days` enum7/14/28 default14; optional `run_id` (latest if absent) | Forecast; 404 if no completed run |
| API28 | `GET /recommendations` | M; optional `status,action,location_id,limit,cursor` | `Page<Recommendation>`; order priority score descending then id |
| API29 | `GET /recommendations/{recommendation_id}` | M | Recommendation |
| API30 | `POST /recommendations/{recommendation_id}/review` | M; `{decision:"APPROVE"|"REJECT",expected_version:int,note:string(0..300)}` | 200 `{recommendation:Recommendation,transfer:Transfer?,purchase_order:PurchaseOrder?}` |
| API31 | `GET /dashboard` | M; optional `location_id` | `{run_id:UUID?,as_of_date:Date,stale:boolean,stockout_sku_locations:int,excess_units:int,excess_value_minor:Money,estimated_margin_opportunity_minor:int,pending_proposals:int,catalog_score:number?,observed_orders:int,observed_contribution_minor:int,segment_label:string}` |
| API32 | `GET /trends` | M; optional `category_code,location_id` | `{items:{signal_id:UUID,category_code:string,region_code:string,current_index:number,previous_index:number,reliability:Ratio,is_synthetic:boolean,internal_sessions_current:int,internal_sessions_previous:int,decision:"ACT"|"MONITOR"|"NO_ACTION",reason:string,recommendation_ids:UUID[]}[]}` |
| API33 | `POST /catalog/audits` | M; `{product_ids:UUID[]?}` null means all active ≤40 | 201 `{items:CatalogAudit[],score_overall:number}` |
| API34 | `GET /catalog/audits` | M; optional `product_id,limit,cursor` | `Page<CatalogAudit>` latest per product |
| API35 | `POST /catalog/patches` | M; `{audit_id:UUID}` | 201 CatalogPatch; deterministic fact template if AI unavailable |
| API36 | `POST /catalog/patches/{patch_id}/review` | M; `{decision:"APPROVE"|"REJECT",expected_version:int,expected_product_version:int}` | 200 `{patch:CatalogPatch,product:Product,reaudit:CatalogAudit}` |
| API37 | `GET /catalog/products/{product_id}/structured-data` | M; no body | `{json_ld:object,validation_issues:AuditIssue[],ready_for_export:boolean,publication_status:"PREVIEW_ONLY"}` |
| API38 | `GET /outcomes` | M; optional `intent_id,recommendation_id,limit,cursor` | `Page<{id, intent_id?,order_id?,recommendation_id?,event_type,observed_units,observed_contribution_minor,observed_at,is_synthetic}>` |
| API39 | `GET /traces/{intent_id}` | S owner or M | `{intent_id,trace_id,nodes:{type:"INTENT"|"QUOTE"|"ORDER"|"EVENT"|"RECOMMENDATION"|"OUTCOME",id:UUID,label:string,time:Timestamp}[],edges:{from_id:UUID,to_id:UUID,relation:string}[]}` |

API26 marks prior still-PROPOSED recommendations STALE only after the new run commits. Recommendations expire 30 wall-clock minutes after creation. For source linkage, select the most recent matching APP intent as recommendation.intent_id and retain every relevant source event ID in Decision; no APP intent means null.

API30 rejects APPROVE for MONITOR/NO_ACTION with422; no consequential operation exists. A proposal is EXECUTED only once its related transfer/PO is received, not merely approved. Cancel marks action CANCELLED in transfer/PO while retaining approval audit; it does not re-open the old proposal. Concurrent approvals serialize on recommendation row and share one action record with unique recommendation FK.

API31 sums only current, mutually exclusive chosen proposals, never all alternatives. Once approved, a proposal is removed from pending estimates; its action remains tracked. Category/store rollups sum forecast points, without treating summed scenario bounds as a calibrated interval. Trace graph must not imply causal attribution; edges say “informed by,” “reserved,” “fulfilled,” etc.

Outcomes use the complete enum in [03_DATABASE_AND_DATA_MODEL.md](03_DATABASE_AND_DATA_MODEL.md), including `RETURN_DAMAGED`. Return receipt reverses contribution margin; damage separately writes negative inventory cost and zero observed units. This is simplified demo accounting, not financial reporting compliance.

## Example flow

Resolved seed UUIDs below are placeholders for IDs obtained from API05/06, not literal valid seed IDs.

```json
{
  "text": "I need a 10000 mAh USB-C power bank under ₹1500 for travel. VoltGo Pro is unavailable; I can pick up in Indiranagar today.",
  "destination_code": "INDIRANAGAR",
  "preferred_store_code": "S1",
  "previous_intent_id": null
}
```

API09 yields MATCHED, `budget_minor=150000`, `mode=PICKUP`, `needed_within_days=0`, `category=POWER`, preferred SKU `Q001`, candidate `Q002` with price129900 and S1 ATP10. Facts cite verified 10000mAh and USB-C records. It must not claim airline approval; no such fact exists. The string “today” maps to `needed_within_days=0`, not an invented calendar date.

API11 with Q002, qty1, S1, PICKUP returns unit price129900, fee0, total129900, lead_days0. API12 creates a hold and ATP becomes9. API15 converts it without another decrement. API17 FULFILL_PICKUP leaves on_hand11, seed active ORDER allocations2 and ATP9. It produces an observed simulation contribution of 59900 paise and trace links. A subsequent planning refresh sees ATP9; golden baseline formulas in [06_FORECASTING_AND_DECISION_ENGINE.md](06_FORECASTING_AND_DECISION_ENGINE.md) use a fresh workspace ATP10.

## Gemini tool contracts

These are internal read-only interfaces, not public endpoints. All tool dispatch receives a server-generated `ToolContext {workspace_id,actor_uid,request_id,intent_id?}` outside model arguments. Unknown arguments or names are rejected. Max4 tool dispatches/request; max10 candidate products.

| Tool | Exact arguments | Result schema | Implementation |
|---|---|---|---|
| `search_catalog` | `{category_code:string?,budget_minor:Money?,required_attributes:AttributeConstraint[],query_terms:string[0..8]}` | `{products:Product[],unsupported_constraints:string[]}` | Parameterized catalog filters; missing hard facts exclude product |
| `get_availability` | `{product_ids:UUID[1..10]}` | `{items:Stock[]}` | Same inventory service as API08 |
| `get_fulfillment_options` | `{product_id:UUID,quantity:Qty,destination_code:string,mode:"ANY"|"PICKUP"|"SHIP",preferred_store_code:string?,needed_within_days:int?}` | `{options:QuoteOption[],unavailable_reasons:string[]}` | Read-only preview; does not create a quote or hold |
| `get_decision_evidence` | `{recommendation_id:UUID}` | `{decision:Decision}` | Manager-only; checks context role before dispatch |

The application may call these services deterministically after extraction. Function calling is demonstrated in a bounded explanation turn with explicit dispatch, automatic function execution disabled. No SQL/MCP/shell/browser runtime tools are exposed to the model. Tool result provenance is retained; generated numeric prose is never used as authoritative UI data.

## External integration boundaries

MVP loads external signal fixtures from [13_SYNTHETIC_DATASET.md](13_SYNTHETIC_DATASET.md); no ingestion HTTP endpoint is public. A future importer accepts `{source_ref,license_or_permission_ref,region_code,window_start,window_end,keyword,current_index,previous_index,reliability,is_synthetic:false}`, validates date/index bounds, maps category with Gemini then human review, and writes external_signals. Source access and redistribution must be authorized. Google Trends alpha access is not assumed. Merchant feeds, real stock systems, payment, courier, Maps and private assistant analytics are not runtime dependencies. Ship lanes and “festival” signals are explicitly synthetic fixtures.
