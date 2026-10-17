# RetailIQ — Final Video Demo Recording Flow & Word-for-Word Transcript
## AI Builder Cup 2026 · Retail & Commerce Prototype Submission
**Target Duration:** Exactly 2 Minutes 50 Seconds (Hard limit: < 3 Minutes)  
**Tone:** Confident, high-velocity, commercially grounded, architecturally authoritative.  
**Screen Setup:** 1920x1080 full-screen browser at `http://127.0.0.1:5173`, backend live on `http://127.0.0.1:8000`.

---

### Quick Preparation Checklist Before Hitting Record
1. Open browser at `http://127.0.0.1:5173`.
2. Click **Reset Prototype** (`RotateCcw` button in top header) to ensure fresh canonical state.
3. Keep mouse movements smooth, deliberate, and directly matched to the voiceover cues below.

---

### Timeline Breakdown (0:00 – 2:50)

```
0:00 ─── 0:20 : High-Stakes Commercial Hook & Executive Overview
0:20 ─── 0:50 : Stage 1: Shopper Discovery, Spec Comparison & 15-Min Reservation
0:50 ─── 1:10 : Stage 2: Associate Pick & Pack with Real-Time Inventory Ledger
1:10 ─── 1:45 : Stage 3: Priority Rebalancing Decisions (Transfer vs PO Trade-off)
1:45 ─── 2:10 : Stage 4: Dual-Model Forecasting & Anti-Hype AI Restraint
2:10 ─── 2:32 : Stage 5: Self-Healing Product Catalog & Answer Engine Optimization (AEO)
2:32 ─── 2:50 : Stage 6: Immutable Event DAG Trace & Closing Value Impact
```

---

### Segment 1: The Commercial Hook (0:00 – 0:20)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **0:00 – 0:10** | Show **App Header** with `RetailIQ` logo, Store Switcher (`Indiranagar Store`), and Live API indicator. Hover briefly over header. | *"Physical retailers lose over ₹35,000 Crore every single year to a brutal paradox: shoppers walk out empty-handed when their preferred product is out of stock, while inventory planners panic-buy surplus goods from distant suppliers—trapping millions in dead working capital."* |
| **0:10 – 0:20** | Click on **Shopper Discovery** tab. Show the clean search bar pre-populated with: `10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today`. | *"Meet RetailIQ: the autonomous retail intelligence engine that recovers the customer purchase in sixty seconds, protects retailer cash flow, and teaches the supply chain exactly what to stock next."* |

---

### Segment 2: Stage 1 — Shopper Discovery & Walkout Prevention (0:20 – 0:50)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **0:20 – 0:32** | Click **Find Matches**. Watch Gemini parse intent in real time. Three verified alternatives appear on screen (`VoltGo Go 10000`, `VoltGo Mini 5000`, `VoltGo Max 20000`). | *"Let’s start with the shopper. A customer enters an urgent travel query. Gemini parses the natural language into hard constraints—ten thousand mAh, USB-C, under fifteen hundred rupees. Our preferred model is out of stock. But instead of a dead-end walkout, RetailIQ checks authoritative Available-To-Promise stock in PostgreSQL and returns three verified in-stock alternatives."* |
| **0:32 – 0:42** | Click **Compare Specifications** on the first product card (`VoltGo Go 10000`). Highlight the 2-column factual comparison table showing 20W PD compatibility vs requested VoltGo Pro. | *"Clicking Compare Specifications triggers a factual hardware check. Gemini verifies charging protocols—confirming the VoltGo Go delivers full twenty-watt Power Delivery and 100% phone compatibility, saving the customer ₹200."* |
| **0:42 – 0:50** | Click **Select for Pickup**, then click **Reserve for 15 Minutes**. Watch countdown timer start (14:59). Click **Place Customer Order**. Order confirmed modal appears. | *"With one click, the shopper secures a guaranteed fifteen-minute reservation hold backed by database row locks. No phantom stock, no double-selling. We convert the hold into a confirmed Store Pickup order. A lost sale is recovered."* |

---

### Segment 3: Stage 2 — Store Associate Counter Fulfillment (0:50 – 1:10)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **0:50 – 1:00** | Switch to **Store Associate Operations** tab in header. Show the incoming pick queue displaying `Rahul Sharma`, `RQ002`, and shelf coordinates. | *"Switching to Store Associate Operations, our order appears in the real-time queue with exact shelf coordinates. When Rahul arrives at the counter, the associate clicks Fulfill Pickup."* |
| **1:00 – 1:10** | Click **Fulfill Pickup**. Point to the inventory numbers updating live: physical on-hand drops from 12 to 11 units, blocked drops to 0, authoritative ATP remains stable at 9. | *"Watch the authoritative ledger update: physical on-hand stock decrements from twelve to eleven units, while available-to-promise stays mathematically preserved. Zero counter friction, zero ghost inventory."* |

---

### Segment 4: Stage 3 — Priority Rebalancing Decisions (1:10 – 1:45)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **1:10 – 1:22** | Switch to **Business Intelligence & Replenishment** tab. Show KPI summary cards: Margin Opportunity (+₹34,724), Stockouts Avoided, and the **3 Priority Decisions**. | *"Now let's examine the executive perspective. That same pickup purchase has triggered an impending stockout warning for Indiranagar Store. Traditional ERPs would trigger a vendor purchase order—locking up ₹25,380 in minimum order quantities and arriving seven days too late."* |
| **1:22 – 1:35** | Click **Compare Transfer vs Purchase** on Decision 1 (Whitefield Store $\rightarrow$ Indiranagar Store, 12 units). Show the trade-off comparison matrix and Gemini explanation. | *"RetailIQ evaluates the entire network. Whitefield Store holds surplus inventory. An inter-store transfer takes just one day, requires zero new working capital, eliminates supplier lead time, and captures ₹15,074 in net margin."* |
| **1:35 – 1:45** | Click **Approve Transfer (12 units)**. Card transitions cleanly to green **APPROVED** state. | *"The manager reviews the trade-off matrix and approves the transfer with a single click. We solved a critical stockout without spending a single rupee of new capital."* |

---

### Segment 5: Stage 4 — Forecasting & Anti-Hype "AI Restraint" (1:45 – 2:10)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **1:45 – 1:56** | Click on **Demand Forecast (14-Day)** sub-tab. Point out the interactive chart comparing 28-day Moving Average (MA28) vs 7-day Seasonal Naive (SNAIVE7), WAPE metric (8.4%), and Day 2 stockout boundary. | *"Under the Forecast sub-tab, RetailIQ runs dual-model ensemble predictions: a 28-day baseline against a 7-day seasonal challenger with full backtesting metrics, proving the Day 2 stockout curve mathematically."* |
| **1:56 – 2:10** | Click on **External Trends & Demand Signals** sub-tab. Contrast Signal 1 (`EXT01 Solar Camp Lantern`, High-Utility Spike $\rightarrow$ Actionable PO) with Signal 2 (`EXT02 LED Glow Clip`, Viral Social Fad $\rightarrow$ Monitor Only, Qty 0). | *"RetailIQ also demonstrates genuine AI restraint. When social media trends spike, most AI systems hallucinate massive purchase orders. Here, Gemini classifies viral TikTok fads with low conversion, damping the signal to Quantity Zero Monitor Only—saving the business from warehouses full of unsellable dead inventory."* |

---

### Segment 6: Stage 5 — Self-Healing Catalog & AEO (2:10 – 2:32)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **2:10 – 2:22** | Click on **Catalog & AEO Quality** sub-tab. Show the 8-rule audit defect on `RQ001` (missing technical wattage and mAh specs). Point to the fact-grounded proposed patch. Click **Approve and Apply Patch**. | *"Modern shoppers search via ChatGPT and Perplexity. If product specs are incomplete, local store stock becomes invisible to AI search engines. RetailIQ runs an 8-rule deterministic audit, drafts grounded OEM specification patches, and upon approval, immediately elevates catalog health from 88 to 96%."* |
| **2:22 – 2:32** | Scroll to **Live Schema.org JSON-LD Inspector**. Select `RQ002` from the dropdown to show real-time structured microdata. Click on **Product Catalog & AI Enricher** sub-tab briefly. | *"It generates live Schema.org JSON-LD structured microdata, ensuring physical store shelves are directly indexable by autonomous AI purchasing agents."* |

---

### Segment 7: Stage 6 — Immutable Governance DAG & Conclusion (2:32 – 2:50)

| Timecode | On-Screen Action | Exact Voiceover Script |
|---|---|---|
| **2:32 – 2:42** | Click on **System Audit Trace** tab. Scroll through the visual Directed Acyclic Graph (DAG) showing the full chain: Shopper Search $\rightarrow$ Reservation Hold $\rightarrow$ Order Fulfillment $\rightarrow$ Stockout Forecast $\rightarrow$ Transfer Approval. | *"Every action is cryptographically tracked in an immutable audit ledger with visual DAG event tracing, actor accountability, and human-in-the-loop boundaries—eliminating black-box AI risk."* |
| **2:42 – 2:50** | Return to top header, showing clean, synchronized state across the platform. Conclude strongly. | *"RetailIQ: Built with FastAPI, PostgreSQL, React, and Google Gemini for the AI Builder Cup 2026. Recovering lost sales today, engineering the retail supply chain of tomorrow. Thank you."* |

---

### Video Delivery Tips for High Marks
- **Pacing**: Deliver voiceover at approximately 135–140 words per minute. Confident, steady, not rushed.
- **Audio Quality**: Record in a quiet room with a directional microphone or headset.
- **Resolution**: Record at 1080p 60fps. Ensure browser zoom is at 100% or 110% for crisp typography readability.
