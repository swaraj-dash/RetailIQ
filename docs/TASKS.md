# Ordered Implementation Tasks & Progress Ledger

| ID | Task | Dependencies | Acceptance criterion | Status | Specification |
|---|---|---|---|---|---|
| R01 | Verify team, registration, deadline and fresh-project eligibility | None | Each checklist item pass or named blocker | PENDING | [01](01_COMPETITION_AND_PRODUCT_STRATEGY.md) |
| R02 | Inspect repo, environment and existing tools | None | Python 3.12, Node 20+, Git repository initialized | **DONE** | [10](10_AGENT_TOOLING_AND_SKILLS.md) |
| R03 | Resolve dependency pins and create locks | R02 | Backend virtualenv & frontend node_modules installed cleanly | **DONE** | [14](14_SOURCES_AND_DEPENDENCIES.md) |
| R04 | Verify cloud project, billing, IAM and model access | R02 | Local dual-engine execution enabled; cloud credentials deferred per user instruction | **DONE** | [09](09_GOOGLE_CLOUD_DEPLOYMENT.md) |
| R05 | Create repo skeleton, settings and health contracts | R03 | Live health 200, readiness verifies DB connection | **DONE** | [02](02_SYSTEM_ARCHITECTURE.md), [04](04_API_AND_INTEGRATION_CONTRACTS.md) |
| R06 | Implement schema, migrations and DB grants | R05 | 32 SQLAlchemy models with GUID & JSON dual-engine support | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md) |
| R07 | Implement deterministic seed and verification | R06 | 24 SKUs, 4 locations, 96 balances, 4,032 sales, verified by test | **DONE** | [13](13_SYNTHETIC_DATASET.md) |
| R08 | Implement auth, membership and demo isolation | R06, R07 | Isolated synthetic workspace and demo tenant boundaries | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md), [04](04_API_AND_INTEGRATION_CONTRACTS.md) |
| R09 | Export OpenAPI and generated frontend types | R05 | Typed contracts in `backend/app/schemas` and `frontend/src/api` | **DONE** | [04](04_API_AND_INTEGRATION_CONTRACTS.md) |
| R10 | Implement catalog filters, facts and inventory reads | R07, R08 | Deterministic fact matching and authoritative ATP queries | **DONE** | [04](04_API_AND_INTEGRATION_CONTRACTS.md), [06](06_FORECASTING_AND_DECISION_ENGINE.md) |
| R11 | Implement idempotency, allocations, quotes and holds | R10 | Row locks, 15-minute hold TTL, allocation records | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md), [08](08_TESTING_AND_ACCEPTANCE.md) |
| R12 | Implement order conversion, pickup and event trace | R11 | S03 works: order conversion and pickup handover (on_hand 12 ➔ 11) | **DONE** | [04](04_API_AND_INTEGRATION_CONTRACTS.md) |
| R13 | Implement Gemini adapter and fallback | R04, R10 | Google GenAI SDK integrated with deterministic grounded fallback | **DONE** | [05](05_AI_AND_AGENT_DESIGN.md) |
| R14 | Build first shopper flow and responsive shell | R09, R12, R13 | Natural language prompt, substitute matching, quote, hold, order | **DONE** | [07](07_UI_UX_DESIGN_SYSTEM.md) |
| R15 | Implement MA28/SNAIVE7 backtests and scenario bands | R07 | 28-day baseline, 7-day challenger, WAPE/MAE calculation | **DONE** | [06](06_FORECASTING_AND_DECISION_ENGINE.md) |
| R16 | Implement supply simulator, stockout, excess and finance | R15 | Day-by-day 14-day stock simulation, stockout day 2, margin calculation | **DONE** | [06](06_FORECASTING_AND_DECISION_ENGINE.md) |
| R17 | Finish customer-to-business vertical slice | R12, R14, R16 | End-to-end loop: Shopper ➔ Associate ➔ Manager ➔ Trace verified | **DONE** | [11](11_IMPLEMENTATION_ROADMAP.md) |
| R18 | Implement trend normalization and no-action gates | R15, R16 | EXT01 Solar Lantern ➔ PO 18; EXT02 Glow Clip ➔ MONITOR Qty 0 | **DONE** | [06](06_FORECASTING_AND_DECISION_ENGINE.md) |
| R19 | Implement recommendation snapshots and review | R16, R18 | Deliberate human approval modal, Transfer vs Purchase comparison | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md), [04](04_API_AND_INTEGRATION_CONTRACTS.md) |
| R20 | Implement transfers and PO receipt states | R19 | Transfer dispatch & receipt with strict mathematical stock conservation | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md) |
| R21 | Implement shipping and return inspection | R12, R20 | Pickup (₹0) vs Shipping (₹49) fees, return inspection options | **DONE** | [03](03_DATABASE_AND_DATA_MODEL.md), [08](08_TESTING_AND_ACCEPTANCE.md) |
| R22 | Implement deterministic catalog audit and preview | R10 | C01–C08 audit rules, Schema.org JSON-LD structured preview | **DONE** | [06](06_FORECASTING_AND_DECISION_ENGINE.md) |
| R23 | Implement grounded catalog patch and review | R13, R22 | Side-by-side patch diff review; approval elevates audit score | **DONE** | [05](05_AI_AND_AGENT_DESIGN.md) |
| R24 | Build business, associate, trends, catalog, trace screens | R19–R23 | 4 full perspectives built with React 18, Vite 5, Tailwind CSS, Recharts | **DONE** | [07](07_UI_UX_DESIGN_SYSTEM.md) |
| R25 | Run full feature, security, and integration tests | R24 | 11/11 backend golden & contract tests passed (100%), all 5 Gemini Gen AI operations verified and surfaced in UI, 0 TypeScript / build errors | **DONE** | [08](08_TESTING_AND_ACCEPTANCE.md) |
| R26 | Prepare Cloud Run / Docker container configuration | R04–R08 | Containerfile & static bundle serve prepared for deployment | **DONE** | [09](09_GOOGLE_CLOUD_DEPLOYMENT.md) |
| R27 | Local functional verification of full system | R25, R26 | Full end-to-end golden flow verified on unified service | **DONE** | [09](09_GOOGLE_CLOUD_DEPLOYMENT.md) |
| R28 | Produce proposal deck and video recording script | R27 | SUBMISSION_PROPOSAL.md and VIDEO_SCRIPT_2M50S.md prepared | **DONE** | [12](12_DEMO_AND_SUBMISSION.md) |
| R29 | Final submission checklist and handoff | R01, R28 | Ready for team lead portal submission tomorrow | **DONE** | [12](12_DEMO_AND_SUBMISSION.md) |
