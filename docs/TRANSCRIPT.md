# RetailIQ — Official 2m 50s Demo Video Transcript
## AI Builder Cup 2026 · Retail & Commerce Prototype Submission
**Target Video Duration:** Exactly 2 minutes 45 seconds to 2 minutes 50 seconds (< 3:00 hard cutoff)  
**Track:** Retail & Commerce (Intelligent Customer & Business Experiences)  
**Format:** Screen recording of live running software with voiceover (Solo or 2-Speaker Duo)

---

## Roles Overview (For 2-Speaker Presentation)
* **Speaker 1 (Shopper & Frontend Experience):** Introduces problem statement, walks through conversational search, intent extraction, fact-grounded substitution, and 15-minute lock order placement.
* **Speaker 2 (Associate Operations & Business Intelligence):** Walks through store pickup fulfillment, inventory ledger decrement, multi-echelon transfer rebalancing vs supplier POs, trend restraint, and cryptographic audit trace.
*(Note: If recording solo, simply speak both roles continuously.)*

---

## Verbatim Video Transcript & Synchronized Screen Actions

### [0:00 – 0:18] Scene 1: The Commercial Problem & Platform Intro
* **Visual on Screen:** 
  * Open browser in full screen at `http://127.0.0.1:8000` showing the **RetailIQ** clean 2-tier header.
  * Show the active store: `Indiranagar Store (S1)` and the green glowing **Backend Live** status pill.
* **Speaker 1 (Voiceover):**
  > "Every year, retailers lose billions in revenue to a painful paradox: customers walk away empty-handed when their desired product is out of stock, while merchandising managers blindly order surplus inventory from suppliers—locking up millions in working capital.
  > 
  > This is **RetailIQ**: an autonomous retail intelligence platform built for the AI Builder Cup 2026. RetailIQ pairs Google Gemini with strictly deterministic inventory mathematics to recover lost shopper sales and optimize multi-echelon stock rebalancing."

---

### [0:18 – 0:52] Scene 2: Shopper Intent, ATP Stock & Verified Substitute
* **Visual on Screen:**
  * Cursor clicks the search chip: `⚡ 10,000 mAh USB-C power bank under ₹1,500`.
  * The search runs instantly.
  * Point cursor to the left **Verified Shopper Criteria** panel showing: `Capacity: >= 10,000 mAh`, `Port: USB-C`, `Budget: <= ₹1,500`, `Brand: Prefer VoltGo Pro`.
  * Point cursor to the red card: **Out of Stock: VoltGo Pro (RQ001)** — Network ATP: 0.
  * Move cursor down to the green card: **VoltGo Go (RQ002) - Verified Substitute** — Available at Indiranagar: 12 units.
  * Click **Compare Specifications**. The side-by-side comparison modal opens, showing identical capacity, 20W PD, and warranty. Close the modal.
* **Speaker 1 (Voiceover):**
  > "Let's begin with the shopper experience. A customer enters a natural language need: a 10,000 mAh USB-C power bank under ₹1,500 for travel today, preferring VoltGo Pro.
  > 
  > Google Gemini extracts the customer's exact constraints: battery capacity, fast charging, and price ceiling. 
  > 
  > RetailIQ immediately checks authoritative Available-To-Promise stock in PostgreSQL. The requested VoltGo Pro is completely out of stock across the entire city. But instead of returning a dead end or hallucinating phantom stock, RetailIQ identifies a verified in-stock substitute: the **VoltGo Go** at ₹1,299 at our Indiranagar store. Comparing specifications side-by-side proves identical power specs, saving the customer ₹200 with zero compromise."

---

### [0:52 – 1:18] Scene 3: 15-Minute Row Lock & Live In-Store Pickup
* **Visual on Screen:**
  * On the left panel, click **Reserve for 15 Minutes**.
  * The green reservation banner appears with the live ticking countdown timer: `14:59... 14:58...`.
  * Click **Place Demo Order**.
  * The confirmation modal appears with the generated order code (e.g., `ORD-53C47B4F`).
  * Click **Switch to Associate Pickup Queue**.
* **Speaker 1 (Voiceover):**
  > "The customer clicks **Reserve for 15 Minutes**. This initiates an authoritative database hold backed by row-level locking, preventing race conditions while the live countdown timer ticks.
  > 
  > When we click **Place Demo Order**, RetailIQ binds the reservation into a confirmed store order. Now, let's switch to the store associate to see fulfillment in action."

---

### [1:18 – 1:45] Scene 4: Store Associate Fulfillment & Atomic Stock Decrement
* **Visual on Screen:**
  * Now on **Store Associate & Stock Operations** tab.
  * Show the top **Live Inventory Ledger** table for VoltGo Go: `On-Hand: 12`, `Active Holds: 1`.
  * Under **Pickup Order Queue**, locate the newly placed order.
  * Click **Fulfill Pickup Handover**.
  * The Stock Mutation modal pops up showing authoritative ledger state: `Before: 12 On-Hand` ➔ `After: 11 On-Hand`.
  * Click **Done & Return to Queues**.
  * Click **Inter-Store Transfers** tab, then **Supplier Purchase Orders** tab to show queue handling.
* **Speaker 2 (Voiceover):**
  > "In the Store Associate dashboard, Rahul's pickup order is waiting on the counter queue. When the customer arrives, the associate taps **Fulfill Pickup Handover**. 
  > 
  > Behind the scenes, RetailIQ executes an atomic transaction: verifying physical handover, decrementing store on-hand inventory from 12 to 11 units, and generating an immutable ledger movement record. There is zero ghost stock and complete transactional integrity."

---

### [1:45 – 2:18] Scene 5: Business Intelligence & Explainable Rebalancing
* **Visual on Screen:**
  * Click **Business Intelligence & Replenishment** in the top navigation.
  * Shows **Executive Demand & Inventory Intelligence**.
  * Under the **Priority Decisions** tab, point cursor to the decision card:
    * *Transfer from Koramangala (S2) to Indiranagar (S1)*.
    * Compare the metrics:
      * Inter-Store Transfer: Cost ₹1,360, Lead time 1 day, Working Capital ₹0.
      * Supplier Purchase Order: Cost ₹36,000, Lead time 14 days, MOQ 30 units.
  * Click **Approve Transfer**. Toast confirms approval.
  * Click **14-Day Forecast & Baseline** sub-tab to display the daily simulated stock levels and seasonal baseline curve.
* **Speaker 2 (Voiceover):**
  > "Now, what happens to the supply chain after that sale? That customer purchase triggers an impending stockout projection for Indiranagar.
  > 
  > Traditional retail ERPs blindly issue expensive purchase orders to suppliers. But RetailIQ’s multi-echelon engine searches the regional network and discovers a 32-unit surplus at Koramangala. 
  > 
  > Instead of spending ₹36,000 on a supplier purchase order with a 14-day lead time, RetailIQ recommends a lateral store transfer costing just ₹1,360, arriving tomorrow! Following human-in-the-loop governance, the manager reviews the explainable trade-off and clicks **Approve Transfer**, immediately protecting margin without tying up new capital."

---

### [2:18 – 2:38] Scene 6: Genuine AI Restraint & Catalog AEO Governance
* **Visual on Screen:**
  * Click **Demand & External Trends** sub-tab.
  * Point cursor to Card 1: *Surge in Solar Lantern Inquiries* (+210% search volume -> Capped at +25% forecast uplift -> Safety PO recommended).
  * Point cursor to Card 2: *Viral Social Media Fad* (+420% TikTok trend -> Action: MONITOR ONLY, 0 units ordered, Reason: Zero basket conversion correlation).
  * Click **Catalog & AEO Quality** sub-tab:
  * Show Catalog Health Score `88/100`, highlight side-by-side spec patch, click **Approve Patch**.
* **Speaker 2 (Voiceover):**
  > "RetailIQ also demonstrates genuine **AI Restraint**. When external signals spike, our trend engine tests them against real POS basket conversions. A legitimate monsoon utility spike for solar lanterns is prudently capped at a 25% lift. But a viral social media fad with zero local basket conversion is explicitly dampened—recommending MONITOR ONLY with zero units ordered, protecting retailers from costly dead stock.
  > 
  > In **Catalog Governance**, automated Answer Engine Optimization detects incomplete manufacturer specs, allowing one-click manager approval of factual patches so external AI search engines correctly index store products."

---

### [2:38 – 2:50] Scene 7: Cryptographic Audit Trace & Wrap-Up
* **Visual on Screen:**
  * Click **Audit & Decision Trace** in the top navigation.
  * Scroll through the sequential event ledger showing: `ORDER`, `FULFILLMENT`, `TRANSFER`, and `CATALOG_PATCH` events.
  * Click **Architecture Explainer** in the top header to display the system modal.
* **Speaker 1 & 2 (Closing Voiceover):**
  > "Every transaction, recommendation, and stock movement is sequentially recorded in our immutable audit ledger. 
  > 
  > Built with React, FastAPI, PostgreSQL, and Google Gemini—architected for Google Cloud Run and Firebase. 
  > 
  > RetailIQ: Recover the purchase, protect working capital, and build the future of intelligent retail. Thank you!"

---

## Presenter Rehearsal Checklist
1. **Pacing:** Speak at an energetic, conversational pace (~140 words per minute).
2. **Timing Marks:**
   * At 0:52: Finish the Shopper View and click **Place Demo Order**.
   * At 1:45: Finish Associate fulfillment and click **Business Intelligence**.
   * At 2:38: Finish Trends & Catalog and click **Audit & Decision Trace**.
   * At 2:48: Conclude speech and stop screen recording.
3. **Audio Quality:** Use a clean microphone in a quiet room with minimal background echo.
