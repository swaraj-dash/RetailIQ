# RetailIQ coding-agent instructions

This repository contains the RetailIQ omnichannel inventory and demand platform. Read [docs/00_MASTER_PLAN](docs/00_MASTER_PLAN), [docs/03_DATABASE_AND_DATA_MODEL.md](docs/03_DATABASE_AND_DATA_MODEL.md), [docs/04_API_AND_INTEGRATION_CONTRACTS.md](docs/04_API_AND_INTEGRATION_CONTRACTS.md), [docs/06_FORECASTING_AND_DECISION_ENGINE.md](docs/06_FORECASTING_AND_DECISION_ENGINE.md), [docs/13_SYNTHETIC_DATASET.md](docs/13_SYNTHETIC_DATASET.md), then all remaining files in `docs/` before modification. Follow [docs/TASKS.md](docs/TASKS.md).

1. Inspect existing code, locks, instructions, tools and cloud configuration first. Report exact blockers without printing credentials.
2. Follow the fixed React/Vite, FastAPI, PostgreSQL, Gemini, Firebase Hosting and Cloud Run architecture. Do not silently substitute frameworks, databases, hosting or agent platforms.
3. Pin and resolve dependencies following [14_SOURCES_AND_DEPENDENCIES.md](14_SOURCES_AND_DEPENDENCIES.md). Do not force incompatible peers or install untrusted plugins. Optional MCP failure has a complete CLI fallback.
4. Implement database, API, UI and test contracts together. Generate frontend types from OpenAPI. An unimplemented button is not a working feature.
5. Keep inventory, allocations, forecasts, quantities and financial calculations deterministic. Enforce row locks and idempotency. Never use model-generated stock or money as authority.
6. Validate all model tools and arguments. Tools are read-only. Preserve factual grounding, tenant isolation and prompt-injection boundaries.
7. The public demo uses isolated synthetic workspaces. Real suppliers, payments, couriers and purchases require a separate explicit decision and authorization.
8. Require deliberate human approval for business actions and catalog patches. Approval does not mean stock has been received. A model recommendation never substitutes for approval.
9. Complete the first vertical slice and real PostgreSQL/browser tests before expanding. Run tests at each milestone and record actual failures, passes and skips.
10. Never claim unrun tests, unverified deployment, real retailer impact or live AI when a fallback was used. Keep blocked tasks visible.
11. Maintain docs/DECISIONS.md for version repairs, scope changes and unresolved issues. If authoritative contracts conflict, stop the affected task and resolve all linked contracts together; continue unrelated work.
12. Deploy an early health slice to expose access issues. Complete public functional verification before claiming deployment is done. Keep credentials out of repositories, bundles, logs and recordings.
13. Do not use destructive resets as a general repair. Test fixtures target explicit disposable databases/workspaces. Preserve existing user work and backups.
14. At each milestone, record the commit, tests, remaining risk and next task. Do not implement the full platform in one unverified pass.

Definition of done and precedence: [docs/00_MASTER_PLAN](docs/00_MASTER_PLAN). Tests: [docs/08_TESTING_AND_ACCEPTANCE.md](docs/08_TESTING_AND_ACCEPTANCE.md). Tooling: [docs/10_AGENT_TOOLING_AND_SKILLS.md](docs/10_AGENT_TOOLING_AND_SKILLS.md). Final handoff must distinguish implemented, tested, deployed, simulated and unimplemented capabilities.
