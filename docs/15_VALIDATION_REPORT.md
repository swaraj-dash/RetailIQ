# Stage 1 specification validation

Validation date: 17 October 2026. Scope: the specification package and its arithmetic, not an implemented application. No application source, deployment, test recording, PDF deck or submission was requested or produced in this phase.

## Checks actually executed

The local structural/arithmetic check completed successfully: 20 Markdown files, 113 resolving internal file links, balanced fenced blocks, consistent table columns, 40 unique API operations, 24 unique SKU rows, and the stated stock/forecast/financial examples. This is document validation only. The file-link count is a package snapshot and may change as implementation evidence is added.

## Review outcome

The selected architecture, database semantics, 40 HTTP operations, four read-only model tools, screens, deterministic dataset and milestone tasks form a connected implementation specification. The package contains all 17 requested Markdown files plus the dataset, source/dependency register and this report. The ZIP retains the complete retailiq-spec directory.

| Check | Result / evidence class |
|---|---|
| Required filenames and nonempty content | Structural check; all 20 Markdown files required |
| Internal Markdown file references | Structural check; every local target must resolve |
| API operation IDs | Structural check; API01–API40 unique and complete |
| UI endpoint mapping | Review plus ID-reference check; routes map to specified APIs |
| Data model and transactions | Design review: tenant FKs, allocations, quotes, orders, transfer/PO/return states and outcomes are defined |
| AI input/output contracts | Design review: typed extraction/explanations and four bounded read-only tools; no mutation tools |
| Forecast and finance | Independently recalculated synthetic golden examples; no application result claims |
| Dataset completeness | Blueprint count check: 24 SKUs, 4 locations, 96 balances, 72 policies, 4,032 historical sales rows |
| Tech stack consistency | Design review: one React/Vite/FastAPI/PostgreSQL/cloud topology throughout |
| Tool recommendations | Official documentation checked; installed Antigravity compatibility explicitly unverified |
| Dependency pins | Primary release evidence checked; actual resolver/security/build gates pending |
| Deployment runbook | Commands checked against official CLI/docs and reviewed for order, IAM, secrets and connectivity; not executed |
| Fallbacks | Gemini, external signals, optional MCP, browser tooling and cloud access have explicit fallback/blocker behavior |
| Acceptance/roadmap | AC01–AC13 mapped to scenarios/tests and ordered implementation tasks |
| Definition of done | Requires real tests, live API, public deployment and actual submission checks |

A structural pass is not proof that a database migration, browser interaction or cloud command has run successfully. The implementing agent must execute the acceptance gates and replace pending statuses with evidence.

## Corrections made during consistency review

- Centralized signal mapping/provenance fields and return-damage outcome enum in the authoritative database model.
- Fixed existing reservations as ORDER allocations, so fixture quantities do not expire after 15 minutes.
- Added a material-growth threshold so one shopper does not create a market-demand spike; its order still affects stock and traceable outcomes.
- Specified a virtual donor-stock budget so dashboard opportunities do not double-count the same available source units.
- Clarified that current-day rows do not enter complete-day historical model fitting.
- Separated dependency release verification from actual compatibility and installation testing.
- Corrected Markdown table escaping and made the demo/agent handoff instructions readable as ordinary text.

## Reproducible arithmetic checks

Fresh RQ002/S1 scenario: ATP 10; target 48; requirement 32; rounded purchase 36. No action loses 26 units with first shortage on day 6. Transfer 32 loses 0, ends at 6, has 322 incremental unit-days, holding cost 123.51 and contribution opportunity 15,074.49. Purchase 36 arriving day 7 loses 2, ends at 12, has 180 incremental unit-days, holding cost 69.04 and contribution opportunity 13,286.96. With one shopper fulfillment and no material trend change, ATP and transfer requirement remain 33.

Lantern scenario: internal increment 40 × 0.10; external 0.20; capped combined uplift 0.50; final daily demand 1.50; target 20; requirement 14; purchase 18; capital 14,550. Slow speaker: mean 0.25, safety 1, 56-day demand 14, excess 65, value 39,000. These are synthetic scenario calculations, not measured retailer results.

## Unresolved blockers and precise next actions

| ID | What is unknown or blocked | Next action | Can development continue? |
|---|---|---|---|
| B01 | Team eligibility/registration not supplied; employed students may still be excluded | Team lead verifies all members and existing registration; seek organizer clarification for enrollment ambiguity | Yes; submission eligibility remains unconfirmed |
| B02 | Portal cutoff time/timezone and exact private submission form unknown | Open registered-team dashboard and verify current instructions | Yes; reserve submission time |
| B03 | No Google project, billing, IAM credentials or model entitlement verified | Cloud owner supplies/selects authorized project; run early model and deployment probes | Local PostgreSQL work can continue; public deployment cannot be claimed |
| B04 | Actual Antigravity version/installations unavailable in the specification workspace | Inspect user's installation, loaded rules, plugins and browser capabilities | Yes; ordinary CLI/docs workflow remains specified |
| B05 | Registry requests from authoring environment returned 403; no dependency lock resolution executed | Run [14](14_SOURCES_AND_DEPENDENCIES.md) freeze procedure, peer checks, imports, build and security audit | Design complete; implementation foundation gate remains pending |
| B06 | Complete MVP is ambitious for the remaining public deadline window | Prioritize [11](11_IMPLEMENTATION_ROADMAP.md), record unfinished features or continue independently | Yes; no deadline guarantee |
| B07 | Live Trends/merchant/social sources not authorized/available | Use labeled synthetic fixtures; later verify source access and permissions | Yes; core demo is self-contained |

## Assumptions retained

One synthetic retailer per isolated demo workspace; fixed scenario date; INR paise; 24 SKUs; one-SKU shopper cart; full receipt operations; synthetic lanes and lead times; no tax/payment processing; no real orders/suppliers; no production onboarding; forecasting permitted for synthetic facts; confidence scores are heuristic, not calibrated probabilities. Discoverability work is a fact audit and preview, not measured ranking improvement.

## Final execution boundary

This package is ready for the implementer's environment/access/dependency gate. It does not certify runtime compatibility, successful application tests, actual cloud deployment or competition eligibility. No public deployment URL exists from this phase. The final application handoff must include real URLs, lock hashes, test results, and a distinction between implemented, tested, deployed, simulated and unfinished features.
