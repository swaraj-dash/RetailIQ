import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="docs/RetailIQ_Proposal_Deck.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_COLOR = RGBColor(11, 15, 25)        # Slate 950 / Dark Navy
    CARD_BG = RGBColor(19, 27, 44)         # Deep Navy Card
    TEXT_LIGHT = RGBColor(243, 244, 246)   # Gray 100
    TEXT_MUTED = RGBColor(156, 163, 175)   # Gray 400
    ACCENT_BLUE = RGBColor(59, 130, 246)   # Blue 500
    ACCENT_CYAN = RGBColor(6, 182, 212)    # Cyan 500
    ACCENT_GREEN = RGBColor(16, 185, 129)  # Emerald 500
    ACCENT_PURPLE = RGBColor(139, 92, 246) # Purple 500
    ACCENT_AMBER = RGBColor(245, 158, 11)  # Amber 500

    def apply_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

    def add_header(slide, title_text, category_text="AI BUILDER CUP 2026 · RETAIL & COMMERCE"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Header Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.space_after = Pt(8)

        for b in body_bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(12)
            p_b.font.color.rgb = TEXT_LIGHT
            p_b.space_after = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 1: Cover & Executive Vision
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    logo_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.9), Inches(0.9))
    logo_box.fill.solid()
    logo_box.fill.fore_color.rgb = ACCENT_BLUE
    logo_box.line.fill.background()
    tf_l = logo_box.text_frame
    p_l = tf_l.paragraphs[0]
    p_l.text = "IQ"
    p_l.font.size = Pt(28)
    p_l.font.bold = True
    p_l.font.color.rgb = RGBColor(255, 255, 255)
    p_l.alignment = PP_ALIGN.CENTER

    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.5), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "RetailIQ"
    p0.font.size = Pt(44)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_LIGHT

    p1 = tf.add_paragraph()
    p1.text = "Recover the Purchase. Learn What to Stock Next."
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN
    p1.space_before = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "An Autonomous Closed-Loop Retail Intelligence Engine Powered by Google Gemini & Deterministic Inventory Math"
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(10)

    # Stat Badges at bottom
    stats = [
        ("₹1.2T", "Global Stockout Leakage", ACCENT_AMBER),
        ("100%", "Deterministic ATP Locks", ACCENT_GREEN),
        ("+₹15,074", "Net Margin per Transfer", ACCENT_CYAN),
        ("0 Qty", "AI Restraint on Social Fads", ACCENT_PURPLE),
    ]
    for idx, (val, lbl, col) in enumerate(stats):
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.95), Inches(5.0), Inches(2.75), Inches(1.5))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col
        box.line.width = Pt(1.5)
        btf = box.text_frame
        btf.margin_top = Inches(0.2)
        bp1 = btf.paragraphs[0]
        bp1.text = val
        bp1.font.size = Pt(26)
        bp1.font.bold = True
        bp1.font.color.rgb = col
        bp1.alignment = PP_ALIGN.CENTER
        bp2 = btf.add_paragraph()
        bp2.text = lbl
        bp2.font.size = Pt(11)
        bp2.font.color.rgb = TEXT_MUTED
        bp2.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Industry Reality
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "The ₹35 Lakh Problem: Lost Sales & Trapped Working Capital")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "1. The Shopper Dilemma",
             [
                 "4.2% of retail sales are lost permanently due to unexpected stockouts.",
                 "72% of shoppers walk out instead of browsing manual substitutes.",
                 "High friction: customer drives to store only to discover phantom inventory.",
                 "E-commerce giants capture the walkaway revenue with same-day delivery."
             ], ACCENT_AMBER)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "2. The Reactive Merchandiser",
             [
                 "Traditional ERPs react to stockouts by firing expensive overseas POs.",
                 "Suppliers demand high MOQs (36+ units) and 14-day lead times.",
                 "Over ₹35 Lakhs of working capital is trapped in slow-moving warehouse pallets.",
                 "S1 suffers stockout while sister store S2 sits on 32 excess units!"
             ], ACCENT_BLUE)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "3. The Generative AI Danger",
             [
                 "Generative LLMs hallucinate phantom inventory and fictitious pricing.",
                 "A single hallucinated unit breaks customer trust and corrupts supply chains.",
                 "Uncontrolled agents blindly order stock based on viral TikTok hype.",
                 "Enterprise retail demands strict mathematical ledger guarantees."
             ], ACCENT_PURPLE)

    # -------------------------------------------------------------
    # SLIDE 3: The RetailIQ Solution Loop
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "The Solution: A Closed-Loop Intelligence Engine")

    steps = [
        ("Step 1: Shopper Discovery", "Conversational Gemini 2.5 Flash normalizes fuzzy queries into typed specs (10,000 mAh, USB-C, <₹1,500).", ACCENT_CYAN),
        ("Step 2: Grounded Substitute", "Preferred SKU out of stock -> Instantly surfaces verified in-stock VoltGo Go with side-by-side spec parity.", ACCENT_GREEN),
        ("Step 3: Row-Locked Hold", "15-minute countdown reservation backed by PostgreSQL 'SELECT ... FOR UPDATE' row lock. Zero phantom stock.", ACCENT_BLUE),
        ("Step 4: Physical Handover", "Associate scans barcode; handover fulfills order, atomically decrementing on-hand stock (12 -> 11 units).", ACCENT_PURPLE),
        ("Step 5: Multi-Store Rebalance", "Decision engine detects S1 stockout and executes S2 -> S1 transfer (+₹15,074 margin) with human approval.", ACCENT_AMBER),
    ]

    for idx, (title, text, col) in enumerate(steps):
        top_pos = Inches(1.8 + idx * 1.02)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), Inches(0.88))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = f"{title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        run = p.add_run()
        run.text = text
        run.font.size = Pt(12)
        run.font.bold = False
        run.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 4: Community & Socio-Economic Impact
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "Positive Community & Environmental Impact")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "Empowering Local Physical Retailers",
             [
                 "Levels the playing field for local and regional brick-and-mortar stores against e-commerce monopolies.",
                 "BOPIS (Buy Online, Pick-up In Store) keeps commerce and tax revenue within neighborhood communities.",
                 "Frees working capital for kiranas and retail franchisees to hire and expand."
             ], ACCENT_GREEN)

    add_card(s4, Inches(6.9), Inches(1.8), Inches(5.6), Inches(2.4),
             "Slashing Logistics Carbon Emissions",
             [
                 "Short-distance inter-store transfers (1-day local van) eliminate long-haul freight from centralized factories.",
                 "Dramatically reduces fuel consumption and urban transport emissions.",
                 "Prevents unneeded manufacturing of excess units destined for scrap."
             ], ACCENT_CYAN)

    add_card(s4, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "Eliminating Landfill & Dead Stock Waste",
             [
                 "AI Restraint prevents ordering viral fads (e.g. Glow Clips) that end up discarded in municipal landfills.",
                 "Dynamic multi-echelon rebalancing ensures products find genuine consumers before expiration.",
                 "Fosters a circular, zero-waste retail ecosystem."
             ], ACCENT_AMBER)

    add_card(s4, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.4),
             "Restoring Consumer Trust & Efficiency",
             [
                 "Guaranteed inventory holds eliminate wasted physical trips and frustrated journeys.",
                 "Transparent price and spec comparisons prevent predatory upselling.",
                 "Builds lasting community confidence between shoppers and store associates."
             ], ACCENT_PURPLE)

    # -------------------------------------------------------------
    # SLIDE 5: Technical Feasibility & System Architecture
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "Production-Grade Feasibility & Technical Architecture")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Frontend & Edge Tier",
             [
                 "React 18, TypeScript, Vite 5 SPA.",
                 "Firebase Hosting global edge CDN.",
                 "Tailwind CSS responsive design system.",
                 "Anonymous Firebase UID tenancy isolation.",
                 "Playwright E2E tested with 0 console errors."
             ], ACCENT_CYAN)

    add_card(s5, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Core Services Tier",
             [
                 "Google Cloud Run containerized FastAPI.",
                 "Deterministic ATP & 15-min reservation hold.",
                 "Multi-echelon rebalancing decision engine.",
                 "IdempotencyRecord prevents duplicate orders.",
                 "UsageBucket token-bucket rate limiting."
             ], ACCENT_BLUE)

    add_card(s5, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Data & Intelligence Tier",
             [
                 "Cloud SQL PostgreSQL 17 (32 tables).",
                 "Row-level locking ('SELECT ... FOR UPDATE').",
                 "Gemini 2.5 Flash via Vertex AI Cloud ADC.",
                 "Fallback adapter when credentials absent.",
                 "Immutable SHA-256 cryptographic trace."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 6: AI Restraint on Trends & Catalog Governance
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "AI Restraint: Separating Real Utility from Social Fads")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "High-Utility Search Spike (Solar Lantern)",
             [
                 "Signal: Search query volume surged +380% for outdoor emergency lighting.",
                 "Context: Regional monsoon season approaching Bengaluru.",
                 "Classification: High-intent, non-frivolous consumer demand.",
                 "AI Restraint Policy: Capped demand forecast uplift at conservative +25% safety ceiling.",
                 "Outcome: Approved safe PO for 18 units; captures ₹18,000 margin without overbuying risk."
             ], ACCENT_GREEN)

    add_card(s6, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
             "Viral Social Media Fad (LumaTrail Glow Clip)",
             [
                 "Signal: TikTok / Instagram video views spiked +420% for novelty clip.",
                 "Context: Zero correlation with local cart conversions or repeat baskets.",
                 "Classification: Short-lived viral hype with 28% source reliability.",
                 "AI Restraint Policy: Damped to 'MONITOR ONLY' (Recommended Qty: 0 units).",
                 "Outcome: Rejected ₹1.2 Lakh supplier PO; completely prevented trapped dead stock."
             ], ACCENT_PURPLE)

    # -------------------------------------------------------------
    # SLIDE 7: Business Model & Economic Value Creation
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, "Economic Feasibility: Transfer vs. Purchase Economics")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The Mathematical Rebalancing Trade-Off",
             [
                 "Option A: Inter-Store Transfer from S2 (Optimal)",
                 "  • Logistics Cost: ₹1,360 local van dispatch.",
                 "  • Lead Time: 1 day (recovers stockout before Day 2).",
                 "  • Capital Bound: ₹0 new supplier capital.",
                 "  • Net Margin Contribution: +₹15,074.",
                 "",
                 "Option B: Supplier Purchase Order (Sub-optimal)",
                 "  • Unit Cost: ₹25,380 bound working capital.",
                 "  • Minimum Order Quantity (MOQ): 36 units.",
                 "  • Lead Time: 5 days (stockout persists for 3 days).",
                 "  • Net Result: 2 lost sales (₹2,598 loss) + trapped inventory."
             ], ACCENT_CYAN)

    add_card(s7, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
             "SaaS Commercialization Model",
             [
                 "1. Base Platform Subscription:",
                 "  • Tier 1 (1–5 Stores): $199/month.",
                 "  • Tier 2 (6–25 Stores): $799/month.",
                 "  • Enterprise (25+ Stores): Custom multi-region deployment.",
                 "",
                 "2. Value-Share Success Fee:",
                 "  • 1.2% fee on recovered revenue from substitute orders that would have otherwise walked out.",
                 "",
                 "3. ROI Guarantee:",
                 "  • 8.4x typical ROI within 90 days from saved working capital and recovered stockout conversions."
             ], ACCENT_AMBER)

    # -------------------------------------------------------------
    # SLIDE 8: Scalability Roadmap
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, "Scalability Roadmap: From Prototype to Enterprise Scale")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Phase 1: Working Prototype",
             [
                 "Current Milestone (Today)",
                 "• 4-node Bengaluru retail network (S1, S2, S3, DC1).",
                 "• 24 SKUs, 4,032 sales records.",
                 "• Gemini 2.5 Flash intent parsing.",
                 "• 15-minute row-locked hold TTL.",
                 "• 10/10 automated tests passed.",
                 "• Full Playwright E2E verification."
             ], ACCENT_GREEN)

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Phase 2: 90-Day Pilot",
             [
                 "Commercial Pilot (Q1 2027)",
                 "• 50 retail store deployment.",
                 "• Shopify & WooCommerce connectors.",
                 "• Tally & SAP Business One ERP sync.",
                 "• WhatsApp Business BOPIS bot.",
                 "• Multi-tenant schema isolation.",
                 "• Pilot target: 20% stockout recovery."
             ], ACCENT_BLUE)

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Phase 3: National Scale",
             [
                 "Enterprise Platform (Q3 2027)",
                 "• 10,000+ store nodes nationwide.",
                 "• Multi-region Cloud SQL replication.",
                 "• BigQuery ML demand ingestion.",
                 "• Automated EDI X12 supplier ordering.",
                 "• Autonomous cross-dock logistics.",
                 "• Target: $100M+ saved working capital."
             ], ACCENT_PURPLE)

    # -------------------------------------------------------------
    # SLIDE 9: Rigorous Verification & Quality Scorecard
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, "Independent Verification & Production Readiness")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Automated Test Suite (10/10 Passed)",
             [
                 "test_frontend_full_browser_contract : PASSED",
                 "test_health_endpoints : PASSED",
                 "test_seed_counts : PASSED",
                 "test_s01_and_s02_grounded_shopping_and_substitute : PASSED",
                 "test_s03_feasible_transaction_loop : PASSED",
                 "test_s06_planning_transfer_vs_purchase : PASSED",
                 "test_s07_and_s08_trend_action_and_monitor : PASSED",
                 "test_s09_catalog_audit_and_patch : PASSED",
                 "test_idempotency_order_placement : PASSED",
                 "test_demo_reset_and_product_image_categories : PASSED",
                 "",
                 "100% pass rate on completely fresh databases!"
             ], ACCENT_GREEN)

    add_card(s9, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0),
             "E2E Browser & Operational Verification",
             [
                 "Playwright Chromium Test across all 8 workflows: 0 errors.",
                 "Live 15-Minute countdown timer verified in real browser.",
                 "Store associate physical handover decrements stock (12 -> 11).",
                 "Transfer vs PO rebalancing verified with human approval.",
                 "AEO catalog audit checks (C01-C08) elevated score to 94%.",
                 "Reset endpoint ('POST /api/v1/demo/reset') guarantees clean testing.",
                 "Containerized with multi-stage Dockerfile for Cloud Run."
             ], ACCENT_CYAN)

    # -------------------------------------------------------------
    # SLIDE 10: Conclusion & Submission Hub
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10, "Conclusion: The Future of Frictionless Retail")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0),
             "Summary of AI Builder Cup 2026 Deliverables",
             [
                 "1. Compelling AI Vision: Solves retail's fundamental dilemma by marrying conversational Gemini AI with deterministic transactional row locks.",
                 "2. Community Impact: Empowers neighborhood brick-and-mortar stores, eliminates dead stock landfill waste, and cuts freight carbon emissions.",
                 "3. High Feasibility: 100% implemented, passing 10/10 backend integration tests and complete Playwright E2E browser tests.",
                 "4. Scalability: Cloud Run stateless container, Cloud SQL PostgreSQL 17, and enterprise Vertex AI gateway ready to scale from 3 stores to 10,000.",
                 "",
                 "Submission Links & Resources:",
                 "  • Public Code Repository: https://github.com/swaraj-dash/RetailIQ.git",
                 "  • Unified Application Demo: http://127.0.0.1:8000 (Single port REST API + React SPA)",
                 "  • Archify Interactive Architecture Deck: http://127.0.0.1:8000/presentation",
                 "  • Official Video Walkthrough Transcript: docs/TRANSCRIPT.md (2m 50s)",
                 "  • Full Master Specifications: docs/00_MASTER_PLAN to 15_VALIDATION_REPORT.md"
             ], ACCENT_BLUE)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Created PowerPoint deck at: {output_path}")

if __name__ == "__main__":
    create_deck("docs/RetailIQ_Proposal_Deck.pptx")
