# Architecture decision record

Selected design decisions as of 17 October 2026. Accepted means chosen for implementation, not demonstrated by runtime tests.

| ID | Decision and rationale | Alternatives considered | Consequence |
|---|---|---|---|
| ADR01 | Keep RetailIQ; use purchase recovery as the demo narrative | UNLOST standalone, inventory-only, AEO-only | Broad platform with a focused proof |
| ADR02 | One React/Vite SPA and modular FastAPI backend | Next.js, multiple frontends, microservices | Static Hosting and a small operational surface |
| ADR03 | PostgreSQL 17 as system of record | Firestore, SQLite, BigQuery | Relational constraints and transactional stock; paid Cloud SQL |
| ADR04 | Gemini 3.5 Flash through current Google GenAI SDK/cloud API | Retired SDK, preview models, self-hosted Gemma | Provider adapter and real model-access gate |
| ADR05 | Mumbai app/SQL, global model endpoint | Unverified regional PayGo, all-US deployment | India app storage without India-only AI processing claims |
| ADR06 | Firebase Hosting plus direct Cloud Run API/CORS | Hosting rewrite, App Hosting, duplicate hosts | Explicit origin allowlist; no rewrite-region dependency |
| ADR07 | Anonymous Firebase identity and per-UID demo workspace | Shared mutable demo, public manager password | Isolated stock/actions with seed-cloning |
| ADR08 | Deterministic stock, forecast and money services | Autonomous LLM procurement | Testable decisions with explicit review |
| ADR09 | Bounded read-only tools; no agent framework | Multiple autonomous agents; model SQL/shell tools | Smaller attack surface and simpler debugging |
| ADR10 | MA28 baseline, SNAIVE7 challenger, scenario ranges | Neural forecasting; unsupported accuracy claims | Transparent small-data method; uncalibrated ranges |
| ADR11 | Bounded internal/external trend uplift and monitoring | Popularity directly triggers purchasing | Evidence required before new capital commitment |
| ADR12 | Single-SKU cart, full receipts, synthetic lanes | Split carts, WMS, real couriers/payments | Complete testable flow with explicit operational limits |
| ADR13 | Reviewed catalog facts and JSON-LD preview | Guaranteed AI visibility; private assistant analytics | Honest discoverability contribution |
| ADR14 | Separate migration/bootstrap Cloud Run job | Web workers migrate on startup | Owner/runtime separation and controlled schema changes |
| ADR15 | AGENTS and skills; avoid legacy workflows | Depend on old Antigravity workflow system | No dependency on the documented October 19 retirement |
| ADR16 | Exact initial pins and mandatory resolver gate | Floating latest; pretending lock validation | Fixed architecture with recorded package-level repairs |

## Unresolved issues

| ID | Issue | Owner | Resolution |
|---|---|---|---|
| B01 | Enrollment, age, residence and registration unknown | Team lead | Verify eligibility; obtain organizer clarification where needed |
| B02 | Exact cutoff/timezone and portal fields unknown | Team lead | Confirm dashboard/organizer instructions |
| B03 | Cloud project, billing, IAM and model quota not verified | Cloud owner | Successful live probe and public health deployment |
| B04 | Antigravity version unavailable in this workspace | Implementer | Inspect actual installation and run capability probes |
| B05 | Registry requests returned 403 in authoring environment | Implementer | Resolve locks, verify peers, build and audit dependencies |
| B06 | Complete scope exceeds a comfortable one-day build | Team lead | Deliver an honest deadline slice or adopt an independent-project schedule |
| B07 | Live external/merchant source access unavailable | Product owner | Verify authorization and provenance; synthetic demo remains usable |

| ADR17 | Multi-tiered Gemini Gateway with Enterprise ADC + API Key fallback | Rigid single-key dependency | Production-grade resilience supporting both cloud ADC and API key with explicit LIVE/FALLBACK labeling |
| ADR18 | Recommendation sorting prioritized by business actionability | Default creation timestamp sort | Prioritize TRANSFER > PURCHASE > MONITOR > NO_ACTION; prevents dormant monitor items from overshadowing urgent store transfers |
| ADR19 | Dynamic headline metrics calculation aggregating actual location ATP | Static demo literals | Authoritative real-time aggregation across location balances and pending order records |
| ADR20 | Demo workspace reset endpoint (`/api/v1/demo/reset`) with canonical state restoration | Single mutable workspace with no reset | Reliable evaluation handoff allowing judges to replay the full golden purchase recovery scenario cleanly |
| ADR21 | Idempotency enforcement via `IdempotencyRecord` and token-bucket request tracking via `UsageBucket` | Unused schema tables | Eliminates duplicate transactional orders and provides rate-limit audit trails |
| ADR22 | Full wiring of 5 Gemini operations + prompt injection defense + UI compatibility/rationale surfacing | Single operation LLM usage | Complete end-to-end AI wiring across Need Extraction, Spec Patching, Decision Explanation, Trend Signal Normalization, and Hardware Compatibility Evaluation with explicit LIVE vs FALLBACK transparency |

## Change procedure

Append an ADR with date, problem, evidence, alternatives, decision, affected files, tests and approver where required. Update authoritative contracts, generated types, UI and tests together. Routine compatible dependency repairs follow [14](14_SOURCES_AND_DEPENDENCIES.md) and need an evidence record. Database/framework/hosting changes require an explicit product/engineering decision. Never erase old decisions to conceal deviations. ADR17–ADR21 document implementation repairs and resilience enhancements executed during code audit.
