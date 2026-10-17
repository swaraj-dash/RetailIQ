# Antigravity tooling and skills

## Actual inspection and limits

The specification workspace is a ChatGPT/Codex Linux workspace, not the user's Antigravity installation. Executable checks found Node24.19.0, Python3.12.14, npm and uv. Neither `agy` nor `antigravity`, `gcloud`, `firebase`, `docker` or `psql` was on PATH. No application repository or existing AGENTS file was supplied. Consequently **installed Antigravity version, installed extensions/MCP servers and browser capability are unverified**. Documentation support is verified; local compatibility is not.

Do not report tools installed or tested based only on this document. Phase1 records actual product/version via Help→About or available CLI `agy --version`, existing project rules, installed plugin list, allowed providers, terminal approvals and browser controls. If CLI absent but desktop exists, inspect UI; do not install a duplicate IDE to obtain a version string.

## Verified Antigravity mechanisms

Current [rules documentation](https://antigravity.google/docs/rules) supports directory-scoped `AGENTS.md`/`GEMINI.md` and `.agents/rules/*.md`. [Skills documentation](https://antigravity.google/docs/skills) identifies `.agents/skills/<skill>/SKILL.md`, with legacy `.agent/skills` compatibility. Use one project AGENTS file, not conflicting copies of instructions in every mechanism. Copy this package's AGENTS to repository root before implementation and make its links resolve inside `retailiq-spec`.

The official [legacy workflow page](https://antigravity.google/docs/ide/workflows) says current workflows stop working October19, 2026. This handoff therefore does not depend on legacy `.agent/workflows` execution. TASKS and milestone tests are ordinary instructions; optional reusable workflows should be implemented as supported skills after inspecting the installed version.

[MCP](https://antigravity.google/docs/mcp) and [browser](https://antigravity.google/docs/ide/browser) are documented capabilities. Desktop/CLI/IDE installations can differ. Verify one local page inspection and one harmless read-only MCP call before using those integrations. Never extrapolate Codex or Claude installation commands into Antigravity.

## Smallest useful toolset

Essential tools are ordinary language/build/test CLIs plus project instructions. All additional agent plugins/MCPs are optional. Review publisher, source, permissions and any executable hook before installing; record version/commit in `evidence/tooling.md`. Existing compatible installations are preferred. Respect local approval settings; no disabling protection to get deployment working.

| Exact tool/source | Purpose; priority | Activation and compatibility check | Permissions/trust | Verification and manual fallback |
|---|---|---|---|---|
| Antigravity project `AGENTS.md` ([official rules](https://antigravity.google/docs/rules)) | Architecture, review, documentation; essential | Put at repo root; ask agent to restate stack and first gate; installed version must discover it | Local repo read; no global overwrite | Check loaded instructions; paste/read master plan explicitly if discovery unavailable |
| TypeScript compiler / Vite ([Vite](https://vite.dev/guide/)) | React/TS build; essential | Use pinned project dependencies, `npm ci`, `npm run typecheck/build`; not an agent plugin | Package installation runs dependency scripts; inspect lock and sources | Build/typecheck; manual editor/terminal |
| shadcn/ui + Radix ([Vite guide](https://ui.shadcn.com/docs/installation/vite)) | Accessible consistent UI; essential component system | Use reviewed component source and pinned primitives; verify React/Tailwind compatibility before copying | No cloud credentials; review component changes | Keyboard dialogs/forms in Playwright; implement semantic native controls when a nonessential component fails |
| Pytest / FastAPI / Alembic official projects | Python, DB, migrations; essential | Install from `uv.lock`; run migration and T01/T02; no custom “FastAPI agent plugin” assumed | Disposable local DB then scoped cloud DB | CLI test logs; official docs and SQL review |
| Playwright Test ([official guide](https://playwright.dev/docs/intro)) | Browser E2E, responsive; essential | Root pinned package; `npx playwright install chromium`; run one page test | Browser domains only; no personal browser profile | Screenshot+trace+assertions; manual browser run documented if automation blocked, but automated acceptance stays pending |
| axe-core/playwright ([Deque repository](https://github.com/dequelabs/axe-core-npm)) | Accessibility; essential QA dependency | Pinned npm dependency; scan each main route | Local page DOM only | Zero serious/critical; manual keyboard/contrast still required |
| Firebase agent skills ([official guide](https://firebase.google.com/docs/ai-assistance/agent-skills)) | Hosting/Auth conventions; optional recommended | Inspect existing Firebase plugin; Antigravity Customizations→Marketplace→Firebase; alternatively official `npx skills add firebase/agent-skills --agent=antigravity` | Trusted Firebase source; inspect scripts; use same chosen Google project; don't install both routes | Invoke `firebase-hosting-basics` and `firebase-auth-basics`; fallback Firebase CLI+docs |
| Google skills collection ([google/skills](https://github.com/google/skills)) | Cloud model API guidance; optional | Official interactive `npx skills add google/skills`; choose only `Gemini API in Agent Platform` after reviewing source; select project scope and Antigravity | Broad bundle includes irrelevant tools; don't select all; check install artifact against repo | Agent explains current SDK interface and read-only probe; fallback SDK docs+[05](05_AI_AND_AGENT_DESIGN.md) |
| Cloud Run remote MCP server ([official setup](https://docs.cloud.google.com/run/docs/use-cloud-mcp)) | Cloud inspection/deployment troubleshooting; optional | Add remote Streamable HTTP endpoint `https://run.googleapis.com/mcp` in installed client's MCP configuration; verify supported protocol/auth; no invented JSON config | OAuth/IAM, not API key; start `run.readonly` scope and `roles/run.viewer` + `roles/mcp.toolUser`; mutation needs explicit scoped deployment permissions | List known service; fallback exact `gcloud run/logging` commands in [09](09_GOOGLE_CLOUD_DEPLOYMENT.md) |
| Google Cloud CLI ([official install](https://cloud.google.com/sdk/docs/install)) | Provision/deploy/logs; essential | Reuse installed CLI or Cloud Shell; `gcloud version`, active account/project; record version | Human OAuth or short-lived impersonation; no downloaded service-account key | Describe project and enabled APIs; console for account-only actions |
| Firebase CLI ([official CLI guide](https://firebase.google.com/docs/cli)) | Static deploy/Auth emulator; essential | Reuse installed `firebase`; otherwise official npm package `firebase-tools` pinned after version check; `firebase projects:list` | OAuth project access; no repository tokens | List expected project, local emulator; console provider enable and Hosting fallback |
| Native Antigravity browser ([official](https://antigravity.google/docs/ide/browser)) | Interactive inspection; optional | Enable supported browser feature in installed product, open localhost; preserve permission prompts | Restrict domain scope; no personal account browsing | Inspect visible current page; fallback Playwright |

Firebase skills relevant here: `firebase-basics`, `firebase-local-env-setup`, `firebase-hosting-basics`, `firebase-auth-basics`. Do not invoke Firestore, App Hosting or client-side Firebase AI Logic setup; those would change the selected architecture. Installing the Firebase plugin may include extra skills; presence does not authorize their use.

Google's `google-gemini/gemini-skills` repository is a documented source for the Developer API. It is not the default cloud-platform skill here and its README says it is not an officially supported Google product. It does not substitute for current Interactions/provider-specific guidance; the Google Cloud skill collection is preferred for current provider-specific guidance; actual skill identifier must be selected from its retrieved manifest, not invented.

Cloud Run MCP is tooling, not an app runtime. The remote server's current protocol/auth may exceed an old client's support; that is a compatibility blocker for MCP only. The CLI fallback remains complete. No PostgreSQL MCP with production write privileges is necessary.

## Setup order

1. Inspect repo, AGENTS, installed product/version, tool locations and existing credentials without printing them.
2. Validate Node/Python and pin/resolve dependencies as [14](14_SOURCES_AND_DEPENDENCIES.md).
3. Confirm PostgreSQL/local container or supported installed DB; confirm migrations and concurrency behavior.
4. Confirm Google project, billing, IAM and a live model structured-output probe.
5. Add only missing Firebase/Cloud CLI tools. Optionally activate the two relevant Firebase skills; skip optional MCP if setup takes more than 20 minutes near deadline.
6. Run Playwright local smoke; verify native browser only if useful.
7. Record trusted source, exact installed version/commit, permissions, probe result and fallback in `evidence/tooling.md`.

Security review and architecture review are explicit milestone checklists, not invented “security skills.” Documentation maintenance is TASKS/DECISIONS updates and OpenAPI generation, not a mandatory documentation plugin. Extensions for Python/TS/Tailwind may be enabled if already installed and trusted; no unverified extension marketplace IDs are recommended. Tool absence never justifies changing the database, skipping tests or claiming deployment.
