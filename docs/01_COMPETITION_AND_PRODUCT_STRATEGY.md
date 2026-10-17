# Competition and product strategy

Checked against the organizer's public pages on 17 October 2026. Portal access, participant eligibility and submission acceptance were not verified. Sources below are official; product architecture and delivery estimates are our engineering recommendations.

## Official compliance findings

| Topic | Verified public instruction | Required team action |
|---|---|---|
| Status | Registration is closed; prototype deadline is October 18, 2026 | Confirm existing registration and dashboard submission access immediately |
| Team | 2–4 people, age 21+, based in JAPAC; students excluded | Check every member; employment does not settle formal student status |
| Build | Functional prototype using eligible Google AI/models or agentic platforms, deployed on Google Cloud through Cloud Run/Firebase | Retain live Gemini evidence and public deployment |
| Deliverables | Proposal deck as PDF; deployed prototype; public video; FAQ additionally specifies public GitHub repository | Provide all four |
| Video | Themes page says three minutes; FAQ says under three minutes | Target 2:50, public YouTube/Vimeo/Drive link |
| Originality | FAQ permits fresh projects built during this hackathon only | Check project start date and disclose prior reusable components |
| Language/theme | English materials; one solution under one theme | Select Retail & Commerce |

Sources: [organizer overview](https://aibuildercup.com/), [challenge and judging page](https://aibuildercup.com/themes.html), [FAQ](https://aibuildercup.com/Faqs.html), [linked terms](https://docs.google.com/document/d/e/2PACX-1vRm7ChZ6Tj9FG7UrDkxzUmpgVebBmnQ6cMDnA1EEX84AiLB0009cYbl35SOzFBbcVb8TF5S5-evPjXb/pub).

Two ambiguities need organizer/dashboard confirmation: the exact deadline time/timezone, and stale category/social-impact text in the submission section that does not match the page's six current themes. Do not switch away from Retail because of that inconsistent text. Team formation is already closed. If not registered, do not assume late admission; obtain organizer confirmation or use this package for independent development. No one was contacted during specification work.

## Eligibility checklist

Team lead records each member's age eligibility, JAPAC residence, employment/entrepreneurship status, current enrollment status, single-team participation and registration acceptance. Keep personal evidence private; store only pass/pending/fail in the project checklist. A student on the roster is a blocking issue pending written organizer clarification, including an employed student. Do not infer graduation from an employment history or describe the team as eligible without evidence.

## Final positioning

RetailIQ is a retail decision workspace joining shopping recovery with future stock and catalog decisions. The demo centers on a shopper looking for a reliable travel power bank under ₹1,500, finding the preferred model unavailable, reserving a verified substitute, and exposing a stockout risk whose best action is a transfer from another store. A second example turns a supported lantern trend into a cautious purchase proposal and rejects a social-only fad.

| Alternative | Strength | Limitation | Decision |
|---|---|---|---|
| General retail copilot | Broad enterprise story | Hard to prove value; easy to become disconnected chat tools | Reject as primary narrative |
| Inventory optimizer only | Clear quantitative evidence | Loses customer intent and discoverability loop | Keep as one capability |
| AEO consultant only | Distinct emerging problem | Visibility and ranking claims hard to verify | Keep fact-quality audit inside platform |
| UNLOST standalone recovery | Immediate customer story | Too narrow for the requested ecosystem | Use journey, retain RetailIQ platform |
| Connected RetailIQ | Customer action explains planning, catalog corrections and outcome tracking | More integration work | Select, with one tightly controlled dataset |

This is differentiated by integration and evidence traceability. Do not claim the category has no competitors or the forecasting method is novel. Novelty should be demonstrated by the live connection between previously separate decisions.

## Judge evidence plan

The official weights are technical/GenAI 40%, problem/impact 25%, innovation 25%, UX 10% ([judging source](https://aibuildercup.com/themes.html)).

| Criterion | Evidence to show | Evidence that does not suffice |
|---|---|---|
| Technical/GenAI | Real model trace; schema validation; transaction trace test; deployed flow; deterministic forecast backtest | A chat bubble labeled AI |
| Problem/impact | Exact stock/route constraints, working substitute order, estimated prevented shortage and working capital comparison | Unqualified uplift percentage |
| Innovation | One intent ID linking need, recommendation, order, demand signal, stock proposal and observed outcome | Many agents with unrelated dashboards |
| UX | Clear confidence, source badges, mobile flow, approval diff, readable failure states | Screenshots of nonfunctional pages |

## Metrics and measurement definitions

| Metric | Definition | Evidence class |
|---|---|---|
| Fulfillment feasibility | Valid quote responses / all quote attempts with a suitable catalog match | Measured in synthetic app |
| Recovery completion | Fulfilled substitute orders linked to `unavailable_preferred` intents with that reason | Observed simulation, not causal saved sales |
| Inventory promise errors | Confirmed orders that cannot consume their allocation; target zero | Correctness invariant |
| Forecast WAPE | Sum absolute holdout error / sum holdout actual units, same origins for both models | Synthetic backtest |
| Estimated avoided lost units | Simulated no-action shortages minus chosen-action shortages over common horizon | Counterfactual estimate |
| Contribution opportunity | Formula in [06_FORECASTING_AND_DECISION_ENGINE.md](06_FORECASTING_AND_DECISION_ENGINE.md), including action logistics and holding | Scenario estimate |
| New capital needed | Newly purchased units × cost + inbound freight | Scenario estimate |
| Catalog quality | Weighted rule pass rate before/after approved patches | Measured rule coverage, not search rank |
| Closed-loop coverage | Orders/proposals with valid source intent/event links / relevant orders/proposals | Traceability measure |

Real impact evaluation later requires a retailer pilot: compare matched stores or randomized eligible requests, define stockout exposure, collect return-adjusted contribution, and measure incremental conversion with confidence intervals. Do not derive actual uplift from seeded transactions.
