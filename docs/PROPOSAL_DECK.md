# RetailIQ — Proposal Deck
### Intelligent Customer & Business Experiences for AI Builder Cup 2026
**Theme:** Retail & Commerce  
**Team:** RetailIQ  
**Target Submission:** 18 October 2026  

---

## Slide 1: Cover & Executive Summary

# RetailIQ
### Recover the Purchase. Learn What to Stock Next.
**An Intelligent, Closed-Loop Commerce Engine Powered by Google Gemini & Deterministic Inventory Math**

* **Category:** Retail & Commerce (AI Builder Cup 2026)
* **Core Problem:** 4.2% of retail sales are permanently lost when items are out of stock; merchandising teams overreact with ungrounded supplier orders, tying up working capital.
* **Our Solution:** A closed loop connecting Shoppers (semantic discovery & fact-grounded substitutes), Store Associates (instant pickup & atomic stock decrements), and Business Managers (explainable transfer-vs-purchase rebalancing with AI restraint).

---

## Slide 2: The Core Problem in Modern Retail

### The ₹35 Lakh Problem: Stockouts & Overbuying

1. **Shopper Frustration & Lost Revenue:**
   * When a customer searches for a specific product and finds it out of stock, 72% abandon the purchase rather than browsing alternatives manually.
2. **The Reactive Merchandiser Trap:**
   * Traditional ERP systems respond to stockouts by firing expensive purchase orders to external suppliers (14-day lead times, high Minimum Order Quantities).
3. **The AI Hallucination Danger:**
   * Generative models cannot be trusted with inventory balances or financial transactions. A single hallucinated unit or price destroys customer trust and breaks audits.

---

## Slide 3: The RetailIQ Solution Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE CLOSED-LOOP ENGINE                      │
└─────────────────────────────────────────────────────────────────┘
   [ 1. Shopper Need ]  ──►  [ 2. Gemini Fact Extraction ]
                                    │
                                    ▼
   [ 4. 15-Min Row Lock ] ◄──  [ 3. Deterministic ATP Check ]
            │                     (Out of stock? Suggest verified
            │                      in-stock alternative)
            ▼
   [ 5. Store Pickup ]  ──►  [ 6. Atomic Inventory Decrement ]
                                    │
                                    ▼
   [ 8. Multi-Store Balance ] ◄── [ 7. Transfer vs Purchase Engine ]
      (Approve ₹1,360 Transfer        (Saves ₹34,640 vs ₹36,000 PO)
       arriving tomorrow)
```

---

## Slide 4: Where Google Gemini Delivers Real Value

* **Zero Hallucination Boundary:**
  * Gemini interprets fuzzy natural language and extracts typed requirements (battery capacity, port types, price ceilings).
  * Gemini provides conversational, human explanations grounded strictly in retrieved catalog facts.
* **Deterministic Boundary:**
  * Available-to-Promise (ATP) calculations, row locks, transfer cost-benefit comparisons, and ledger balances are 100% mathematical and enforced by PostgreSQL transactions.
  * Gemini **never** invents stock, never writes financial amounts, and never approves orders autonomously.

---

## Slide 5: The Four Operational Perspectives

1. **Shopper View:**
   * Conversational natural language query: *"10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today"*.
   * Factual side-by-side comparison between out-of-stock preference (VoltGo Pro) and verified alternative (VoltGo Go).
   * Live 15-minute reservation timer backed by database row locking.
2. **Store Associate Operations:**
   * Real-time pickup queue with atomic inventory decrement on handover (`on_hand: 12 → 11`).
   * Inter-store transfer dispatch and receipt dock management.
3. **Business Intelligence & Replenishment:**
   * 14-day baseline demand forecasting.
   * Transfer vs. Purchase mathematical tradeoff (Lead time, holding cost, stockout risk).
   * Human-in-the-loop one-click approval.
4. **Trace & Audit Ledger:**
   * Cryptographic event stream verifying every state transition, model invocation, and stock movement.

---

## Slide 6: Genuine AI Restraint in Demand Intelligence

RetailIQ does not blindly amplify external hype:
* **Validated Search Lift (Solar Lanterns):**
  * External query volume surged +210%.
  * Local store traffic confirmed 60 in-store inquiries.
  * **Action:** Lift is capped at a conservative +25% safety ceiling, approving a measured 36-unit purchase order.
* **Social Media Viral Fad (Selfie Rings):**
  * Social media video trend spiked +420%.
  * Local basket conversion: 0%. Source reliability: 28%.
  * **AI Restraint Applied:** Flagged as a short-lived viral fad. Rebalancing rejected; prevents locking ₹1.2 Lakh in dead stock.

---

## Slide 7: Technical Architecture

* **Frontend:** React 18, TypeScript, Vite, Tailwind CSS (Mobile-first, responsive, zero clutter).
* **Backend:** FastAPI (Python 3.12), SQLAlchemy, Pydantic v2 contracts.
* **Database:** PostgreSQL with row-level locks (`SELECT FOR UPDATE`), UUID primary keys, and immutable event streams.
* **AI Engine:** Google Gemini 1.5 Flash via official `@google/genai` / `google-genai` SDK with typed JSON schemas.
* **Cloud Infrastructure:**
  * API: Google Cloud Run (Containerized, auto-scaling, stateless).
  * Frontend: Firebase Hosting (Global edge CDN).
  * Data: Cloud SQL for PostgreSQL.

---

## Slide 8: Business Impact & Pilot Hypotheses

| Metric | Industry Baseline | RetailIQ Projected Impact |
|---|---|---|
| **Lost Sale Recovery** | 0% (Walkaway) | **22%** recovered via verified instant alternatives |
| **Stockout Prevention** | Reactive PO (14-day lead) | **1-day** inter-store transfer resolution |
| **Working Capital Saved** | High safety buffer | **₹34,640** saved per rebalancing decision |
| **Catalog Completeness** | 68% manual accuracy | **96%** AEO-compliant catalog specs |
| **Inventory Discrepancy** | Unaudited manual entries | **0** discrepancies (atomic row-locked mutations) |

---

## Slide 9: Scalability Roadmap

* **Phase 1 (Prototype / Current):**
  * Single-city multi-node network (3 stores + 1 DC), deterministic golden scenarios, Gemini intent extraction and explainability.
* **Phase 2 (Enterprise Pilot - 90 Days):**
  * Direct integration with Shopify / Magento APIs, POS receipt webhooks, and multi-tenant PostgreSQL schema isolation.
* **Phase 3 (Nationwide Network):**
  * Multi-region Cloud Run deployment, BigQuery forecasting ingestion, and automated supplier EDI connectors.

---

## Slide 10: Summary & Submission Links

* **Public Repository:** https://github.com/swaraj-dash/RetailIQ.git
* **Prototype Demo URL:** http://127.0.0.1:8000 / Deployed Cloud Run URL
* **Video Demo (YouTube):** [Included in Submission Portal]
* **Key Differentiator:** The only retail AI engine combining **Google Gemini semantic intelligence** with **zero-hallucination deterministic inventory integrity**.
