# RetailIQ — Proposal & Technical Architecture Deck
## AI Builder Cup 2026 · Retail & Commerce Theme

> **Project Name:** RetailIQ  
> **Tagline:** Recover the purchase. Learn what to stock next.  
> **Theme:** Retail & Commerce — Intelligent Customer and Business Experiences  
> **Deployment Model:** Google Cloud Run / Firebase / Google Gemini API  
> **Repository:** https://github.com/swaraj-dash/RetailIQ.git  

---

## Slide 1: Executive Summary & The Retail Dilemma

### The Problem
Retailers lose billions annually to two opposing, destructive forces:
1. **Lost Sales from Stockouts:** Customers search for specific products with hard constraints (e.g., *"10,000 mAh USB-C power bank under ₹1,500, pickup today"*). When the preferred SKU is out of stock, standard e-commerce fails or shows irrelevant alternatives, causing immediate basket abandonment.
2. **Trapped Working Capital from Uncalibrated Replenishment:** Category managers respond by over-purchasing from external suppliers with high Minimum Order Quantities (MOQs) and long lead times, trapping working capital in excess stock while adjacent stores sit on identical surplus inventory.

### The RetailIQ Solution
RetailIQ bridges the gap between **shopper intent** and **store operations**. It interprets unstructured customer needs, finds verified factual substitutes with live Available-to-Promise (ATP) inventory, reserves shelf stock, and automatically calculates whether to satisfy future demand via **zero-capital inter-store rebalancing** or **supplier replenishment**.

---

## Slide 2: The End-to-End Decision Loop

RetailIQ is designed as a closed-loop system connecting the shopper's moment of intent to the store associate's physical workflow and the executive's inventory ledger:

```
[ Shopper Need (Natural Language) ]
               │
               ▼
[ Gemini Factual Extraction & Verification ] ──▶ Filters attributes without hallucinations
               │
               ▼
[ Live Database ATP Stock & Alternative ] ──▶ Identifies in-stock substitute across stores
               │
               ▼
[ 15-Minute Reservation Hold & Order ] ──▶ Row locks guarantee zero ghost inventory
               │
               ▼
[ Store Associate In-Store Fulfillment ] ──▶ On-hand drops (12 ➔ 11); creates audit event
               │
               ▼
[ Business Demand & Forecast Engine ] ──▶ Detects impending stockout at Indiranagar (S1)
               │
               ▼
[ Transfer vs Purchase Decision Engine ] ──▶ Evaluates S2 transfer (32 units) vs Supplier PO
               │
               ▼
[ Manager Approval & Physical Receipt ] ──▶ Stock conservation strictly preserved
```

---

## Slide 3: Shopper & Associate Experience

### Shopper Discovery
- **Natural Language Understanding:** Interprets messy shopper inputs into typed criteria: category, battery capacity, connector type, price ceiling, and fulfillment speed.
- **Transparent Stock Visibility:** When the preferred item (*VoltGo Pro RQ001*) is out of stock across the entire network, RetailIQ does not hide it or hallucinate stock. Instead, it presents the verified substitute (*VoltGo Go RQ002*), highlighting exact factual matches (10,000 mAh, 20W USB-C, ₹1,299 vs ₹1,499).
- **Authoritative Reservation:** 15-minute reservation hold backed by server timestamp TTL and transactional allocations.

### Associate Operations
- **Store-Level Fulfillment:** Pickups are fulfilled with one click, decrementing physical on-hand inventory while keeping ATP accurate.
- **Stock Conservation:** Multi-store transfers require two explicit physical milestones: **Dispatch** at donor store (decrementing donor on-hand) and **Receipt** at recipient store (incrementing recipient on-hand). No ghost units are created or lost.

---

## Slide 4: Deterministic Decision Engine & Financial Optimization

When Indiranagar (S1) approaches stockout on VoltGo Go, RetailIQ evaluates three mutually exclusive pathways:

| Criterion | Inter-Store Transfer (Recommended) | Vendor Purchase Order | No Action |
|---|---|---|---|
| **Source** | Store 2 (Koramangala Excess) | PowerTech Electronics | None |
| **Quantity** | **32 units** (Exact rebalance) | 36 units (Supplier MOQ) | 0 units |
| **Lead Time** | **1 day** (Arrives before stockout) | 5 days (Arrives after stockout) | Stockout on Day 2 |
| **Working Capital** | **₹0** (Zero new cash outlay) | **₹25,380** (Tied up cash) | ₹0 |
| **Freight / Logistics** | ₹200 local delivery | ₹450 vendor freight | ₹0 |
| **Avoided Lost Units** | **32 units** | 18 units | 0 units |
| **Net Contribution** | **+₹15,074.49** | +₹8,200.00 | **-₹15,074.49 (Lost)** |

### AI Restraint: The Trend-to-Stock Gate
- **High-Utility Spike (EXT01 - Solar Lantern):** High basket intent and emergency utility ➔ Safe 18-unit Purchase Order approved.
- **Viral Social Fad (EXT02 - Glow Clip):** High search volume but 0.4% checkout conversion ➔ **MONITOR ONLY (0 units ordered)**. Protects retailer from supplier MOQ trap.

---

## Slide 5: Meaningful Gemini & Google AI Integration

RetailIQ implements strict boundaries to ensure enterprise-grade safety:

1. **What Gemini Does:**
   - Interprets unstructured customer natural language into structured Pydantic schemas.
   - Extracts hard constraints (e.g., connector = USB-C, capacity ≥ 10,000 mAh).
   - Generates natural, grounded customer explanations backed by verified product facts.
2. **What Gemini Is NEVER Allowed to Do:**
   - Invent stock levels or available quantities.
   - Compute monetary amounts, margins, or prices.
   - Authorize purchase orders or transfer inventory without human sign-off.
   - Write directly to the database or financial ledgers.

---

## Slide 6: Production System Architecture

RetailIQ is architected for instant deployment and high availability on Google Cloud:

```
┌────────────────────────────────────────────────────────┐
│               Frontend (React 18 + Vite)                │
│    Tailwind CSS · Lucide Icons · Recharts · Radix UI   │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON
┌───────────────────────────▼────────────────────────────┐
│              Backend Service (FastAPI)                 │
│      Pydantic v2 Contracts · Dual-Engine Database      │
│  (PostgreSQL 17 / SQLite) · Google GenAI Python SDK   │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
┌──────────────▼──────────────┐  ┌────────▼──────────────┐
│  Transactional DB & Ledger  │  │ Google Gemini 3.5 API │
│  Row-Locked ATP Balances    │  │ Grounded Intent & AEO │
└─────────────────────────────┘  └───────────────────────┘
```

- **Hosting & Compute:** Google Cloud Run (Containerized backend & static assets).
- **Dual-Engine DB Support:** Seamless local execution on SQLite with zero cloud dependencies, upgrading directly to PostgreSQL 17 via `DATABASE_URL` environment variable.

---

## Slide 7: Verification & Test Evidence

RetailIQ was rigorously validated against 7 comprehensive golden scenarios:

| Test Name | Validated Behavior | Result |
|---|---|---|
| `test_health_endpoints` | Health liveness & readiness check with database verification | **PASS** |
| `test_seed_counts` | 24 SKUs, 4 locations, 96 balances, 72 policies, 4,032 sales | **PASS** |
| `test_s01_and_s02_shopping` | VoltGo Pro unavailable (ATP 0); VoltGo Go verified match | **PASS** |
| `test_s03_transaction_loop` | Hold TTL ➔ Order ➔ Pickup fulfillment (On-hand 12 ➔ 11) | **PASS** |
| `test_s06_planning_decision` | S2 transfer 32 units approved; margin > ₹14k; ₹0 working capital | **PASS** |
| `test_s07_s08_trend_restraint` | ACT on solar lantern (PO 18); MONITOR on glow clip (Qty 0) | **PASS** |
| `test_s09_catalog_audit` | C01/C02 patch approval increases audit score from 75 to 88 | **PASS** |

**Overall Backend & Frontend Test Status:** 7/7 Backend Tests Passed (100%), 0 TypeScript / Lint / Build Errors.

---

## Slide 8: Scalability, Pilot Plan & Project Links

### Deployment & Scalability Path
- **Phase 1 (Prototype - Current):** Single isolated synthetic demo workspace, 24 benchmark SKUs, 4 multi-store nodes, 100% deterministic reproducibility.
- **Phase 2 (Enterprise Pilot):** Connect to retailer ERP/WMS via webhook adapters; multi-tenant workspace isolation via PostgreSQL schema partitions.
- **Phase 3 (Omnichannel Autonomous Rebalancing):** Multi-echelon inventory routing across regional distribution centers and 500+ physical storefronts.

### Repository & Links
- **GitHub Repository:** https://github.com/swaraj-dash/RetailIQ.git
- **Core Developers:** RetailIQ AI Builder Cup Team
