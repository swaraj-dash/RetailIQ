# Implementation roadmap

Implement one verified milestone at a time. Estimated total: 6–10 experienced engineer-days. This is a planning estimate, not a deadline promise. Check portal access and eligibility immediately. Check deployment access first and attempt an early cloud health deployment during foundation; complete deployment remains Phase 6.

| Phase | Ordered deliverables | Acceptance gate | Recovery |
|---|---|---|---|
| P1 — Environment | Read contracts; inspect repository and Antigravity; resolve locks; check project, billing and model | Tooling and dependency evidence; live schema probe or precise blocker | Use CLI/manual documentation when optional tools fail |
| P2 — Foundation | Repository, identity, PostgreSQL, migrations, seed, health, tenant context and OpenAPI | Seed counts, migration and authorization tests; early public health check | Continue locally with PostgreSQL if cloud access is blocked |
| P3 — Vertical slice | Need → catalog → ATP → quote → hold → order → stock proposal → trace | S01–S04 in a browser; concurrency and idempotency tests | Explicit filters can support fallback; live AI remains a separate gate |
| P4 — Intelligence | Backtests, ranges, trend caps, transfer/purchase comparison, catalog audit and excess | Golden mathematics and S05–S09; stale approval rejected | Keep synthetic sources; no live data dependency |
| P5 — UX and integration | Associate, shipping, returns, outcomes, mobile and accessibility | AC01–AC11 and AC13; real browser tests | Correct defects before extra visual polish |
| P6 — Deployment | Immutable image, bootstrap job, Cloud Run, Firebase, CORS, secrets and public smoke | Actual URLs; live model; persistent DB; second-browser isolation | Record exact IAM, billing or quota blocker |
| P7 — Readiness | Regression, video, PDF deck, public repository and evidence review | Four deliverables accessible; team checks portal | Disclose incomplete features or continue independently |

## Deadline triage

With at most 24 hours remaining, allocate roughly 2 hours to access and early deployment, 6–8 hours to the vertical slice, 4–6 hours to intelligence and catalog, 2 hours to integration defects, and reserve 3 hours for recording and submission. These estimates may exceed the time available; the team must prioritize honestly.

Preserve stock correctness, meaningful live Gemini use, actual deployment, clear provenance and one complete loop. Defer optional live signals, additional tools and decorative polish. If returns or a broader analytics screen remains unfinished, list it as incomplete; do not quietly redefine full MVP acceptance. Do not wait until the last hour to discover billing or public-service restrictions.

## Parallel work opportunities for the implementing team

After schemas and OpenAPI are fixed, frontend work can use typed contract fixtures while backend stock transactions are implemented. Forecast functions can proceed independently of the Gemini adapter. Cloud provisioning can proceed alongside local work after the authorized project and budget are established. These are team workstream options, not a requirement to spawn autonomous agents.

One integration owner controls contract changes and merge order. Do not independently rewrite the database or API types in separate workstreams. Replace frontend fixtures with actual calls at P3; mock responses do not count as demonstrated functionality. Integrate after each milestone and rerun affected tests.

## Milestone exit protocol

Record commit SHA, commands, actual results, remaining issues and next task IDs. Run targeted tests after changes and the complete critical suite at P3, P5 and P6. Fix a failed gate or mark it blocked; dependent tasks cannot be done. Roll back to a passing commit or compatible cloud revision. Architecture changes require a DECISIONS entry and synchronized contract/test updates. Use `TASKS.md` for individual verifiable work.
