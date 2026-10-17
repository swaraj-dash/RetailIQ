# Evidence register and dependency freeze

Research date: 17 October 2026. Web pages describe supported products; they do not prove credentials, quotas, installed versions or runtime compatibility in the user's project. All product algorithms and synthetic examples are original engineering specifications, not claims copied from Google documentation.

## Official source register

| ID | Source | Decision supported |
|---|---|---|
| SRC01 | [Competition overview](https://aibuildercup.com/) | Current public status, date, eligibility |
| SRC02 | [Challenges and requirements](https://aibuildercup.com/themes.html) | Retail theme, eligible stack, deliverables, weights |
| SRC03 | [Competition FAQ](https://aibuildercup.com/Faqs.html) | Public repo, video under 3 minutes, fresh-project and team rules |
| SRC04 | [Linked competition terms](https://docs.google.com/document/d/2PACX-1vRm7ChZ6T19fG7uFDkxZUMpwgVBm0n6cMDAEEXE84AI8LBOQ9cYb13S5OzFBbcVb8TF5Ss-eVPiXb/pub) | Team/single-entry conditions; recheck dashboard for private instructions |
| SRC05 | [Gemini 3.5 Flash model](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash) | GA model ID, structured output, function calling, locations, PayGo distinction |
| SRC06 | [Model migration guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate) | Use Google GenAI SDK; legacy Vertex modules no longer suitable |
| SRC07 | [Google GenAI SDK](https://googleapis.github.io/python-genai/) and [maintainer PyPI package](https://pypi.org/project/google-genai/) | Current client interface, structured output, manual tool dispatch, SDK release history |
| SRC08 | [Google model endpoints](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations) and [API service](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest) | Global endpoint/service and region distinctions |
| SRC09 | [Cloud Run locations](https://cloud.google.com/run/docs/locations), [Cloud SQL locations](https://docs.cloud.google.com/sql/docs/postgres/locations) | Mumbai compute/SQL availability |
| SRC10 | [SQL creation flags](https://docs.cloud.google.com/sdk/gcloud/reference/sql/instances/create), [Cloud Run SQL integration](https://docs.cloud.google.com/sql/docs/postgres/connect-run), [Python Unix socket](https://docs.cloud.google.com/sql/docs/postgres/connect-auth-proxy#python) | Provisioning and Cloud SQL socket design |
| SRC11 | [Cloud Run secrets](https://docs.cloud.google.com/run/docs/configuring/services/secrets), [jobs](https://docs.cloud.google.com/run/docs/create-jobs), [job CLI](https://docs.cloud.google.com/sdk/gcloud/reference/run/jobs/deploy) | Versioned secrets, one-off migrations and job deployment |
| SRC12 | [Cloud Build submit](https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit), [SQL user password setup](https://docs.cloud.google.com/sdk/gcloud/reference/sql/users/set-password) | Build/provision command syntax |
| SRC13 | [Hosting quickstart](https://firebase.google.com/docs/hosting/quickstart), [Firebase billing](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans), [token verification](https://firebase.google.com/docs/auth/admin/verify-id-tokens) | Static Hosting, Blaze planning, server token verification |
| SRC14 | [Antigravity rules](https://antigravity.google/docs/rules), [skills](https://antigravity.google/docs/skills), [workflows](https://antigravity.google/docs/ide/workflows), [browser](https://antigravity.google/docs/ide/browser), [MCP](https://antigravity.google/docs/mcp) | Supported documented mechanisms; legacy workflow retirement |
| SRC15 | [Firebase agent skills](https://firebase.google.com/docs/ai-assistance/agent-skills), [Google skills](https://github.com/google/skills), [Gemini Developer skills](https://github.com/google-gemini/gemini-skills) | Trusted skill sources and provider-specific selection |
| SRC16 | [Cloud Run MCP](https://docs.cloud.google.com/run/docs/use-cloud-run-mcp) | Optional official remote endpoint, OAuth/IAM and manual fallback |
| SRC17 | [Google product structured data](https://developers.google.com/search/docs/appearance/structured-data/product) | Factual structured-product representation; no guarantee of rich results |
| SRC18 | [Trends API alpha announcement](https://developers.google.com/search/blog/2025/07/trends-api) | Limited access must not be presumed; not proof this team has access |
| SRC19 | [Vite guide](https://vite.dev/guide/), [shadcn Vite](https://ui.shadcn.com/docs/installation/vite), [shadcn Tailwind 4 / React 19](https://ui.shadcn.com/docs/tailwind-v4), [Tailwind Vite](https://tailwindcss.com/docs/installation/using-vite) | Frontend integration patterns |
| SRC20 | [Playwright](https://playwright.dev/docs/intro), [Deque axe packages](https://github.com/dequelabs/axe-core-npm) | Browser/accessibility tooling |

Pricing/quota pages to recheck at provision time: [Cloud SQL pricing](https://cloud.google.com/sql/pricing), [Cloud Run pricing](https://cloud.google.com/run/pricing), [Firebase pricing](https://firebase.google.com/pricing), [model pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing), [model quotas](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/quotas). No exact bill or quota allocation is asserted here.

## Primary dependency selection

These are exact initial direct-dependency pins, not floating “latest.” Version availability was checked where indicated; a dependency resolver/build was **not run** because registry requests from this workspace returned 403 and no application source was being generated. Phase 1 must produce real lockfiles and run smoke tests. It cannot treat this table as a validated lockfile. This is a concrete remaining verification gate, not permission to redesign the stack.

| Package/runtime | Initial pin | Evidence/status |
|---|---|---|
| Python | 3.12.14 | Available in authoring environment; base image digest must be resolved for deployment |
| Node | 24.19.0 | Available in authoring environment; exceeds Vite's documented baseline |
| PostgreSQL | 17 | Cloud SQL selectable major; local image resolved to immutable digest at implementation |
| fastapi | 0.143.3 | [Maintainer release listing](https://pypi.org/project/fastapi/) |
| pydantic | 2.12.5 | [Version page](https://pypi.org/project/pydantic/2.12.5/) |
| SQLAlchemy | 2.0.48 | [Version page](https://pypi.org/project/SQLAlchemy/2.0.48/) |
| alembic | 1.18.4 | [Version page](https://pypi.org/project/alembic/1.18.4/) |
| psycopg[binary] | 3.3.3 | [Version page](https://pypi.org/project/psycopg/3.3.3/) |
| google-genai | 1.231.0 | SDK release listing; pin below upcoming breaking changes |
| firebase-admin | 7.2.0 | [Version page](https://pypi.org/project/firebase-admin/7.2.0/) |
| uvicorn | 0.41.0 | [Version page](https://pypi.org/project/uvicorn/0.41.0/) |
| httpx | 0.28.1 | [Version page](https://pypi.org/project/httpx/0.28.1/) |
| pytest (dev) | 9.0.2 | [Version page](https://pypi.org/project/pytest/9.0.2/) |
| react / react-dom | 19.3.1 | [React releases](https://github.com/facebook/react/releases); SPA only, no server components |
| vite | 8.3.4 | [Maintainer changelog](https://github.com/vitejs/vite/blob/main/packages/vite/CHANGELOG.md) |
| @vitejs/plugin-react | 6.1.2 | [Maintainer releases](https://github.com/vitejs/vite-plugin-react/releases) |
| typescript | 5.9.3 | [Release](https://github.com/microsoft/TypeScript/releases/tag/v5.9.3); deliberate stable baseline, not claim of latest |
| tailwindcss / @tailwindcss/vite | 4.3.3 | [Maintainer releases](https://github.com/tailwindlabs/tailwindcss/releases) |
| firebase | 12.19.0 | [Maintainer releases](https://github.com/firebase/firebase-js-sdk/releases); stable 12.x baseline for Auth only |
| recharts | 3.10.1 | [Maintainer stable release](https://github.com/recharts/recharts/releases); no canary |
| lucide-react | 1.58.0 | [Maintainer releases](https://github.com/lucide-icons/lucide/releases) |
| @playwright/test (root dev) | 1.64.1 | [Maintainer releases](https://github.com/microsoft/playwright/releases) |

Auxiliary initial pins to verify against registry metadata before install: `@types/react=19.2.2`, `@types/react-dom=19.2.2`, `@types/node=24.10.1`, `react-router-dom=7.6.2`, `@radix-ui/react-dialog=1.1.15`, `@radix-ui/react-alert-dialog=1.1.15`, `@radix-ui/react-select=2.2.6`, `@radix-ui/react-tabs=1.1.13`, `@radix-ui/react-tooltip=1.2.8`, `@radix-ui/react-slot=1.2.3`, `clsx=2.1.1`, `tailwind-merge=3.3.1`, `class-variance-authority=0.7.1`, `openapi-typescript=7.10.1`, `@axe-core/playwright=4.10.2`. These auxiliary pins are proposals pending availability/peer verification; no claim that all were independently release-verified. Prefer native HTML controls when an extra primitive is unnecessary. No separate state/query library required: typed fetch wrapper and React state are enough for this dataset.

## Deterministic dependency freeze procedure

1. Inspect existing package/lockfiles. If none, write the exact primary pins to `frontend/root package.json` and `backend/pyproject.toml`. Python requires `>=3.12,<3.13`. Node engines require `24.x`. Use package-manager-specific files only; do not mix npm and pnpm lockfiles.
2. Inspect `npm view <name>@<pin> version engines peerDependencies --json` for every direct frontend/root dependency. Resolve auxiliary pins with this table first. If a proposed auxiliary version does not exist, choose the lowest published non-prerelease patch in its stated major/minor line that satisfies peers; if no such version exists, choose the lowest compatible minor within the same major and record exact rationale. Do not upgrade across major versions or swap libraries without a DECISIONS entry.
3. Run `npm install --package-lock-only --ignore-scripts` in frontend and root, inspect resolution, then `npm ci`. Do not use `--force` or `--legacy-peer-deps` to hide incompatibility. Use `uv lock --project backend`, inspect, then `uv sync --project backend --frozen --all-groups`. Run `uv pip check --python backend/.venv/bin/python`.
4. If a primary pin conflicts, preserve framework/DB major; select the smallest documented compatible patch/minor of the conflicting package only. Record rejected constraint and selected pin in DECISIONS, then rerun only relevant smoke tests and lock resolution. If no compatible version exists, mark blocked rather than silently altering architecture.
5. Build one React page with Tailwind+dialog+chart; import FastAPI, Pydantic, SQLAlchemy, psycopg, GenAI/Firebase; run migration and live model schema probe. Run audit tools and resolve material vulnerabilities. Existing version evidence is not a security audit.
6. Commit package-lock.json, uv.lock, resolved base-image digests and installed gcloud/Firebase/uv versions to `evidence/dependencies.md`. Future installs use `npm ci`/`uv --frozen`; no unreviewed refresh during demo recording.

Cloud CLIs are operator tools rather than runtime libraries; inspect already-installed versions first, use supported official installers if absent, record exact version after install and verify commands with `--help`. No made-up Cloud Run MCP npm package or Antigravity extension ID is required.

## Research limitations

Some direct GitHub tag/PyPI JSON requests failed; maintainer release pages supplied current primary versions. Registry resolution and dependency security checks remain pending. Competition portal and user enrollment were not accessed. Regional service documentation confirms availability, not project entitlement/capacity. Future Trends or merchant integrations require fresh access verification. These limitations are explicit in [15](15_VALIDATION_REPORT.md).
