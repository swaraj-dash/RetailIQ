# RetailIQ — Prototype Build Brief for AI Builder Cup 2026

**Purpose:** Instructions for the coding agent. Build a compelling, functional prototype—not the entire RetailIQ platform. Preserve the long-term product architecture, but optimize this phase for a reliable end-to-end proof that can be deployed, recorded and submitted.

**Status:** Prototype scope only. This document is not evidence that implementation, deployment, model access, eligibility or submission has succeeded.

## 1. Competition requirements

The official AI Builder Cup 2026 pages describe a **working prototype**, not just a pitch deck or UI mockup. The submission must:

1. Address **Retail & Commerce: Intelligent Customer and Business Experiences**.
2. Meaningfully use a Google AI model such as Gemini/Gemma, or an eligible Google agentic platform.
3. Be deployed on Google Cloud using **Cloud Run or Firebase**.
4. Include a clear proposal deck exported to **PDF**.
5. Include a public **3-minute** YouTube/Vimeo video or public Google Drive video link showing the AI creation working.
6. Use English for code, documentation and submission materials.
7. Demonstrate a functional, user-friendly solution with a credible path to scalability.

Official sources:
- Themes and submission requirements: https://aibuildercup.com/themes.html
- Main page, timeline and eligibility: https://aibuildercup.com/
- Organizer contact: support+aibuildercup@hack2skill.com

The public site lists the prototype submission deadline as **18 October 2026** and says registration is closed. It also states this edition is for working professionals and students are ineligible. The team lead must immediately verify registration, cutoff/timezone, portal fields and eligibility. Do not represent eligibility as confirmed. If eligibility or registration is uncertain, contact the organizer; building a prototype does not make a team eligible.

The theme page contains a stale/inconsistent “Category Specification” paragraph referring to unrelated categories. Use the actual Retail & Commerce theme and verify the private registered-team portal for the category field before submitting.

## 2. Product thesis

**RetailIQ helps retailers recover sales lost because the right product is unavailable, while protecting working capital from poorly justified replenishment.**

The differentiating loop is:

**Shopper need → verified product facts and availability → stock-aware alternative or quote → real demo transaction → demand/stock intelligence → explainable transfer or purchasing decision → measurable simulated outcome.**

Do not make every planned module equally complete. Demonstrate this loop convincingly with a small number of screens, real API calls, a real database, meaningful Gemini use, deterministic business logic and transparent synthetic-data labels.

## 3. Prototype definition: build now

Build one polished, responsive web app for one fictional/synthetic retailer, with a single isolated demo workspace and three connected perspectives:

- **Shopper:** express a need in natural language, see fact-grounded product matches and alternatives, check stock, quote/reserve and complete a demo pickup order.
- **Associate:** fulfill the demo order and review a recommended inter-store transfer with dispatch/receive actions.
- **Business manager:** inspect resulting stock and the decision trace, compare transfer versus purchase, and review a simple forecast/stockout or trend signal.

All perspectives must share the same backend, inventory state and audit/decision trace. Shared state is more valuable than many disconnected screens.

### Required end-to-end story

Use the deterministic synthetic dataset and golden scenario. Follow `12_DEMO_AND_SUBMISSION.md`; do not invent a conflicting demo.

1. Start in a fresh isolated demo workspace and show the synthetic-data label.
2. Ask for a **10,000 mAh USB-C power bank under ₹1,500, for travel, pickup today**, with a preference for VoltGo Pro.
3. Show the preferred SKU is unavailable, then show the verified available alternative with correct capacity, connector and output facts. Explain why the preferred item is unavailable and why the alternative matches.
4. Create a quote/hold and place a demo pickup order through actual backend endpoints. Show the order ID and allocation. Do not present a mock response as a completed transaction.
5. Fulfill pickup in the associate view. Show inventory decrement and linked event/decision trace.
6. Open the manager's stock proposal for the same SKU. Compare transfer versus purchase using deterministic calculations: lead time, stockout risk, expected lost units, holding/working-capital impact and estimated contribution. Show assumptions.
7. Approve, dispatch and receive a demo transfer. These actions must mutate the database through real endpoints, enforce stock conservation and be idempotent.
8. Refresh the proposal and show it recalculated against changed stock. Do not replay a stale recommendation or fake an unchanged result.
9. Show one demand/trend insight and one catalog audit/patch preview if stable. Keep them secondary to the main loop.
10. End with the actual deployment URL, a concise limitations note and a planned pilot path.

If time is tight, finish the main loop and real test/deployment gates first. Do not sacrifice stock correctness, real Gemini use, security boundaries or public deployment for extra dashboards.

## 4. Must-have functionality

### A. Shopper
- Natural-language need extraction using Gemini with a typed/validated output schema.
- Deterministic catalog filtering and verified-attribute comparison.
- Network/store availability derived from database-backed ATP, not Gemini.
- A fact-backed alternative with explicit differences and recommendation rationale.
- Quote/hold/order/pickup path using real backend endpoints and persistent storage.
- Loading, empty, validation, error and success states.
- Clear labels for synthetic retailer data and demo transactions.

### B. Associate and stock movement
- Order lookup and fulfillment state.
- Source/destination stock visibility.
- Transfer proposal with source/destination quantities.
- Human approval, dispatch and receipt as distinct states.
- Stock ledger/event trace explaining what changed and why.
- Concurrency/idempotency protection; no negative stock or double receipt.

### C. Business intelligence
- Current stock, ATP, shortfall/target, forecast baseline/range and assumptions.
- Deterministic transfer-versus-purchase comparison.
- Stockout/excess or trend insight with a clear “monitor/no action” option.
- Decision snapshot with freshness/version; reject stale approvals.
- Separate observed synthetic demo transactions from counterfactual estimates.

### D. Meaningful Gemini use
Gemini must do visible, real work: interpret shopper intent into a validated structured request, or provide a grounded explanation using retrieved facts and bounded read-only tools. Demonstrate both if reliable.

Gemini must **not**:
- Invent product facts, availability, stock, prices, lead times or calculations.
- Write inventory or money values.
- Approve, dispatch, receive or place an order without explicit user action.
- Bypass tenant isolation or tool argument validation.
- Be described as live if a fixture/fallback was used.

Deterministic services remain authoritative for filters, ATP, forecast arithmetic, financial calculations, permissions and mutations. If Gemini is unavailable, use a clearly labeled development fallback; the final recording must accurately state whether the real Google model call worked.

## 5. Explicitly defer in this phase

Do **not** complete the entire roadmap before demonstrating the prototype. Unless required for the core story, defer:

- Full omnichannel commerce, multi-item cart, taxes, payment processing and real courier integrations.
- Real suppliers, live purchase orders, live WMS and external retailer integrations.
- Production-grade forecasting across many seasons/SKUs; no neural forecasting required.
- Broad merchant/social/Google Trends ingestion. Access may be unavailable; use the labeled synthetic signal dataset.
- Private assistant prompt analytics, guaranteed AEO/GEO ranking gains or claims of improved AI search ranking.
- Full returns/reverse-logistics suite.
- Multiple autonomous agents or an elaborate agent framework.
- Enterprise onboarding, SSO, extensive role administration and compliance certifications.
- Decorative dashboards that do not use working APIs.

Keep the future capabilities in the specifications and mark them **not implemented in prototype**. A narrower working prototype is acceptable when its limitations and expansion plan are honest.

## 6. Architecture constraints

Read the authoritative files, especially `00_MASTER_PLAN.md`, `02_SYSTEM_ARCHITECTURE.md`, `03_DATABASE_AND_DATA_MODEL.md`, `04_API_AND_INTEGRATION_CONTRACTS.md`, `05_AI_AND_AGENT_DESIGN.md`, `06_FORECASTING_AND_DECISION_ENGINE.md`, `07_UI_UX_DESIGN_SYSTEM.md`, `08_TESTING_AND_ACCEPTANCE.md`, `09_GOOGLE_CLOUD_DEPLOYMENT.md`, `10_AGENT_TOOLING_AND_SKILLS.md`, `11_IMPLEMENTATION_ROADMAP.md`, `12_DEMO_AND_SUBMISSION.md`, `13_SYNTHETIC_DATASET.md`, `14_SOURCES_AND_DEPENDENCIES.md`, `15_VALIDATION_REPORT.md`, `TASKS.md`, `DECISIONS.md` and `AGENTS.md`.

Do not silently replace the chosen architecture:
- React + TypeScript + Vite SPA.
- FastAPI backend.
- PostgreSQL as transactional system of record.
- Current supported Google GenAI SDK and a verified Gemini model.
- Firebase Hosting for the frontend and Cloud Run for the API.
- Controlled, isolated synthetic demo workspace.

A prototype may contain fewer features, but it must not have fake architecture: no frontend-only inventory mutations, hard-coded success messages, in-memory-only order flow presented as persistent, or fixture responses presented as live model output.

Use the exact synthetic seed data and scenario values. Do not change golden values to make a test pass. Keep source provenance and synthetic labels visible.

## 7. Prioritized execution plan

### P0 — Confirm access and submission constraints
- Verify team registration, eligibility, portal cutoff/timezone and required fields.
- Inspect repository, Antigravity version/rules, installed tools and lockfiles.
- Confirm Google Cloud project, billing/IAM permissions, model entitlement/quota and allowed region.
- Run a tiny real Gemini structured-output probe.
- Deploy a minimal health endpoint to Cloud Run and a minimal frontend to Firebase Hosting early.
- Record blockers and owners; never print secrets.

### P1 — Build one vertical slice locally
- Resolve dependency versions and create lockfiles; run install/import/build smoke tests.
- Implement schema/migrations, deterministic seed and health/readiness endpoints.
- Implement catalog/facts/ATP reads and typed OpenAPI contract.
- Implement idempotent quote/hold/order/fulfillment.
- Integrate Gemini intent extraction and grounded explanation with deterministic fallback.
- Build shopper journey and real API calls.
- Test stock, concurrency, authorization, stale data and errors before adding screens.

### P2 — Connect the business decision loop
- Implement transfer-versus-purchase calculations using documented golden values.
- Add proposal snapshot/versioning, explicit approval, dispatch and receipt.
- Ensure inventory is conserved and receipts are idempotent.
- Build associate and manager screens reading/mutating the same backend state.
- Add one trend/forecast insight and one catalog audit preview only after the main flow passes.

### P3 — Verify and deploy
- Run backend unit/integration tests against real PostgreSQL.
- Run browser end-to-end tests against the deployed app, including a fresh workspace.
- Verify the public app in a logged-out/clean browser; verify health/readiness and API calls.
- Record actual frontend URL, Cloud Run URL, deployed revision/image identifier, commit, test results and limitations.
- Inspect billing before creating paid resources. Budget alerts are not hard spending caps.
- Do not claim zero cost or successful deployment until verified.

### P4 — Submission assets
- Create a professional proposal deck and export it to PDF. It must describe the version actually deployed.
- Record a **public 3-minute** video showing the real running app. Target about 2:50 to leave a margin.
- Show the real Google model call, backend-backed transaction, stock decision, test/deployment evidence and limitations.
- Prepare a public code repository/README if required by the private portal. Never publish credentials or personal account details.
- Verify links logged out/incognito and check the final submission preview. Submission itself requires authorized team action; never claim submitted without receipt/evidence.

## 8. Acceptance gates — no skipping

The prototype is not done because the UI looks finished. Mark every gate PASS, FAIL, BLOCKED or NOT RUN with evidence.

| Gate | Required evidence |
|---|---|
| G1 — Build | Clean dependency install from lockfiles; frontend production build and backend imports pass |
| G2 — Seed | Counts match `13_SYNTHETIC_DATASET.md`; deterministic golden values match |
| G3 — Shopper | Need → verified product/alternative → quote/hold → order → pickup works in browser |
| G4 — Inventory | ATP, allocations and stock ledger reconcile before/after each action |
| G5 — Decision | Transfer/purchase comparison matches documented calculations; assumptions visible |
| G6 — Movement | Approve/dispatch/receive changes DB state, conserves stock and is idempotent |
| G7 — Gemini | Evidence of real Google model call; validated schema; fallback disclosed |
| G8 — Security | Separate demo identities/workspaces cannot access each other's rows; no secrets exposed |
| G9 — UX | Responsive layout, keyboard basics, loading/error/empty/success states; no dead controls |
| G10 — Tests | API/database tests and deployed browser E2E run; failures/skips documented |
| G11 — Deployment | Public frontend/API health work; persistent database confirmed; clean-browser smoke passes |
| G12 — Submission | PDF, public three-minute video, URLs and portal receipt/preview verified as applicable |

A blocked gate remains blocked. Do not change it to PASS because a fallback exists.

## 9. Three-minute video plan

Target duration: approximately **2:50**.

- **0:00–0:15 — Problem:** Retailers lose sales when preferred items are unavailable; buying more is not always the best response.
- **0:15–0:55 — Shopper:** Enter the need, show preferred item unavailable, verified alternative, facts and database-backed quote/order.
- **0:55–1:25 — Operations:** Fulfill pickup; show inventory and trace update.
- **1:25–2:05 — Intelligence:** Compare transfer versus purchase; show lead time, stockout risk, working capital and explicit approval/receipt.
- **2:05–2:30 — Connected intelligence:** Show one grounded trend/forecast or catalog audit preview with synthetic-data provenance.
- **2:30–2:50 — Credibility:** Show deployment, meaningful Gemini use, one test result, limitations and next pilot step.

Record the actual app. Do not splice mock responses into a segment claiming live functionality. Keep the synthetic-data label visible. Do not claim the demo proves actual retailer revenue impact.

## 10. Proposal PDF outline

Do not submit this Markdown file as the proposal PDF.

1. RetailIQ and the retail availability/working-capital problem.
2. Why isolated tools miss the connected shopper-to-stock loop.
3. End-to-end experience and intended users.
4. Architecture and the role of Gemini versus deterministic services.
5. Demonstrated prototype flow and evidence.
6. Explainability, safety, data provenance and human approval.
7. Impact hypotheses and how a pilot would measure them; label estimates as hypotheses.
8. Scalability, rollout stages, integration plan and roadmap.
9. Limitations, synthetic dataset and unimplemented capabilities.
10. Team and public demo/repository links, as required by the portal.

## 11. UX and demo quality bar

- First screen explains the product in one sentence.
- Clear typography, restrained color, consistent spacing and strong hierarchy.
- One excellent shopper flow and a linked manager view beat a generic dashboard.
- Persistent but unobtrusive “Synthetic demo data” label.
- Use “Estimated contribution opportunity,” not “guaranteed revenue.”
- Show assumptions, units, timestamps/version, source and recommendation rationale.
- Distinguish observed demo transactions from forecast/counterfactual values.
- Include empty/error/loading states; no dead buttons or hidden interactions.
- Keep chart labels readable and do not imply precision beyond the data.

## 12. Required agent handoff report

Update `TASKS.md`, `DECISIONS.md` and the validation report. Provide:
- Implemented files, routes and screens.
- What passed, failed, was blocked or was not run, with test/command evidence.
- Actual public frontend/API URLs and deployment revision/hash, if genuinely deployed.
- Proof of the Gemini model used and whether fallback was invoked.
- Seed counts and golden scenario checks.
- Known limitations and deferred scope.
- PDF/video/repository links and portal submission evidence, where authorized.
- Remaining risks, owners and next actions.

Separate **implemented**, **tested**, **deployed**, **simulated** and **not implemented**. Never report completion without evidence.

## 13. Definition of success for this phase

A small, polished, real and deployed end-to-end proof is more valuable than a broad unfinished platform. The minimum compelling prototype is:

**Real Gemini intent interpretation + verified catalog/ATP + working order/pickup + deterministic transfer-versus-purchase decision + human-approved inventory movement + public Google Cloud deployment + proposal PDF + public three-minute demo.**

If the deadline makes this scope impossible, prioritize the shopper-to-order flow, connected stock decision, real model use and verified deployment. Disclose unfinished items rather than simulating them as complete.
