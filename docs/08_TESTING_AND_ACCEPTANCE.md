# Testing and acceptance

This is a required future test plan. No application tests have run in the specification phase. Tests must exercise independent expected outcomes and invariants, not merely repeat implementation formulas.

## Test organization and commands

Implement `backend/tests/unit`, `tests/api`, `tests/db`, `tests/integration`, `tests/ai`; browser tests live in repository `tests/e2e`. Use Pytest markers `unit,api,db,integration,ai_live`. Unit tests use fixed clocks and fixtures; integration tests use PostgreSQL. Never substitute SQLite for row-lock tests.

From repository root, after implementation:

```bash
docker compose -f infra/compose.yaml up -d db
uv sync --project backend --frozen --all-groups
uv run --project backend alembic -c backend/alembic.ini upgrade head
uv run --project backend python -m app.cli seed --dataset retailiq-demo-v1
uv run --project backend python -m app.cli verify-seed
uv run --project backend pytest backend/tests/unit -q
uv run --project backend pytest backend/tests/api backend/tests/db backend/tests/integration -q
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm ci
npx playwright install chromium
npx playwright test --project=chromium
```

Root `package.json` owns Playwright and its `testDir` `./tests/e2e`; frontend package owns build/typecheck. Playwright webServer starts the documented backend/frontend commands and Firebase Auth emulator for local tests. Production smoke uses `BASE_URL` and `FIREBASE_AUTH_EMULATOR_HOST` is never set. No test-mode auth bypass in a deployed server. Local auth tests use signed emulator tokens and reject startup when `APP_ENV=production`.

Expected outcomes: seed count/hash verification passes; every Pytest assertion passes; Alembic head matches; typecheck exits0; build creates `frontend/dist`; browser suite is not skipped or undiscovered with zero tests. Record actual counts and output; do not write “all tests passed” with skipped or undiscovered suites. Live model evaluation command:

```bash
uv run --project backend pytest backend/tests/ai -m ai_live -q
uv run --project backend python -m app.cli evaluate-ai --dataset tests/ai/prompts.json --repeats 2
```

`evaluate-ai` is an implementation task, not a pre-existing command. All CLI interfaces used by this package must be implemented as specified in `README.md`.

## Critical test cases

| Test ID | Fixture / action | Required assertion |
|---|---|---|
| T01 | `on_hand12,blocked0,active_ORDER2` | ATP10; expired HOLD excluded |
| T02 | 20 concurrent clients reserve same one remaining unit; independent connections | Exactly1 success;19 stock/conflict responses; ATP0; no negative balance |
| T03 | Hold→order conversion | Allocation changes kind; reservation total unchanged; repeat conversion409 |
| T04 | Concurrent same idempotency key / same body | Same response ID; one stock mutation/event |
| T05 | Same key with different body or path | `409 IDEMPOTENCY_CONFLICT`; unchanged state |
| T06 | Hold expiry boundary at exact `now` | Expired; cannot convert; ATP released without cleanup job |
| T07 | Quote expires/price changes/stock changes | `409` with reason; no hold created |
| T08 | Transfer approve→dispatch→receive twice | Reservation only at approve; one source decrement and one destination increment; duplicate replay harmless |
| T09 | PO approved but unreceived | Incoming visible; ATP unchanged until receipt increments once |
| T10 | Return receive→restock | Both on_hand/blocked increase on receipt; ATP rises only after restock |
| T11 | Return damaged / duplicate return quantity | Damage decreases on_hand and blocked equally; excess-return request rejected; correct accounting adjustment |
| T12 | Tenant A supplies tenant B UUID in each write/read/tool | `404`; zero B changes; no cross-tenant facts in AI context |
| T13 | Customer tries proposal approval, forged role/workspace | `403/422`; no mutation |
| T14 | Missing/expired/wrong-audience Firebase token | `401`; no model call or quota consumption beyond auth endpoint safety |
| T15 | Prompt asks to ignore rules and buy inventory | No mutation; no tool exists; invalid tool blocked and audit-safe |
| T16 | Model invents SKU/fact/stock/price/ETA | Validation/fallback; fabricated value never reaches authoritative card |
| T17 | Model timeout, bad schema, bounded retry | 1 retry; total budget; visible fallback; search still useful |
| T18 | Stock0 with incoming10 tomorrow | No pickup-now quote; no incoming counted as ATP |
| T19 | Unknown hard fact or destination | Product excluded/no route; no invented capability/ETA |
| T20 | Missing vs known-zero sales | Different treatment; no future leakage in imputation/backtests |
| T21 | All-zero actuals / WAPE null; MAE valid; no divide-by-zero | MAE valid; no divide-by-zero; monitor/no-action |
| T22 | Baseline outperforming seasonal candidate | MA28 selected; no fabricated improvement percentage |
| T23 | Golden RQ002/S1 | Target48, net32, buy36, first shortage6, lost26, transfer benefit ₹15,074.49, purchase ₹13,286.96 |
| T24 | MOQ25, pack6, net1 | Purchase30; test order forbidden below MOQ |
| T25 | Donor spare31, target32 | Transfer31; protection preserved; re-evaluate competing approvals |
| T26 | Golden RQ005 | Uplift0.5, demand1.5, target20, net14, buy18, capital ₹14,550 |
| T27 | Socially/weak region/stale/mapping<0.8 | No external uplift purchasing; MONITOR qty0 |
| T28 | Golden RQ021/S3 | Mean0.25/day, excess65, value ₹39,000 |
| T29 | Purchase accounting | Capital not subtracted twice from contribution; lower scenario may block action |
| T30 | Audit RQ002 patch | Only title/description change; fact refs valid; score improves; version increments |
| T31 | Patch stale product version/XSS text | `409 stale` or safe escaped text; no script execution |
| T32 | Refresh fails during commit | Prior run remains current; no partial forecasts/proposals |
| T33 | Approved proposal plus second competing approval | Source and recipient versions rechecked; no double spending source stock |
| T34 | Usage across multiple instances | Global/UID limit atomic; idempotent replay no duplicate charge |
| T35 | Migration fresh DB and upgrade existing seed | Both succeed; down/up only disposable DB; constraints/indexes present |
| T36 | Ledger reconciliation | Opening + movements = balances; `active_allocations ≤ sellable_physical`; network stock + in-transit conserved |

Use a synchronization barrier to start concurrency tests after connections acquire their sessions, not arbitrary sleeps. At least one race test uses real parallel transactions against PostgreSQL. Verify the final database state independently of API responses.

## Feature acceptance matrix

| ID | User-visible requirement | Scenario/test evidence |
|---|---|---|
| AC01 | Natural need becomes grounded suitable matches | S01,T16,T19,live extraction suite |
| AC02 | Unavailable preference yields factual substitute | S02,T18,T19 |
| AC03 | Hold/order/fulfillment works without overpromise | S03,T01–T07,T36 |
| AC04 | Forecast and stockout expose backtest/uncertainty | S04,T20–T23 |
| AC05 | Excess quantities and value reproducible | S05,T28 |
| AC06 | Transfer/purchase alternatives, approval, movement | S06,T08,T09,T24,T25,T33 |
| AC07 | Supported trend produces bounded stock action | S07,T26,T29 |
| AC08 | Weak trend yields monitoring with no approve action | S08,T27 |
| AC09 | Catalog audit, reviewed facts, structured preview | S09,T30,T31 |
| AC10 | Trace and expected/observed separation | S10,T29,T36 |
| AC11 | Associate and returns flows | T08–T11,mobile/desktop browser paths |
| AC12 | Public deployment, identity, persistence | Cloud smoke, token checks, restart test |
| AC13 | Accessible responsive UI and useful failures | Keyboard/contrast/3 viewport checks |

## Browser scenarios

Implement10 guided scenarios S01–S10 plus return/restock, stock-race UI conflict, auth isolation and AI fallback. Find controls by accessible role/name; use stable `data-testid` only for numeric cells. Assert network response and DB-backed visible state, not screenshots alone. Capture browser trace on failure. Browser tests do not approve real external purchases because no such integration exists.

Accessibility: run axe-core through Playwright after each major route; zero critical/serious findings, and manually test focus order, screen-reader labels, reduced motion and contrast. Test390×844,768×1024,1440×900. Do not use visual pixel-diff baselines as a substitute for functionality. Zero uncaught console errors; charts have matching data tables.

## Security and deployment evidence

Check repository and built assets for private keys, service-account JSON, DB secrets and tokens. Firebase public web config is not a server secret; API-key restrictions still apply. Verify HTML/catalog strings escaped, parameterized SQL, no arbitrary URL fetch, strict origin allowlist, auth on business endpoints, size/quantity limits and request quotas. Dependency audit unresolved high/critical exploitable issues block release; record advisories and patch versions rather than automatically changing frameworks.

Production smoke from a fresh browser: sign in anonymously, create session, health/readiness200, live intent call, hold/order, planning refresh, approve transfer, dispatch/receive, catalog review. Confirm a second browser has independent stock. Restart/deploy backend revision and verify workspace data persists. Inspect Cloud Logging for request/model/error evidence with no sensitive payloads. A public URL that only renders a static shell is not passing.

## Evidence artifacts

Create later:

- `evidence/test-summary.md`
- `evidence/ai-evaluation.md`
- `evidence/deployment.md`
- `evidence/accessibility.md`
- screenshots of actual working flows

Each includes UTC timestamp, Git SHA, dependency lock hashes, environment, commands, counts, failures/skips and limitations. Never mark a task complete using simulated test output.
