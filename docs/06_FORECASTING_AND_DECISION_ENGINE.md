# Deterministic forecasting and decision engine

Algorithm version `retailiq-v1`. All numerical examples are invented synthetic scenarios. Use Python `Decimal` for money and deterministic rounding; quantity planning uses mathematical ceiling. Persist forecasts to 6 decimals, calculate at full decimal precision before rounding. Convert rupees to paise once at input; display currency with2 decimals. Money round-to-nearest paise with `ROUND_HALF_UP`. Sum before rounding, never round each intermediate daily term.

## 1. Time, demand and availability

Business origin `D` is `workspace.scenario_date`, initially2026-10-17. Daily history uses dates D−56 through D−1. Operational actions use real UTC timestamps for TTL/expiry, and `D` for simulated business date. Do not advance D automatically at midnight. The UI says “Scenario date17 Oct2026; operational clock live.” Today's incomplete sales are excluded from model training; they remain visible as observed outcomes and inventory changes.

Forecast gross fulfilled unit demand, not revenue or sales net of returns. A day with <12 in-stock hours is censored, not zero demand. For training only, replace its units with the median of available same-weekday uncensored prior observations within28 days, falling back to mean uncensored prior28 days. Never use a future day to impute a past training point. If none exist, retain missing and mark LOW. Backtest targets must be uncensored; report exclusion count and never score an imputed target as observed truth.

All zero-sales days with known in-stock exposure are genuine zeros. All missing rows are unknown, not zero. Duplicated sales rows fail the unique key. Cold start (<28 valid training days) uses category per-SKU mean over uncensored locations, or0 if unavailable, with LOW confidence and no bulk purchase.

## 2. Baseline, candidate model and backtest

Model `MA28`: daily forecast is arithmetic mean of preceding28 corrected daily observations; requires at least21 valid values. No weekday multiplier.

Model `SNAIVE7`: day k forecast repeats the most recent observed/corrected value of the same weekday from the prior7 days; needs all7 values. Forecast all28 days by cycling that vector; do not recursively learn from forecast points.

Use four7-day holdouts starting D−28, D−21, D−14 and D−7. At each origin train only on earlier data. Pool valid actual/prediction pairs across the four folds. For each model:

`MAE = sum(abs(actual - prediction))/n`

`WAPE = sum(abs(actual - prediction))/sum(actual)`; if denominator0 return null and compare MAE. Never add epsilon and call it ordinary WAPE.

Select SNAIVE7 only if its pooled error is at least5% lower than MA28 and it has the same valid evaluation dates; otherwise choose MA28. Ties choose MA28. Fewer than14 valid holdout dates -> LOW confidence, keep MA28/COLD. No hyperparameter search. Persist selected model using data through D−1. Baseline metrics always refer to MA28, before trend uplift, on the same dates. No claim that the candidate always wins.

Uncertainty: sort absolute selected-model residuals; `e = residual[ceil(0.8*n)-1]`. If fewer14 residuals, `e=max(1,sqrt(mu))`. For each final forecast `f_d`, display lower=`max(0,f_d-e)`, upper=`f_d+e`. These are **scenario ranges, not calibrated prediction intervals**. Sum daily bounds for scenario simulations, but never label an80% confidence interval. Future production calibration is separate scope.

SKU/category/store rollups sum bottom-level store/SKU points. DC has inventory and incoming supply but no independent sales demand forecast. DC replenishment beyond explicit store proposals is later scope.

## 3. Internal intent normalization

For each SKU/store, let sessions be unique `(session_key,category,store,business_date)` within a period. A session contributes at most one intent unit, even if it has SEARCH, VIEW, COMPARE, CART and CHECKOUT events. PURCHASE is an outcome, not an additional intent. Deduplicate product and category matches to avoid counting one session twice. If no SKU is named, apportion category sessions by that category's prior28-day gross-sales share per SKU, normalized to1; use equal shares for no history. This allocation is deterministic and recorded, not another Gemini estimate.

`N_cur` = eligible sessions in D−7..D−1 plus APP sessions since workspace creation (APP sessions assigned to current D); `N_prev` = eligible sessions in D−14..D−8. Current APP contribution is capped at10% of seeded N_cur (minimum1) for a demo refresh so one session cannot fabricate a market surge. Display raw and capped counts. Compare equal7-day seed windows; label the current-day overlay explicitly. A completed order must not create both a new history demand point and extra independent intent uplift in the same refresh; APP purchase only changes outcomes/stock.

Conversion `c` uses the28 days ending D−8: distinct sessions with a matched purchase / distinct intent sessions, constrained0..0.30. If fewer20 sessions or5 purchase sessions, set internal evidence reliability low and use `c=0` for purchasing decisions. A material growth gate requires `N_cur−N_prev >= max(5,ceil(0.20*N_prev))`. Below it, set `u_i=0`. Above it, internal incremental daily demand `u_i=max(0,N_cur−N_prev)*c/7`. One new shopper is logged and traceable but cannot by itself create a market-growth uplift.

## 4. External trend normalization and bounded uplift

External indices are relative interest, not market size. Only compare current and previous values from the same source/region/category scale. `g=clip((index_cur-index_prev)/max(index_prev,10),0,1)`; reliability `r` is a configured0..1 source-quality value, never model enthusiasm. Stale signal window (>14 days old), mapping confidence<0.8, unknown permission/provenance, or mismatched region -> no external uplift.

For baseline daily mean `mu`, `u_e = mu * min(0.25,0.25*g*r)` **only when the internal sample and material growth gates are met**. Otherwise `u_e=0`. Multiple overlapping external sources use the maximum supported `u_e`, not a sum. Combined uplift `u=min(0.5*mu,u_i+u_e)`. External-only popularity cannot trigger purchase.

Future daily forecast `f_d = baseline_d + u`. If approved promotion applies, multiply by its bounded multiplier, with final value capped at1.5×baseline_d; don't add trend on top of an overlapping promotion as independent evidence. If baseline_d=0 use mu for this cap only when mu>0; fully zero history remains LOW and monitoring only. Seed fixture has no active promotion, so golden figures are unaffected.

Gemini may map “off-grid evening lamp” to LIGHTING and relevant facts. It cannot choose g,r,c,u, quantities or supplier lead time. Raw synthetic versus imported provenance travels with every decision.

## 5. Confidence and no-action gates

Define data completeness `a = uncensored_present_days/56`, accuracy `b = clip(1-WAPE,0,1)` (use0.5 if WAPE null with all-zero actuals), support `s=min(1,N_cur/40)`, source quality `r_eff =1` for history-only planning or external trend reliability when external trend contributes. `score=0.35*a+0.35*b+0.20*s+0.10*r_eff`. HIGH≥0.80, MEDIUM≥0.60, otherwise LOW. This is an evidence score, not a purchase probability. Synthetic data may score HIGH but still displays SYNTHETIC.

Force LOW for cold start, >25% censored/missing days or <14 evaluation pairs. Permit normal purchase/transfer only with MEDIUM/HIGH evidence and positive lower-scenario net benefit, feasible supply and capital cap. Trend buying also requires `N_cur≥20`, valid conversion sample, fresh source and mapping≥0.8. If evidence fails: MONITOR. If evidence is adequate but no candidate has positive benefit or replenishment is unnecessary: NO_ACTION. Quantity0 for both. A TEST_ORDER is only one pack, respecting MOQ, and allowed when MOQ≤one pack, valid internal evidence exists, confidence≥MEDIUM and lower-scenario loss is within a configured ₹500 cap; otherwise monitor. Do not manufacture a small test order below supplier MOQ. A SKU with an observed trend that fails these evidence gates has LOW recommendation confidence (its historical forecast confidence can differ) and receives MONITOR even when its baseline inventory is adequate; ordinary non-trend sufficient-stock cases receive NO_ACTION. Genuine baseline stock risk is assessed independently and is not suppressed by an unrelated weak trend.

## 6. Stock, incoming and day-by-day simulation

ATP semantics are in [03_DATABASE_AND_DATA_MODEL.md](03_DATABASE_AND_DATA_MODEL.md). Base stock `A0=ATP` at snapshot. Open order/transfer allocations are already excluded. Include remaining units of approved POs and approved/in-transit transfers due within horizon; don't count a received/cancelled record again. Source transfer allocations reduce source ATP immediately; destination incoming becomes physical only on receipt. Overdue not-received supply is flagged uncertain and excluded from the guaranteed base scenario until ETA is reconfirmed.

For simulated days d=1..H, receipts arrive at start of day: `available_d=ending_(d-1)+incoming_d+candidate_receipt_d`. `fulfilled_d=min(available_d,f_d)`; `lost_d=max(0,f_d-available_d)`; `ending_d=available_d-fulfilled_d`. Fractional demand is permitted for planning; actual stock/orders stay integer. Lost demand is not backordered. First d with lost_d>0 is stockout_day. Day1 means next business scenario day, not the current-day pickup quote.

Days of cover is ATP/mu (null/infinite label if mu=0); this rough indicator must not override date-sensitive simulation.

Safety units `SS=max(1,ceil(safety_days*mu_final))` when mu_final>0; otherwise0. Default safety_days2. For supplier lead L and review R, target=`ceil(sum(f_d,d=1..L+R))+SS`; forecast horizon extends to max28 or L+R using the fixed model. Net requirement=`max(0,target-ATP-incoming_due_by(L+R))`. Do not subtract orders twice. A transfer quantity can be smaller than net requirement if donor supply is limited, but its downside must be shown.

Excess horizon defaults56; extend selected pattern and same bounded uplift. `excess=max(0,ATP-ceil(sum(f_d,d=1..56))-SS)` and `excess_value=excess*cost`. External uplift should not conceal slow stock when signal is weak. Excess itself is not a promise that markdowns or transfers will sell units.

## 7. Candidate generation and fulfillment

Purchase quantity=`pack*ceil(max(net_requirement,MOQ)/pack)` when net_requirement>0, else0. MOQ need not be a multiple of pack; round upward. Supplier active, delivery destination allowed, capital limit and lead verified. `TEST_ORDER` follows gate above.

For each alternative source, donor protection horizon=`max(recipient evaluationH, donor supplier lead+review days)`, donor protected=`ceil(sum(donor forecast over protection horizon))+donor SS`; donor spare=`max(0,donor ATP-donor protected)`. Do not count incoming donor stock as currently transferable. Candidate transfer qty=`min(net_requirement, donor spare)`. Use one source per proposal, not an unimplemented split shipment. Include DC as a source; reserve a DC protection quantity equal to all existing outbound allocations already excluded from ATP plus an explicitly configured free-stock floor of5 units (do not subtract allocations again). For DC candidate available spare=ATP−5. Limit DC to one chosen transfer proposal at approval time; all proposals are advisory until revalidated.

Transfer feasibility requires active lane, qty>0, no conflict with committed stock and arrival before the recipient's need window when used for shopper fulfillment. Shopper quotes **do not wait for a proposed transfer or unreceived PO**. Only currently available pickup/ship options count. Pickup lead at an enabled store; ship lead from lane1–3. Unknown destination means no shipping quote. Price total and budget must satisfy all hard constraints. Sort eligible options by shortest lead, then customer total, then retailer fulfillment cost, then origin code. Show alternatives; don't silently substitute a different product in a quote.

Product matching first removes unmet hard category/budget/attribute constraints (unknown fact fails a hard requirement). Score remaining candidates: +4 for each distinct soft preference equal to a verified fact after Unicode NFKC normalization, lowercase and whitespace trimming, +2 for ATP at preferred store, +1 for available elsewhere; deterministic tie by price then SKU. Preferred SKU is tried first but an unavailable preferred product yields suitable substitutes with explicit tradeoffs. This score is not an AI confidence number.

## 8. Financial comparison and ranking

Compare every alternative on common14-day demand/receipt scenario, plus lower and upper daily scenarios. Assume constant unit price `p` and cost `c`, excluding taxes and payment fees. Unit gross margin `m=p-c`. Reject replenishment if m≤0. Candidate scenario0 is no action; its lost units are `L0`. Candidate action lost units `La`, recovered units=`max(0,L0-La)`.

Action logistics=`lane_fixed+q*lane_unit` for transfer, supplier freight for purchase. Working capital=`q*c+freight` for purchase; transfer capital0 with transfer expense shown separately. This deliberately distinguishes new inventory investment from operating expense.

Incremental holding cost=`sum(max(0,ending_action_d-ending_noaction_d))*c*annual_rate/365`. Purchase unsold risk=`max(0,ending_action_H-ending_noaction_H)*c*unsold_risk_rate`. Transfer unsold risk0 because units already belong to network; donor opportunity cost is controlled by donor protection, and residual network demand uncertainty is disclosed.

Estimated margin opportunity=`recovered_units*m - logistics - holding_cost - unsold_risk`. This is incremental contribution opportunity, not revenue, not net profit or cash flow. COGS is already in m; do not subtract purchase capital a second time. Downside risk=`max(0,-lower_scenario_margin_opportunity)`; also display unsold units and committed capital even if this formula is0. Expected upside is `max(0,base margin opportunity)`; include signed margin_opportunity separately.

Choose feasible positive lower-scenario benefit with highest base margin opportunity; ties within₹1 choose lower new working capital, then earlier arrival, then source code. Compare NO_ACTION (benefit0,cost0) as a real candidate. Rank chosen proposals by `max(0,benefit_rupees)*confidence_score/(1+days_until_stockout_or14)`. A refresh initially ranks candidates, then selects one mutually exclusive proposal per SKU/store using a virtual source-stock budget. Walk proposed actions in descending priority (tie SKU then store); subtract each selected transfer from that source's spare budget and recompute later candidates against remaining spare. Save only this jointly feasible proposal set for dashboard totals, not physical stock. Real approvals still revalidate stock, versions and protections; competing external mutations can make later proposals stale.

## 9. Reproducible examples

### A. Transfer beats new purchasing

Fresh seed: RQ002/S1 ATP10, constant forecast3/day,6 incoming start of day4, safety6, supplier lead7/review7, MOQ24/pack6, price₹1299, cost₹700, purchase freight₹180. S2 ATP55, donor mean1/day, protection14 and safety2 -> spare39. Transfer lane S2→S1 arrives day1, fixed₹120 +₹8/unit.

Target=14×3+6=48; net=48−10−6=32; transfer32 is feasible; purchase rounds to36. Transfer expense=₹376; purchase capital=₹25,380. No-action loses26 units over14 days, first shortage day6. Transfer loses0 and ends with6; purchase arrives day7, loses2 and ends with12. Recovered units26 vs24. Gross contribution opportunities before logistics/holding/risk are₹15,574 vs₹14,376.

Transfer daily incremental ending stocks relative to no-action:32,32,32,32,32,30,27,24,21,18,15,12,9,6; sum322 unit-days. Holding=322×700×0.20/365=₹123.51. Transfer net=₹15,074.49. Purchase incremental ending stocks:0,0,0,0,0,0,30,27,24,21,18,15,12,9; sum156. Holding=₹59.84; unsold risk=12×700×0.10=₹840. Purchase net=₹13,286.96. The proposal chooses TRANSFER32. These numbers are calculated from the stated scenario, not measured saved sales.

After the demo shopper fulfills1 unit, ATP9. Refresh recomputes target/net to33; purchase remains36. The UI must not keep showing the original32 proposal as approvable; inventory version mismatch requires review of the recomputed proposal.

### B. Supported trend

RQ005/S1 baseline1/day,60 current versus20 prior unique intent sessions, conversion0.10 supported by50 historical sessions and5 purchases, external index30→60 reliability0.8. `u_i=40×0.10/7=0.571428…`; `u_e=1×0.25×1×0.8=0.2`; cap0.5; final1.5/day. Lead4/review7, SS3, ATP6, no incoming: target=ceil16.5+3=20; net14; MOQ12/pack6 -> purchase18. With price₹1499, cost₹800, freight₹150, capital₹14,550. Evaluate lower-scenario benefit before approval; show the capped uplift and sample counts. Do not call this a doubling of sales.

### C. Reject popularity alone

RQ006 has index10→100 but8 current/7 previous sessions, no valid conversion sample, weak mapping/reliability and MOQ120. External uplift0 and purchasing gate fails. Action MONITOR qty0, not purchase120. RQ021/S3 has ATP80, mean0.25/day, SS1: 56-day forecast14, excess65 units, inventory cost₹39,000.

## 10. Catalog audit and discoverability

Rules and weights per SKU: C01 clear title with brand/model10; C02 description contains required verified category facts15; C03 all required typed facts present20; C04 brand+MPN or valid GTIN10; C05 image present10; C06 price>0 and currency INR10; C07 published availability matches network ship-enabled ATP>0 for supported localities15; C08 variant/parent consistency10. Score=100−sum failed weights, floor0. Network availability uses current ATP, never incoming. Audit runs record product version and timestamp.

GTIN is optional when a fictional MPN is present; never invent identifiers. An invalid supplied GTIN is an issue even with MPN; validate check digit deterministically. C02 checks required fact token representations, not an LLM quality score. Attribute inconsistencies are reported for human correction; generated patch cannot modify verified facts.

Patch priority=issue_weight×(1+min(2,recent_7d_affected_sessions/20)); tie by SKU. Title/description patches must cite verified fact IDs. Apply only after human diff approval with product-version check; rerun audit. Structured-data preview constructs Schema.org Product/Offer with name,description,sku,brand,mpn,image when present,price,priceCurrency,availability and a placeholder-free real deployment URL only when configured. Missing URLs/images remain errors; do not invent public merchant URLs. JSON-LD serialization escapes `<` to prevent script breakout.

The SPA demo is `noindex`; JSON-LD preview and rule checks prove export readiness only. Real product landing pages, merchant registration, feed validation against target platform and external visibility measurements are later work. Official structured-data guidance is listed in [14_SOURCES_AND_DEPENDENCIES.md](14_SOURCES_AND_DEPENDENCIES.md). No score guarantees recommendations, ranking or rich-result eligibility.

## 11. Observed demo accounting

On pickup fulfillment or shipment delivery, observed contribution equals `q*(unit_price_minor-unit_cost_minor)+customer_fee_minor-fulfillment_cost_minor`. Recognize it once per order. Return receipt reverses `q*(unit_price_minor-unit_cost_minor)` once; the demo keeps shipping fees/costs unchanged. Damage after inspection records a separate negative `q*unit_cost_minor` adjustment and zero units. Aggregated outcomes include these adjustments, never predicted margin. This simplified synthetic accounting excludes taxes, payment fees and real refund execution.
