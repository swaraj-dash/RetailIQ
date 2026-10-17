# RetailIQ — 3-Minute Video Demo Walkthrough & Presenter Script
**Competition:** AI Builder Cup 2026  
**Track:** Retail & Commerce (Intelligent Customer & Business Experiences)  
**Target Video Duration:** 2 minutes 50 seconds (Target < 3:00 max)

---

## Quick Setup Before You Record

1. **Start the Backend & Web Application:**
   ```powershell
   cd D:\Projects\RetailIQ\backend
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
2. **Open in Browser:** `http://127.0.0.1:8000` (Chrome or Edge in full-screen `F11`).
3. **Zoom Level:** Set browser zoom to 100% or 110% for crisp readability.
4. **Default Store:** Keep store set to **Indiranagar (Store 1)** in the top header.
5. **Status Pill:** Verify the green **"Backend Live"** indicator is glowing in the top right.

---

## 3-Minute Video Timeline & Exact Script

```
0:00 ─── 0:20  [Intro] The Core Problem in Retail
0:20 ─── 0:55  [Scene 1: Shopper] Fact Grounding & Real In-Stock Alternative
0:55 ─── 1:25  [Scene 2: Operations] 15-Min Lock & Live Counter Pickup Handover
1:25 ─── 2:05  [Scene 3: Business Intelligence] Transfer vs Purchase Rebalancing
2:05 ─── 2:30  [Scene 4: AI Restraint & Catalog AEO] Filtering Social Fads
2:30 ─── 2:50  [Wrap-up] Architecture, Google Cloud & Production Scalability
```

---

### Segment 1: The Problem (0:00 – 0:20)
* **Screen:** Open on the **Shopper View** (`http://127.0.0.1:8000`).
* **Speaker:**
  > "Every year, retailers lose billions in revenue because customers walk away when the exact product they want is out of stock. Even worse, merchandising teams often overreact by blindly purchasing excess stock from suppliers, locking up precious working capital in dead inventory.
  > 
  > This is **RetailIQ**: an intelligent, closed-loop commerce platform powered by Google Gemini and deterministic inventory math. It recovers lost shopper purchases with verified in-stock alternatives, and optimizes inventory rebalancing before spending money on suppliers."

---

### Segment 2: Shopper Intent & Verified In-Stock Match (0:20 – 0:55)
* **Screen Action:**
  1. Click the first prompt chip: **`⚡ 10,000 mAh USB-C power bank under ₹1,500`** (or press Enter in the search bar).
  2. Point your cursor to the left **"Verified Shopper Criteria"** card.
  3. Point your cursor to the red **"Out of Stock: VoltGo Pro (RQ001)"** card, then down to the green **"VoltGo Go (RQ002) - Verified Substitute"** card.
  4. Click **"Compare Specifications"** button to open the side-by-side comparison modal, then close it.
* **Speaker:**
  > "Let's start from a shopper's perspective. A customer asks in natural language for a *10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today*, with a preference for VoltGo Pro.
  > 
  > Google Gemini extracts the customer's hard requirements: 10,000 mAh minimum, USB-C bi-directional charging, and ₹1,500 budget ceiling.
  > 
  > Notice what happens: our deterministic Available-to-Promise engine checks live store stock and discovers VoltGo Pro has 0 units across the city. Instead of losing the customer or hallucinating stock, RetailIQ immediately identifies a verified, in-stock substitute: the **VoltGo Go** at ₹1,299 at our Indiranagar store. Comparing specifications side-by-side confirms identical battery capacity, USB-C PD, and a 1-year warranty—saving the customer ₹200."

---

### Segment 3: 15-Minute Row Lock & Store Associate Pickup (0:55 – 1:25)
* **Screen Action:**
  1. In the left **"Reserve & Pickup Cart"**, click **"Reserve for 15 Minutes"**.
  2. Point out the ticking countdown timer (`Hold Active: 14:59...`).
  3. Click **"Place Demo Order"**.
  4. The Confirmation Modal pops up with Order Code `ORD-...` and Allocation ID.
  5. Click **"Switch to Store Associate Operations"**.
  6. In Associate View, look at the top order: click **"Fulfill Pickup Handover"**.
  7. Point out the green confirmation toast and the live inventory table decrementing (`on_hand: 12 → 11`).
* **Speaker:**
  > "The customer reserves the item for 15 minutes. This creates an authoritative database hold backed by row-level locking, preventing race conditions.
  > 
  > We click **Place Demo Order**, which instantly generates a confirmed order and reserves stock at the Indiranagar counter.
  > 
  > Now let's switch to the **Store Associate**. The store employee sees Rahul's pickup order waiting at the counter. When the customer arrives, the associate taps **Fulfill Pickup Handover**. Behind the scenes, RetailIQ executes an atomic transaction: verifying stock, decrementing on-hand inventory from 12 to 11 units, and generating an immutable audit movement record."

---

### Segment 4: Business Intelligence & Explainable Rebalancing (1:25 – 2:05)
* **Screen Action:**
  1. Click **"Business Intelligence"** in the top navigation bar.
  2. In the first tab **"Priority Decisions"**, point to the recommendation card:
     * *Transfer 8 units from Koramangala (S2) to Indiranagar (S1)*.
  3. Highlight the mathematical cost comparison box:
     * Transfer Cost: ₹1,360 (1-day lead time).
     * Supplier PO Cost: ₹36,000 (14-day lead time + MOQ 30).
     * Capital Saved / Stockout Prevented: ₹34,640.
  4. Click **"Approve Plan"**.
  5. Click **"14-Day Forecast & Baseline"** tab to show the forecast graph.
* **Speaker:**
  > "Now, what happens to the supply chain after that sale? Let's move to **Business Intelligence**.
  > 
  > With Indiranagar down to 10 units and steady daily demand, a stockout is projected within 4 days. Standard ERP systems would blindly generate an expensive purchase order to a supplier.
  > 
  > RetailIQ’s multi-echelon planning engine analyzes the entire city network. It finds an excess surplus at Koramangala (S2). Instead of issuing a ₹36,000 supplier purchase order with a 14-day lead time, RetailIQ recommends an inter-store transfer of 8 units costing only ₹1,360, arriving tomorrow!
  > 
  > It requires explicit human authorization—we click **Approve Plan**, creating an authoritative transfer and rebalancing store stock while saving working capital."

---

### Segment 5: Genuine AI Restraint & Catalog Governance (2:05 – 2:30)
* **Screen Action:**
  1. Click **"Demand & External Trends"** sub-tab.
  2. Point out the two contrasting trend cards:
     * Card 1: *Surge in Solar Lantern Inquiries* (+210% search spike, validated by store footfall -> Capped at +25% lift, approved PO).
     * Card 2: *Viral Social Media Fad* (+420% TikTok trend -> REJECTED: 0 conversion evidence, low reliability score, avoids dead inventory).
  3. Click **"Catalog & AEO Quality"** sub-tab:
     * Show score 88/100, click **"Approve Catalog Patch"** to update battery specs.
* **Speaker:**
  > "RetailIQ also introduces genuine **AI Restraint** in trend intelligence. When external signals spike, it tests them against real shopper conversion data. A legitimate search spike for solar lanterns is capped at a conservative 25% lift to avoid over-ordering. Meanwhile, a viral social media fad with zero local basket conversion is explicitly rejected, stopping merchandising teams from buying dead stock.
  > 
  > In **Catalog Governance**, automated Answer Engine Optimization checks detect missing battery attributes, allowing managers to approve factual patches in one click."

---

### Segment 6: Architecture, Google Cloud & Production Readiness (2:30 – 2:50)
* **Screen Action:**
  1. Click **"Trace & Audit"** in the top navigation.
  2. Scroll down the cryptographic event stream (showing Order, Transfer, PO, Catalog Patch events).
  3. Click **"Decision Logic"** in the top header to display the architecture diagram modal.
* **Speaker:**
  > "Every transaction, model invocation, and stock movement is recorded in our cryptographic audit trace. Gemini powers natural language understanding and explainability, while all financial, inventory, and allocation calculations remain strictly deterministic.
  > 
  > Built with React, FastAPI, PostgreSQL, and Google Gemini, RetailIQ is containerized for Google Cloud Run and Firebase Hosting.
  > 
  > RetailIQ transforms lost sales into instant conversions, and protects retail balance sheets. Thank you!"

---

## Tips for Recording

1. **Keep cursor movement deliberate:** Smoothly point to what you are describing. Don't rush or shake the cursor.
2. **Audio:** Use a headset or dedicated microphone in a quiet room.
3. **Timer Check:** Practice once with a phone stopwatch. Aim to finish between **2:40 and 2:50** so you stay safely within the 3-minute hard cutoff.
4. **Export Resolution:** 1080p (1920x1080), 30fps or 60fps MP4.
