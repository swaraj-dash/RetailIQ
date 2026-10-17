# RetailIQ Documentation & Specifications Repository

RetailIQ joins grounded shopping, network inventory, fulfillment, demand planning, trend evidence, and catalog quality in one unified retail intelligence platform.

---

## 📑 Master Documentation Index

### 🎥 Demo, Presentation & Video Artifacts
* [**`TRANSCRIPT.md`**](TRANSCRIPT.md) — **Official 2m 50s Demo Video Script & Verbatim Voiceover Dialogue** (Timestamped 0:00–2:50, solo or 2-speaker roles).
* [**`DEMO_WALKTHROUGH.md`**](DEMO_WALKTHROUGH.md) — **Step-by-step Presenter Screen Actions & Click Guide** for recording the prototype walkthrough.
* [**`SUBMISSION_GUIDE.md`**](SUBMISSION_GUIDE.md) — **Competition Submission Checklist**, video hosting instructions, cloud deployment options, and rubric scoring.
* [**`PROPOSAL_DECK.md`**](PROPOSAL_DECK.md) — **10-Slide Pitch & Solution Presentation** formatted for PDF export.
* [**`SUBMISSION_PROPOSAL.md`**](SUBMISSION_PROPOSAL.md) — Full written proposal addressing problem statement, technical architecture, and commercial viability.

### 📐 Authoritative System Specifications
* [**`00_MASTER_PLAN`**](00_MASTER_PLAN) — Master plan, authority rules, and architecture charter.
* [**`01_COMPETITION_AND_PRODUCT_STRATEGY.md`**](01_COMPETITION_AND_PRODUCT_STRATEGY.md) — AI Builder Cup strategy, rubrics, and value proposition.
* [**`02_SYSTEM_ARCHITECTURE.md`**](02_SYSTEM_ARCHITECTURE.md) — High-level architecture, boundaries, and components.
* [**`03_DATABASE_AND_DATA_MODEL.md`**](03_DATABASE_AND_DATA_MODEL.md) — PostgreSQL data model, schemas, migrations, row locking, and ATP math.
* [**`04_API_AND_INTEGRATION_CONTRACTS.md`**](04_API_AND_INTEGRATION_CONTRACTS.md) — REST endpoints, OpenAPI schemas, and payload contracts.
* [**`05_AI_AND_AGENT_DESIGN.md`**](05_AI_AND_AGENT_DESIGN.md) — Google Gemini prompt templates, tool schemas, and grounding boundaries.
* [**`06_FORECASTING_AND_DECISION_ENGINE.md`**](06_FORECASTING_AND_DECISION_ENGINE.md) — 14-day baseline forecasting, trend filtering, and rebalancing solver.
* [**`07_UI_UX_DESIGN_SYSTEM.md`**](07_UI_UX_DESIGN_SYSTEM.md) — Tailwind styling, responsive 2-tier navigation, and component standards.
* [**`08_TESTING_AND_ACCEPTANCE.md`**](08_TESTING_AND_ACCEPTANCE.md) — Integration, unit, and browser Playwright verification tests.
* [**`09_GOOGLE_CLOUD_DEPLOYMENT.md`**](09_GOOGLE_CLOUD_DEPLOYMENT.md) — Google Cloud Run, Cloud SQL, Firebase Hosting, and secret management.
* [**`10_AGENT_TOOLING_AND_SKILLS.md`**](10_AGENT_TOOLING_AND_SKILLS.md) — Coding agent skills, tool calling specifications, and fallbacks.
* [**`11_IMPLEMENTATION_ROADMAP.md`**](11_IMPLEMENTATION_ROADMAP.md) — Phased rollout and completion status.
* [**`12_DEMO_AND_SUBMISSION.md`**](12_DEMO_AND_SUBMISSION.md) — Video criteria, submission constraints, and evaluation checklist.
* [**`13_SYNTHETIC_DATASET.md`**](13_SYNTHETIC_DATASET.md) — Canonical electronics dataset (VoltGo Pro, VoltGo Go, stores S1–S3).
* [**`14_SOURCES_AND_DEPENDENCIES.md`**](14_SOURCES_AND_DEPENDENCIES.md) — Dependency pins, security baselines, and package requirements.
* [**`15_VALIDATION_REPORT.md`**](15_VALIDATION_REPORT.md) — Pre-implementation audit and contract validation results.
* [**`PROTOTYPE.md`**](PROTOTYPE.md) — Prototype execution requirements and acceptance boundaries.
* [**`DECISIONS.md`**](DECISIONS.md) — Architecture decision records and trade-offs.
* [**`TASKS.md`**](TASKS.md) — Milestone task checklist.
* [**`AGENTS.md`**](AGENTS.md) — Agent behavioral guidelines and constraints.

---

## Fixed stack

React/TypeScript/Vite, Tailwind and shadcn/Radix; FastAPI/Pydantic/Python3.12; SQLAlchemy/Alembic/psycopg; PostgreSQL17; Gemini3.5Flash through Google GenAI SDK and the Google Cloud model API; Firebase Authentication/Hosting; Cloud Run; Cloud SQL; Artifact Registry; Cloud Build; Secret Manager. Pin matrix and resolution gate: [14_SOURCES_AND_DEPENDENCIES.md](14_SOURCES_AND_DEPENDENCIES.md).

## Future repository layout

| Path | Required implementation artifact |
|---|---|
| `AGENTS.md` | Root instructions, linked into retailiq-spec |
| `frontend/` | React SPA, package.json, package-lock.json, src, public |
| `backend/` | pyproject.toml, uv.lock, app, tests, Alembic, Dockerfile |
| `infra/compose.yaml` | Local PostgreSQL17 on 127.0.0.1:5432, healthcheck, volume; no real secrets |
| `infra/api-env.yaml` | Nonsecret production environment configuration |
| `infra/build-bucket-lifecycle.json` | 7-day build-object retention policy |
| `firebase.json` | Hosting SPA/static cache/security headers and local Auth emulator |
| `package.json` | Root Playwright/accessibility/OpenAPI generation tooling |
| `tests/e2e/` | Real browser acceptance scenarios |
| `evidence/` | Actual dependency/tool/test/deployment evidence after implementation |
| `retailiq-spec/` | This authoritative package |

## Prerequisites and local setup

Node24, Python3.12, uv, npm, PostgreSQL17 (Docker Compose or existing local instance), Firebase CLI for Auth emulator, Google Cloud access for live AI. Cloud deployment additionally requires billing/IAM and project-specific provider activation. No actual cloud access was provided in the specification phase.

After Phase2 creates the required files, from repository root:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
docker compose -f infra/compose.yaml up -d db
uv sync --project backend --frozen --all-groups
uv run --project backend alembic -c backend/alembic.ini upgrade head
uv run --project backend python -m app.cli seed --dataset retailiq-demo-v1
uv run --project backend python -m app.cli verify-seed
npm ci
npm --prefix frontend ci
firebase emulators:start --only auth --project demo-retailiq
```

In separate terminals:

```bash
uv run --project backend uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

CLI settings validate only the dependencies used by that command: bootstrap/seed need DB configuration, `probe-ai` needs model configuration, and `export-openapi` needs neither live service. The web server validates the full runtime configuration. Application settings load `backend/.env` explicitly only for local development; production config uses injected environment. Backend pyproject installs `app` as an editable package in development so `python -m app.cli` works from repo root. Alembic config resolves `script_location` relative to itself. Frontend default targets `http://127.0.0.1:8000/api/v1`. Docker Compose binds PostgreSQL only to localhost and uses separate disposable local development credentials; no cloud password is included in `.env.example`.

For live cloud AI locally, run `gcloud auth application-default login` in an authorized account and set a real `GOOGLE_CLOUD_PROJECT` for the model API. The Firebase emulator project remains `demo-retailiq`; do not confuse its token audience with the model project. Emulator tokens are accepted only in local mode.

## Environment variable reference

| Variable | Local / deployed value | Secret? |
|---|---|---|
| `APP_ENV` | local / production | No |
| `APP_VERSION` | dev / deployed git SHA | No |
| `DEMO_MODE` | true; false disables public demo creation | No |
| `DB_HOST` | `127.0.0.1` / `/cloudsql/project:region:instance` | No |
| `DB_PORT` | 5432; ignored for socket | No |
| `DB_NAME` | `retailiq` | No |
| `DB_USER` | local owner for migrations; `retailiq_app` at runtime | No |
| `DB_PASSWORD` | local credential / Secret Manager version | Yes |
| `APP_DB_PASSWORD` | bootstrap job only | Yes |
| `GOOGLE_CLOUD_PROJECT` | Authorized model/cloud project | No |
| `GOOGLE_CLOUD_LOCATION` | `global` | No |
| `GEMINI_PROVIDER` | `enterprise`; explicit fallback mode for offline tests | No |
| `GEMINI_MODEL` | `gemini-3.5-flash` | No |
| `FIREBASE_PROJECT_ID` | `demo-retailiq` locally; real project deployed | No |
| `FIREBASE_AUTH_EMULATOR_HOST` | `127.0.0.1:9099` local only; absent in production | No |
| `CORS_ORIGINS` | JSON array of exact frontend origins | No |
| `SCENARIO_DATE` | `2026-10-17`; seed/workspace default, never security clock | No |
| `PORT` | 8000 locally / injected 8080 on Cloud Run | No |
| `VITE_API_BASE_URL` | Backend URL with `/api/v1` | Public |
| `VITE_FIREBASE_API_KEY` | Firebase web config key; restrict appropriately | Public |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase web config | Public |
| `VITE_FIREBASE_PROJECT_ID` | Auth project | Public |
| `VITE_FIREBASE_APP_ID` | Registered web app ID | Public |
| `VITE_USE_AUTH_EMULATOR` | true locally; false deployed | Public |
| `VITE_AUTH_EMULATOR_URL` | `http://127.0.0.1:9099` locally; absent deployed | Public |

Settings for quota defaults in [05_AI_AND_AGENT_DESIGN.md](05_AI_AND_AGENT_DESIGN.md) are code/config constants initially; only operator-controlled environment overrides may change them. Reject unknown provider names or invalid origin JSON at startup. Production must reject emulator variables, missing secrets and local database hosts. Build SQLAlchemy URL with its structured URL API; don't concatenate/URL-escape passwords manually.

## CLI interfaces the coding agent must implement

| Command after `python -m app.cli` | Behavior |
|---|---|
| `bootstrap --seed-template` | Owner-only: create least-privilege app DB role from `APP_DB_PASSWORD`, migrate, seed template, verify; idempotent |
| `seed --dataset retailiq-demo-v1` | Seed read-only template in current DB; refuse overwrite of a different version without explicit new migration |
| `verify-seed` | Assert counts, ATP, signal facts and ledger; print dataset hash and exit 0/1 |
| `probe-ai` | One real structured-output call; validate shape; print provider/model/latency/result status without token/text |
| `evaluate-ai --dataset PATH --repeats 2` | Run fixed test prompts and write redacted evaluation evidence |
| `export-openapi --output PATH` | Export OpenAPI deterministically without DB mutation/model call |
| `cleanup --expired-demo-only` | Owner-only deletion of expired synthetic workspaces; never template/non-demo data |

No CLI reset command is exposed to public users. A new browser UID gets an isolated workspace through API03. E2E uses disposable DB fixtures. Pin script names so smaller agents do not improvise different setup/test commands.

## Build, test and deploy

```bash
uv run --project backend pytest backend/tests -m 'not ai_live' -q
uv run --project backend python -m app.cli export-openapi --output backend/openapi.json
npm run generate:api
npm --prefix frontend run typecheck
npm --prefix frontend run build
npx playwright test --project=chromium
```

Root `generate:api` invokes `openapi-typescript` on `backend/openapi.json` and writes `frontend/src/api/generated.ts`. Frontend scripts: `dev`=`vite`, `typecheck`=`tsc --noEmit`, `build`=`tsc --noEmit && vite build`. Root test config includes actual local servers or supplied public URLs. See [08_TESTING_AND_ACCEPTANCE.md](08_TESTING_AND_ACCEPTANCE.md) for nonoptional test details and [09_GOOGLE_CLOUD_DEPLOYMENT.md](09_GOOGLE_CLOUD_DEPLOYMENT.md) for complete deployment commands.

## Common issues

Auth401: check Firebase project/audience/emulator distinction. DB503: check PostgreSQL health, migration head, DB grants and socket path. No matches: inspect hard constraints and missing verified facts rather than adding invented facts. Stock409: refresh quote or proposal; don't disable locks. Gemini failure: show fallback, check model/global endpoint and IAM, billing/quota. Planning numbers differ from golden examples after shopping: expected because ATP changed; use a fresh fixture for golden tests. Broken deep links: Firebase SPA rewrite. CLI import failure: install backend package and use documented root paths.

Current status: Application fully implemented, 10/10 automated backend contract & golden tests passing (100%), React 18 frontend built and verified with 0 console errors, proposal PDF & interactive presentations created, and synthetic workspaces isolated. See [EVALUATION_HANDOFF.md](EVALUATION_HANDOFF.md) for full evaluation verification.
