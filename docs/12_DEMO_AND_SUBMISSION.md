# Demo and submission

Official requirements are centralized in [01](01_COMPETITION_AND_PRODUCT_STRATEGY.md). This specifies future recordings and screenshots; none were produced in this phase. Use only the synthetic dataset in [13](13_SYNTHETIC_DATASET.md).

## Five-minute live demonstration

Prepare one fresh isolated workspace. Verify seed counts, initial planning, catalog audit, live Gemini and the public URL. Do not preapprove stock movements. Use a second fresh workspace only when showing the untouched numerical example; clearly identify which state is displayed.

| Time | User action | Expected evidence |
|---|---|---|
| 0:00–0:25 | Introduce RetailIQ and its synthetic demo badge | One customer need connects to a retail decision |
| 0:25–1:10 | Select S1 and enter: “I need a 10000 mAh USB-C power bank under ₹1500 for travel, pickup today. I prefer VoltGo Pro.” | RQ001 unavailable; RQ002 is a fact-backed substitute; S1 ATP 10 |
| 1:10–1:40 | Quote RQ002 quantity 1, reserve, place demo order, then fulfill pickup in Associate | ATP 9; on_hand 11; order ID and one allocation |
| 1:40–2:35 | Refresh Business intelligence; open RQ002/S1 proposal and alternatives | Current stock changes the proposal; lead time, new capital and estimated contribution are visible |
| 2:35–3:10 | Approve the demo transfer; dispatch and receive in Associate | Source changes at dispatch; destination changes at receipt; audit/outcome updated |
| 3:10–3:45 | Compare lantern and glow-clip trend cards | Capped lantern demand and PO proposal 18; glow clip is MONITOR with no approval button |
| 3:45–4:20 | Audit RQ002, propose a patch, review facts/diff and approve | Factual content improves; audit score rises; price/stock unchanged |
| 4:20–4:45 | Show RQ021 excess and the forecast baseline/range | Reproducible risk and capital estimates |
| 4:45–5:00 | Open outcomes and the original intent trace | Expected estimates separated from observed demo transactions |

The post-order RQ002 proposal is recalculated; the stated baseline case becomes 33 units. Do not reuse the fresh-workspace 32-unit screenshot. If another action changed donor stock, show stale-proposal refresh rather than overriding the check.

## Submission video: 2 minutes 50 seconds

- 0:00–0:15: Explain the customer availability problem and retailer decision problem.
- 0:15–0:55: Show live need extraction, verified substitute and database-backed hold/order.
- 0:55–1:35: Compare transfer and purchasing, approve and receive, explain working capital.
- 1:35–2:05: Contrast the supported lantern trend with a monitor-only fad.
- 2:05–2:30: Show the catalog patch and connected trace.
- 2:30–2:50: Show actual deployment, meaningful GenAI use, testing evidence, limitations and a pilot plan.

Record the actual running app. Faster navigation is acceptable when faithful; splicing a fixture response into a claim of live Gemini is not. Keep synthetic-data and simulated-action labels visible. Do not state seeded outcomes as real retailer impact. The 2:50 target follows the stricter FAQ requirement of under three minutes.

## Proposal deck outline

The implementing team produces this deck and converts it to PDF; it is not part of this specification-only phase.

1. RetailIQ and the customer/retailer problem.
2. The connected intent, inventory and catalog loop.
3. Shopper and associate journey with verified facts and availability.
4. Deterministic operational decision and worked financial comparison.
5. Gemini responsibilities, grounding, tools and validation boundary.
6. Architecture and deployment with actual URLs and model ID.
7. Test evidence, synthetic limitations and a measured pilot plan.
8. Scalability, next steps, team and public links.

Verify PDF fonts, links and layout. Do not present this Markdown package as the required proposal PDF.

## Screenshots and evidence

Capture the actual match/facts screen, quote/hold, order confirmation, network stock before/after transfer, forecast baseline, decision alternatives, transfer receipt, monitor trends, catalog diff/rescore, outcome trace, mobile view and deployment health. Capture test evidence separately. No screenshots may expose tokens, credentials or personal account details. Captions must distinguish observed simulation transactions from counterfactual estimates.

## Submission checklist

| Check | Owner and evidence | Current status |
|---|---|---|
| Registered team, eligible members and resolved student status | Team lead; private eligibility record | UNVERIFIED |
| Portal cutoff, timezone and theme | Team lead; dashboard | UNVERIFIED |
| Fresh project during event; one entry | Team lead; repository history | UNVERIFIED |
| Public frontend/API work in a clean browser | Engineer; deployment evidence | NOT BUILT |
| Live Google model and all claimed features work | Engineer; model/test evidence | NOT BUILT |
| Public GitHub repository without secrets; reproducible README | Team lead; logged-out link check | NOT CREATED |
| Proposal PDF matches deployed version | Team lead; PDF review | NOT CREATED |
| Public 2:50 video opens logged out | Team lead; YouTube/Vimeo/Drive permission check | NOT CREATED |
| English materials and Retail theme | Team lead; submission preview | PENDING |
| Portal submission accepted | Team lead; confirmation receipt | NOT SUBMITTED |

No public cloud URL or repository existed in the supplied workspace. The implementation handoff must replace pending states with evidence or report the exact blocker. Publishing the repository/video or submitting the entry is a separate authorized team action.
