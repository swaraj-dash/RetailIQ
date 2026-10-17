# RetailIQ — 2-Minute 50-Second Submission Video Script
## AI Builder Cup 2026 · Retail & Commerce Prototype Demo

**Target Length:** Exactly 2 minutes and 50 seconds (follows strict under-3-minute rule).  
**Tone:** Confident, crisp, technical, and commercially grounded.  
**Visual Style:** Screen recording of the live running RetailIQ application. No mockups or slides during the demo; pure software execution.

---

### Timeline Breakdown

| Timecode | Visual on Screen | Spoken Voiceover |
|---|---|---|
| **0:00 – 0:15** | App Header & Landing Page showing "Synthetic Demo Data" and "17 Oct 2026". | *"Retailers lose billions each year to a frustrating paradox: customers walk away empty-handed when preferred items are out of stock, while category managers panic-buy inventory from suppliers—trapping millions in working capital. This is RetailIQ: an autonomous retail intelligence platform that recovers the purchase and learns what to stock next."* |
| **0:15 – 0:40** | **Shopper View:** Type natural language prompt: *"10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today. Prefer VoltGo Pro."* Click **Find Matches**. | *"Let's look at the shopper experience. A customer enters a complex natural language need with strict constraints. Gemini extracts the criteria: capacity over 10,000 mAh, USB-C, under ₹1,500, with a preference for VoltGo Pro. Crucially, RetailIQ checks authoritative Available-To-Promise stock in the database. VoltGo Pro is completely out of stock across the network (ATP 0). Instead of a dead end or hallucinated stock, RetailIQ identifies a verified in-stock substitute: the VoltGo Go at ₹1,299."* |
| **0:40 – 0:55** | Click **Compare Specifications**, show verified checkmarks, click **Reserve for 15 Minutes**, then **Place Demo Order**. | *"We can compare specifications side-by-side: battery capacity, 20-watt PD charging, and warranty are identical. We create a 15-minute reservation hold backed by database row locks, and place our demo pickup order. Order ORD-20261017-001 is confirmed with an authoritative allocation."* |
| **0:55 – 1:20** | Switch to **Associate View**. Show Order queue, click **Fulfill Pickup Handover**. Show On-hand decrement (12 ➔ 11). | *"Now we switch to the store associate view. Our pickup order appears instantly in the queue. When the customer arrives, the associate fulfills the handover with one click. The stock ledger immediately updates: physical on-hand inventory drops from 12 to 11 units, without any ghost inventory or race conditions."* |
| **1:20 – 1:55** | Switch to **Business Intelligence View**. Open **Priority Decisions**, click **Compare Transfer vs Purchase**. Click **Approve Transfer (32 units)**. | *"Now let's look at the executive view. That same pickup purchase has triggered an impending stockout warning for Indiranagar. RetailIQ evaluates three deterministic pathways: a vendor purchase order requires a 36-unit MOQ and 5 days of lead time, tying up ₹25,380 in working capital. But Store 2 in Koramangala has 32 units of safe excess. An inter-store transfer takes only 1 day, requires zero working capital, and captures ₹15,074 in net contribution. As a manager, I review and approve the demo transfer."* |
| **1:55 – 2:15** | Switch back to **Associate View** ➔ **Transfers Tab**. Click **Dispatch from S2**, then **Receive at S1**. | *"In the associate view, the transfer is registered as PENDING_DISPATCH. The donor store dispatches 32 units—reducing their on-hand from 48 to 16. When the truck arrives at Indiranagar, the associate marks it received. Stock conservation is 100% mathematically preserved across our network."* |
| **2:15 – 2:35** | Switch to **Demand & External Trends** tab in Business view. Show EXT01 vs EXT02. | *"RetailIQ also demonstrates genuine AI restraint. In our trend analysis, a high-intent solar lantern search spike justifies an 18-unit safety purchase order. But for a viral social media glow clip with weak basket conversion, RetailIQ dampens the hype and recommends MONITOR ONLY with zero units ordered, protecting the retailer from dead inventory."* |
| **2:35 – 2:50** | Switch to **Decision Audit Trace** tab. Conclude video. | *"Every action—from shopper search to reservation, fulfillment, and rebalancing—is recorded in an immutable audit trace. Built with React, FastAPI, PostgreSQL, and Google Gemini for the AI Builder Cup 2026. RetailIQ: Recover the purchase, protect working capital."* |

---

### Recording Checklist
- [x] Run backend server on `http://localhost:8000` with seeded canonical data.
- [x] Run frontend on `http://localhost:3000` with full-screen browser (1920x1080 or 1440x900).
- [x] Use clean audio voiceover matching the script timestamps.
- [x] Ensure total duration is under 2 minutes 50 seconds.
- [x] Verify resolution is 1080p and text is crisp.
