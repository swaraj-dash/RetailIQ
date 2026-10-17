# RetailIQ — Autonomous Retail Intelligence Platform
### AI Builder Cup 2026 Prototype Submission · Retail & Commerce Theme

> **"Recover the purchase. Learn what to stock next."**

RetailIQ solves retail's most painful dilemma: **lost sales from out-of-stock items** coupled with **trapped working capital from uncalibrated replenishment**.

---

## 🚀 Key Highlights & Differentiators

1. **Closed-Loop Intelligence:**
   - **Shopper Intent:** Natural-language search with Gemini extracts hard factual constraints (e.g. 10,000 mAh, USB-C, <₹1,500, pickup today).
   - **Verified Fact Grounding:** Preferred SKU out of stock (*VoltGo Pro*) ➔ Instantly recommends verified in-stock substitute (*VoltGo Go*).
   - **Authoritative Database ATP:** Available-to-Promise is computed strictly from ledger balances (`on_hand - blocked - holds - orders - transfers_out`). Zero hallucinations.
   - **Transactional Order Conversion:** 15-minute reservation hold backed by server TTL and database row locks ➔ Demo pickup order placed.
   - **Physical Store Handover:** Associate fulfills pickup ➔ On-hand inventory decrements from 12 to 11 units in real time.
   - **Deterministic Planning Optimization:** S1 impending stockout triggers automated comparison:
     - **Inter-Store Transfer from S2:** 32 units excess, 1-day lead time, ₹0 working capital, **+₹15,074 net margin**.
     - **Supplier Purchase Order:** 36 units MOQ, 5-day lead time, **₹25,380 tied up capital**.
   - **Mandatory Human Approval Gate:** Manager reviews and approves the transfer ➔ Dispatched from S2 ➔ Received at S1 with 100% mathematical stock conservation.
   - **AI Restraint:** High-utility search spike (Solar Lantern) triggers safe PO; viral social media fad (Glow Clip) is dampened to **MONITOR ONLY** with 0 units ordered.

---

## 🛠️ System Architecture

- **Frontend:** React 18, TypeScript, Vite 5, Tailwind CSS, Lucide Icons, Recharts, Radix UI primitives.
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 (dual-engine PostgreSQL 17 / SQLite).
- **AI Integration:** Google GenAI SDK (Gemini 3.5 Flash) with deterministic grounded fallback.
- **Audit & Security:** Immutable cryptographic event trace for all stock movements and state changes.

---

## ⚡ Quick Start: Running Locally

### Prerequisites
- Python 3.12+
- Node.js 20+

### Option A: Run Both Together (Unified Server)
The frontend is already built into `frontend/dist`. FastAPI serves both the REST API and the React SPA on a single port:

```bash
# In backend directory
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser at **http://localhost:8000** to explore the complete application!

---

### Option B: Run in Development Mode (Vite Hot-Reload)

**1. Start Backend:**
```bash
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**2. Start Frontend Dev Server:**
```bash
cd frontend
npm run dev
```
Open **http://localhost:3000** (Vite proxies all API requests to port 8000).

---

## 🧪 Running the Verification Test Suite

The test suite validates all core golden scenarios and browser contracts against a fresh database:

```bash
cd backend
.\.venv\Scripts\python.exe -m pytest -v
```

**Test Verification Summary:**
```
tests/test_frontend_api_contract.py::test_frontend_full_browser_contract PASSED [ 10%]
tests/test_golden_scenarios.py::test_health_endpoints PASSED             [ 20%]
tests/test_golden_scenarios.py::test_seed_counts PASSED                  [ 30%]
tests/test_golden_scenarios.py::test_s01_and_s02_grounded_shopping_and_substitute PASSED [ 40%]
tests/test_golden_scenarios.py::test_s03_feasible_transaction_loop PASSED [ 50%]
tests/test_golden_scenarios.py::test_s06_planning_transfer_vs_purchase PASSED [ 60%]
tests/test_golden_scenarios.py::test_s07_and_s08_trend_action_and_monitor PASSED [ 70%]
tests/test_golden_scenarios.py::test_s09_catalog_audit_and_patch PASSED  [ 80%]
tests/test_golden_scenarios.py::test_idempotency_order_placement PASSED  [ 90%]
tests/test_golden_scenarios.py::test_demo_reset_and_product_image_categories PASSED [100%]
======================= 10 passed in 12.24s =======================
```

---

## 🤖 Gemini AI & Cloud Configuration

RetailIQ features a multi-tiered Gemini Gateway (`backend/app/services/ai.py`):
- **Model:** `gemini-2.5-flash` (production-ready multimodal model).
- **Authentication:** Dual-mode authentication supporting either `GEMINI_API_KEY` or Google Cloud Application Default Credentials (Vertex AI Enterprise ADC).
- **Graceful Deterministic Fallback:** When credentials are not supplied, all 5 AI operations (intent extraction, catalog patching, decision explanations, trend signal classification, and device compatibility evaluation) seamlessly transition to deterministic fallback with clear `FALLBACK` / `LIVE` operational badging.
- **Demo State Reset:** Evaluators can reset the demo workspace back to pristine canonical state (12 units at S1) at any time via `POST /api/v1/demo/reset`.

---

## ☁️ Google Cloud Deployment (Cloud Run)

RetailIQ includes a production multi-stage `Dockerfile`:

```bash
# Build and deploy directly to Google Cloud Run
gcloud run deploy retailiq-prototype \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars DEMO_MODE=True,SCENARIO_DATE=2026-10-17,GEMINI_API_KEY=$GEMINI_API_KEY
```

---

## 📁 Repository Structure

```
RetailIQ/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints (shopping, orders, inventory, planning, catalog)
│   │   ├── models/          # 32 relational entities (SQLAlchemy)
│   │   ├── schemas/         # Typed Pydantic request/response contracts
│   │   ├── services/        # ATP row locks, planning engine, Gemini adapter, seed generator
│   │   └── main.py          # FastAPI application entry & static bundle mounting
│   ├── tests/               # Golden scenario & API contract test suite (10/10 passing)
│   ├── pytest.ini           # Pytest configuration
│   └── requirements.txt     # Pinned Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/             # Typed TypeScript API client matching backend contracts
│   │   ├── components/      # Accessible UI components (AppHeader, Cards, Modals, Badges)
│   │   └── features/        # Shopper, Associate, Business Manager, and Trace perspectives
│   ├── package.json         # Pinned frontend dependencies
│   └── tailwind.config.js   # UI/UX design tokens
├── docs/                    # Complete specifications, proposals, presentations, and guides
│   ├── architecture/        # High-res workflow diagrams (Shopper, Associate, Rebalance, AI Restraint)
│   ├── 00_MASTER_PLAN to 15_VALIDATION_REPORT.md  # 20 Master System Specifications
│   ├── RetailIQ_Proposal_Deck.pdf & .pptx         # Official 16:9 Proposal Deck
│   ├── RetailIQ_Proposal_Deck.html                # Interactive Proposal Slide Deck
│   ├── RetailIQ_Architecture_and_Workflows_Presentation.html # Master Archify visualizer
│   ├── EVALUATION_HANDOFF.md # Independent Evaluator Verification Guide
│   ├── DEMO_WALKTHROUGH.md   # Step-by-step Presenter Screen Actions
│   ├── TRANSCRIPT.md         # Official 2m 50s Demo Video Script & Voiceover
│   ├── DECISIONS.md          # Architecture Decision Records (ADR01–ADR21)
│   └── TASKS.md              # Implementation task tracking ledger
├── Dockerfile               # Multi-stage Cloud Run container
├── AGENTS.md                # Agent instruction charter
└── README.md                # Repository entry point & overview
```

---

## 🏆 Submission Documents for AI Builder Cup 2026
- **Official Competition Proposal Deck (PDF):** [`docs/RetailIQ_Proposal_Deck.pdf`](docs/RetailIQ_Proposal_Deck.pdf)
- **Official Competition Proposal Deck (PowerPoint PPTX):** [`docs/RetailIQ_Proposal_Deck.pptx`](docs/RetailIQ_Proposal_Deck.pptx)
- **Interactive Proposal Slide Deck (HTML):** View at [`/proposal`](http://127.0.0.1:8000/proposal) or open [`docs/RetailIQ_Proposal_Deck.html`](docs/RetailIQ_Proposal_Deck.html)
- **Interactive Architecture & Workflows Presentation (Archify):** View at [`/presentation`](http://127.0.0.1:8000/presentation) or open [`docs/RetailIQ_Architecture_and_Workflows_Presentation.html`](docs/RetailIQ_Architecture_and_Workflows_Presentation.html)
- **Complete Documentation Hub:** See [`docs/README.md`](docs/README.md)
- **Official Demo Video Transcript (2:50):** See [`docs/TRANSCRIPT.md`](docs/TRANSCRIPT.md)
- **Demo Presenter Walkthrough Guide:** See [`docs/DEMO_WALKTHROUGH.md`](docs/DEMO_WALKTHROUGH.md)
- **Independent Evaluator Verification Guide:** See [`docs/EVALUATION_HANDOFF.md`](docs/EVALUATION_HANDOFF.md)
- **Architecture Decisions Record (ADR01–ADR21):** See [`docs/DECISIONS.md`](docs/DECISIONS.md)
- **Implementation & Acceptance Task Ledger:** See [`docs/TASKS.md`](docs/TASKS.md)
- **Portal Submission Checklist & Cloud Hosting:** See [`docs/SUBMISSION_GUIDE.md`](docs/SUBMISSION_GUIDE.md)
- **Comprehensive Written Proposal:** See [`docs/SUBMISSION_PROPOSAL.md`](docs/SUBMISSION_PROPOSAL.md)
- **Master Technical Specifications (20 Specs):** Located in [`docs/`](docs/)
