# Master Claude Prompt: Generating the Elite RetailIQ Proposal Presentation Deck

> **How to use this file:**  
> Copy the complete prompt block below and paste it directly into Claude (Claude 3.5 Sonnet / Claude 3 Opus / Claude 3.7 Sonnet). It is engineered to produce a visually rich, non-slop, enterprise-grade presentation deck that transforms the technical and commercial value of RetailIQ into an unforgettable pitch.

---

```markdown
You are an elite Silicon Valley venture pitch architect and principal enterprise software designer. Your task is to generate a world-class, visually stunning, non-boring presentation deck for "RetailIQ" — an autonomous retail intelligence and demand platform built for the Google AI Builder Cup 2026.

### STRICT RULES AGAINST "AI SLOP":
1. NO LAZY BULLET POINTS. Never generate generic bullet lists with buzzwords like "leveraging cutting-edge AI for synergistic optimization."
2. HIGH-DENSITY VISUAL BLUEPRINTS. Every slide MUST have an explicit layout blueprint: Bento grid cards, split-screen technical comparisons, mathematical formula callouts, before/after contrast matrices, or process DAG flowcharts.
3. GROUNDED DATA & REAL COMMERCIAL ROI. Use the exact numbers, SKU codes, and metrics from the ground truth specifications provided below (₹35,000 Crore walkout loss, ₹0 working capital transfer vs ₹25,380 locked PO, +₹15,074 margin, 42% carbon reduction, 88 -> 96.2 AEO catalog health score).
4. COLOR PALETTE & DESIGN TOKENS:
   - Primary Background: Deep Obsidian / High-Tech Slate (`#0B0F19`)
   - Surface Cards: Muted Dark Navy (`#111827` / `#1E293B`) with 1px border (`#334155`)
   - Primary Accent: Electric Cobalt (`#3B82F6` / `#2563EB`)
   - Metric / Profit Accent: Vibrant Emerald (`#10B981`)
   - Warning / Hazard Accent: Vivid Amber (`#F59E0B`)
   - AI Intelligence Accent: Cyber Cyan (`#06B6D4`)

---

### GROUND TRUTH DOMAIN KNOWLEDGE (FROM value.txt):

#### Stage 1: The Shopper Perspective — Natural Language Discovery & Walkout Prevention
- Real-World Problem: Customer walks in/searches with an urgent need ("10,000 mAh USB-C power bank under ₹1,500 for travel, pickup today"). Preferred model (VoltGo Pro RQ001) is OOS. 70% of shoppers walk out empty-handed, costing Indian retail ₹35,000 Crore annually.
- RetailIQ Solution:
  1. Natural Language Need Extraction (Gemini Op 1): Sanitizes prompt injection; extracts category, budget ceiling (₹1,500), battery (≥10,000 mAh), port (USB-C), pickup mode.
  2. Fact-Grounded Substitute Matching: Recommends in-stock VoltGo Go (RQ002) at Indiranagar Store for ₹1,299 (saving ₹200).
  3. Hardware Compatibility Verification (Gemini Op 5): Compares electrical protocols (20W PD vs 22.5W SuperCharge), verifying 90% peak charging speed and safe smartphone battery charging.
  4. 15-Minute Guaranteed Reservation Hold: ACID row lock (`SELECT FOR UPDATE`), decreasing Available-To-Promise (ATP) from 10 to 9 with an active countdown timer.
  5. Order Conversion: Customer converts hold to confirmed store pickup order.

#### Stage 2: The Store Associate Perspective — Flawless Counter Fulfillment
- Real-World Problem: In physical retail, omnichannel pickup fails due to inventory confusion, long wait times, or store staff accidentally double-selling reserved shelf stock to walk-in shoppers.
- RetailIQ Solution: Real-time pick & pack queue displaying customer name (Rahul Sharma), order code, and exact shelf coordinates. Associate clicks "Fulfill Pickup". Deterministic inventory engine decrements physical on-hand stock from 12 to 11 units, blocked stock drops from 1 to 0, and ATP remains mathematically preserved at 9 units. Zero counter friction.

#### Stage 3: The Business Manager Perspective — Capital-Efficient Rebalancing
- Real-World Problem: Day 2 impending stockout at Indiranagar. Traditional ERPs trigger vendor purchase orders: 36-unit MOQ, locks up ₹25,380 cash, takes 7 days to arrive (arriving 5 days too late), leaving dead inventory.
- RetailIQ Solution:
  - Scans sister stores and identifies Whitefield Store with surplus stock.
  - Inter-store transfer: 12 units moved, 1-day lead time (arrives before stockout), ₹0 new working capital required, saves ₹25,380 cash lockup, captures +₹15,074 net contribution margin, 42% lower carbon emissions.
  - Human-in-the-loop: Manager reviews trade-off comparison matrix and approves transfer with 1 click.

#### Stage 4: Merchandising & Supply Chain — Anti-Hype "AI Restraint"
- Real-World Problem: Retailers chase viral TikTok/Instagram trends, buying massive vendor orders that collapse within days, creating warehouses full of dead stock.
- RetailIQ Solution:
  - Signal Ingestion: Scans search spikes vs social engagement.
  - High-Utility Search (EXT01 Solar Camp Lantern): +180% search spike, 85% search-to-basket conversion -> Gemini classifies as HIGH_UTILITY_SEARCH -> Recommends Actionable PO of 18 units.
  - Viral Social Fad (EXT02 TikTok LED Glow Clip): +420% video view surge, but basket conversion is < 1% -> Gemini applies Signal Damping, classifies as VIRAL_SOCIAL_FAD -> Caps replenishment at Quantity 0 (Monitor Only), overriding naive algorithms.

#### Stage 5: E-Commerce & Catalog Ops — Self-Healing Catalog & AEO
- Real-World Problem: Shoppers now use AI agents (ChatGPT, Gemini, Perplexity) to find products. If a catalog lacks verified technical attributes (missing wattage, battery chemistry, port standards), AI search engines fail to recommend it, rendering physical store inventory invisible.
- RetailIQ Solution:
  - 8-Rule Deterministic Audit: Flags defect on RQ001 (missing technical wattage and mAh specs).
  - Grounded OEM Spec Patching (Gemini Op 2): Reads manufacturer datasheets and drafts factual title/description updates with explicit fact citations.
  - AEO Elevation: Generates live Schema.org JSON-LD microdata for AI web agents. Approval jumps catalog health from 88 to 96.2/100.

#### Stage 6: Governance & Audit — Full Explainability & Event Tracing
- Real-World Problem: Regulators and executives distrust autonomous AI because of "black-box" hallucination risks.
- RetailIQ Solution: Visual Directed Acyclic Graph (DAG) event trace tracking the complete provenance chain (Search -> Hold -> Order -> Fulfillment -> Stockout -> Transfer -> Approval). 100% auditable with actor UIDs, timestamps, and Live vs Fallback model flags.

---

### YOUR DELIVERABLE FORMAT:
Generate a complete, slide-by-slide master presentation (12 to 14 slides). For EVERY slide, provide:
1. **Slide Title & Strategic Purpose**: What is the singular punchline of this slide?
2. **Visual Layout Architecture**: (e.g., 3-column Bento grid, split Before/After card, live metric scorecard with glow borders, workflow DAG diagram).
3. **Exact On-Slide Copy**: Headers, sub-headers, KPI chips, and card content.
4. **Visual Graphic / Diagram Specification**: Detailed Mermaid diagram, ASCII flowchart, or CSS visual mockup showing how data is structured.
5. **Presenter Talking Points (2-3 sentences)**: What the speaker should say out loud to captivate judges and investors.

### SLIDE OUTLINE TO BUILD:
- Slide 1: Title & Vision — "RetailIQ: Autonomous Omnichannel Intelligence"
- Slide 2: The ₹35,000 Crore Industry Crisis (Walkout Dilemma vs. Panic Purchasing)
- Slide 3: The Broken Retail Loop vs. The RetailIQ Autonomous Loop
- Slide 4: Persona 1 (Shopper) — Walkout Prevention & Gemini Fact-Grounded Substitution
- Slide 5: The Math of Trust — Deterministic Available-to-Promise (ATP) & ACID Row Locks
- Slide 6: Persona 2 (Store Associate) — Frictionless Counter Handover & The Real-Time Ledger
- Slide 7: Persona 3 (Business Manager) — The Capital Trade-off (Inter-Store Transfer vs Supplier PO)
- Slide 8: Predictive Intelligence — Dual-Model Forecasting (MA28 vs SNAIVE7 with WAPE Backtests)
- Slide 9: Persona 4 (Merchandiser) — Genuine "AI Restraint": Quelling Social Media Fads
- Slide 10: Persona 5 (E-Commerce) — Self-Healing Catalog & Answer Engine Optimization (AEO)
- Slide 11: Persona 6 (CTO & Compliance) — Immutable Provenance & The Governance Event DAG
- Slide 12: Business Impact & Unit Economics Scorecard (Hard Metrics & ROI)
- Slide 13: Technical Architecture & Google Cloud / Gemini Integration
- Slide 14: Conclusion & The Future of Autonomous Commerce

Ensure the output is written with extraordinary precision, elite design taste, and complete fidelity to the RetailIQ codebase and value architecture.
```
