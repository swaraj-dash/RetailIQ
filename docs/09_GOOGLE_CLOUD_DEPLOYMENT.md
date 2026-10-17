# Google Cloud deployment runbook

These commands are a specification for the implementation phase; no cloud resources were created here. Use Bash in Cloud Shell or a trusted workstation. All `app.cli` commands and container/config files below are deliverables to implement before running this runbook. Do not report a URL until the deployed application is verified.

## Verified topology and prerequisites

Firebase Hosting static SPA → public Cloud Run HTTPS API with application-level Firebase auth → Cloud SQL PostgreSQL through Cloud SQL integration; Gemini via Google Cloud model endpoint. Runtime/SQL/registry region `asia-south1`, model endpoint `global`. Model page lists India regional support but standard pay-as-you-go is listed for `global`/`us`/`eu`, so `global` avoids assuming regional purchasing access. Global model processing is not confined to India. Source references and quotas/pricing links are in `[14] (14_SOURCES_AND_DEPENDENCIES.md)`.

Requirements: billing-enabled project; authorized developer; Google Cloud CLI; Firebase CLI; Node24; Python3.12; npm/uv; Git; local Docker needed for Cloud Build. No free tiers are guaranteed to cover Cloud SQL/model usage. Use Blaze-linked Firebase project; public-IP SQL; if so, stop the rollout and request an administrator-supported configuration, not a policy bypass.

The deployer needs project creation/billing-link permission if creating a project; service usage admin; IAM service-account administration; Cloud SQL admin; Secret Manager admin; Artifact Registry admin; Cloud Build editor; Cloud Run admin; Firebase admin/Hosting admin and Service Account User on the specific build/runtime/migration identities. These setup privileges belong to a human/operator, not the application service identity. Narrow them after setup.

## 1. Project and APIs

Replace the project and billing identifiers with authorized values. Check active identity before any mutation.

```bash
export RETAILIQ_PROJECT='replace-with-your-project-id'
export RETAILIQ_REGION='asia-south1'
export RETAILIQ_BILLING='replace-with-billing-account-id'
gcloud auth list
gcloud projects describe "$RETAILIQ_PROJECT"
```

If the project does not exist, create it (include the authorized organization/folder flag if your organization requires one):

```bash
gcloud projects create "$RETAILIQ_PROJECT" --name='RetailIQ Demo'
gcloud billing projects link "$RETAILIQ_PROJECT" --billing-account="$RETAILIQ_BILLING"
gcloud config set project "$RETAILIQ_PROJECT"
gcloud billing projects describe "$RETAILIQ_PROJECT"
gcloud services enable run.googleapis.com cloudsql.googleapis.com \
  artifactregistry.googleapis.com cloudbuild.googleapis.com \
  aiplatform.googleapis.com firebase.googleapis.com firebasehosting.googleapis.com \
  identitytoolkit.googleapis.com secretmanager.googleapis.com logging.googleapis.com \
  monitoring.googleapis.com iam.googleapis.com storage.googleapis.com
```

For an existing project, skip create/link if already correct, but still select/check project and enabled APIs. Keep billing details out of the public repo. Billing budgets are alerts, not spending caps; set an operator-approved budget and alert recipients in Cloud Billing before provisioning.

## 2. Service identities and artifact repository

```bash
gcloud iam service-accounts create retailiq-api --display-name='RetailIQ runtime'
gcloud iam service-accounts create retailiq-migrate --display-name='RetailIQ migrations'
gcloud iam service-accounts create retailiq-build --display-name='RetailIQ image build'
export RETAILIQ_API_SA="retailiq-api@${RETAILIQ_PROJECT}.iam.gserviceaccount.com"
export RETAILIQ_MIGRATE_SA="retailiq-migrate@${RETAILIQ_PROJECT}.iam.gserviceaccount.com"
export RETAILIQ_BUILD_SA="retailiq-build@${RETAILIQ_PROJECT}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding "$RETAILIQ_PROJECT" \
  --member="serviceAccount:${RETAILIQ_API_SA}" --role=roles/cloudsql.client
gcloud projects add-iam-policy-binding "$RETAILIQ_PROJECT" \
  --member="serviceAccount:${RETAILIQ_API_SA}" --role=roles/aiplatform.user
gcloud projects add-iam-policy-binding "$RETAILIQ_PROJECT" \
  --member="serviceAccount:${RETAILIQ_MIGRATE_SA}" --role=roles/cloudsql.client
gcloud artifacts repositories create retailiq --repository-format=docker \
  --location="$RETAILIQ_REGION" --description='RetailIQ application images'
gcloud artifacts repositories add-iam-policy-binding retailiq --location="$RETAILIQ_REGION" \
  --member="serviceAccount:${RETAILIQ_BUILD_SA}" --role=roles/artifactregistry.writer
gcloud projects add-iam-policy-binding "$RETAILIQ_PROJECT" \
  --member="serviceAccount:${RETAILIQ_BUILD_SA}" --role=roles/logging.logWriter
```

`roles/aiplatform.user` is a practical inference role for the demo; production can narrow to approved model invocation permissions. Runtime gets neither SQL admin nor secret admin. The default Cloud Run service agent handles image pulls; preserve its Google-managed role, do not grant owner to fix a pull problem.

Cloud Build needs source/log storage, separate from application storage:

```bash
export RETAILIQ_BUILD_BUCKET="${RETAILIQ_PROJECT}-retailiq-build"
gcloud storage buckets create "gs://${RETAILIQ_BUILD_BUCKET}" \
  --location="$RETAILIQ_REGION" --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding "gs://${RETAILIQ_BUILD_BUCKET}" \
  --member="serviceAccount:${RETAILIQ_BUILD_SA}" --role=roles/storage.objectAdmin
```

Restrict this bucket to build identities/operator; apply a 7-day object lifecycle policy through the generated `infra/build-bucket-lifecycle.json` (rule Delete with age 7). No uploaded customer files or public bucket access.

## 3. PostgreSQL provisioning and secret creation

```bash
gcloud sql instances create retailiq-db --database-version=POSTGRES_17 \
  --edition=ENTERPRISE --tier=db-custom-1-3840 --region="$RETAILIQ_REGION" \
  --availability-type=ZONAL --storage-type=SSD --storage-size=10 \
  --storage-auto-increase --storage-auto-increase-limit=20 \
  --backup-start-time=20:00 --enable-point-in-time-recovery \
  --deletion-protection
gcloud sql databases create retailiq --instance=retailiq-db
export RETAILIQ_SQL_CONNECTION="${RETAILIQ_PROJECT}:${RETAILIQ_REGION}:retailiq-db"
gcloud sql instances describe retailiq-db --format='value(connectionName)'
```

Do not add `0.0.0.0/0` or any authorized networks. The Cloud SQL Auth Proxy integration authenticates/encrypts socket traffic. A public IP does not require opening direct client access. If the tier/region is unavailable in this project, record the exact error and choose another supported Cloud SQL tier/region through `DECISIONS.md`, keeping PostgreSQL and a colocated backend.

Create random owner/app passwords in a private temporary directory, feed a flags file rather than a password command argument, upload to Secret Manager, then remove local copies. This is operational configuration generation, not application code. Run with shell tracing disabled; never print these files.

```bash
set +x
umask 077
export RETAILIQ_SECRET_DIR="$(mktemp -d)"
python3 - <<'PY'
import json, os, secrets
from pathlib import Path
p = Path(os.environ["RETAILIQ_SECRET_DIR"])
owner = secrets.token_urlsafe(32)
(p / "owner.txt").write_text(owner)
(p / "app.txt").write_text(secrets.token_urlsafe(32))
(p / "owner-flags.json").write_text(json.dumps({"--password": owner}))
PY
gcloud sql users set-password postgres --instance=retailiq-db \
  --flags-file="$RETAILIQ_SECRET_DIR/owner-flags.json"
gcloud secrets create retailiq-db-owner-password --replication-policy=automatic \
  --data-file="$RETAILIQ_SECRET_DIR/owner.txt"
gcloud secrets create retailiq-db-app-password --replication-policy=automatic \
  --data-file="$RETAILIQ_SECRET_DIR/app.txt"
rm -f "$RETAILIQ_SECRET_DIR/owner.txt" "$RETAILIQ_SECRET_DIR/app.txt" \
  "$RETAILIQ_SECRET_DIR/owner-flags.json"
rmdir "$RETAILIQ_SECRET_DIR"
unset RETAILIQ_SECRET_DIR
gcloud secrets add-iam-policy-binding retailiq-db-owner-password \
  --member="serviceAccount:${RETAILIQ_MIGRATE_SA}" --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding retailiq-db-app-password \
  --member="serviceAccount:${RETAILIQ_MIGRATE_SA}" --role=roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding retailiq-db-app-password \
  --member="serviceAccount:${RETAILIQ_API_SA}" --role=roles/secretmanager.secretAccessor
```

On reruns, reuse existing secrets/versions; don't recreate users blindly or overwrite passwords. The postgres secret is restricted to the bootstrap/migration identity; the public runtime never receives it. This administrative credential is necessary to establish initial database/schema ownership and the restricted application role. A production rollout should replace bootstrap access with a dedicated schema-owner migration principal after initialization. Version `1` below is correct only for this first creation; subsequent rotations use the actual returned version number. No `latest` secret version in a stable deployment.

`app.cli bootstrap --seed-template` connects as the instance postgres bootstrap administrator, creates `retailiq_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION` using `APP_DB_PASSWORD`, runs Alembic upgrade, grants only `[03] (03_DATABASE_AND_DATA_MODEL.md)` runtime privileges, seeds the read-only template and verifies it. PostgreSQL role/password SQL must use driver-safe identifier/literal handling, not string concatenation. Grant schema usage and DML on mutable tables; append-only tables INSERT/SELECT only. Default privileges must cover future tables. Runtime cannot modify template rows through service policy; tenant isolation is also API-tested.

## 4. Build the container and run bootstrap job

Backend Dockerfile requirements: Python 3.12 base pinned to resolved image digest; install exact `uv.lock` production dependencies; nonroot UID; app package at `/app/app`; working directory `/app`; Alembic files included; listen on `0.0.0.0` at `PORT`; startup command expands `PORT` safely; no migrations at web-server startup. Exclude `.env`, credentials, evidence with tokens, `.git`, `node_modules` using `.dockerignore` and `.gcloudignore`. Commit source before creating the image tag.

```bash
export RETAILIQ_SHA="$(git rev-parse --short=12 HEAD)"
export RETAILIQ_IMAGE="${RETAILIQ_REGION}-docker.pkg.dev/${RETAILIQ_PROJECT}/retailiq/api:${RETAILIQ_SHA}"
gcloud builds submit backend --tag="$RETAILIQ_IMAGE" --region="$RETAILIQ_REGION" \
  --service-account="projects/${RETAILIQ_PROJECT}/serviceAccounts/${RETAILIQ_BUILD_SA}" \
  --gcs-source-staging-dir="gs://${RETAILIQ_BUILD_BUCKET}/source" \
  --gcs-log-dir="gs://${RETAILIQ_BUILD_BUCKET}/logs"
gcloud run jobs deploy retailiq-bootstrap --image="$RETAILIQ_IMAGE" \
  --region="$RETAILIQ_REGION" --service-account="$RETAILIQ_MIGRATE_SA" \
  --set-cloudsql-instances="$RETAILIQ_SQL_CONNECTION" \
  --set-env-vars="APP_ENV=production,DB_HOST=/cloudsql/${RETAILIQ_SQL_CONNECTION},DB_NAME=retailiq,DB_USER=postgres,DEMO_MODE=true" \
  --set-secrets="DB_PASSWORD=retailiq-db-owner-password:1,APP_DB_PASSWORD=retailiq-db-app-password:1" \
  --command=python --args=-m,app.cli,bootstrap,--seed-template \
  --tasks=1 --parallelism=1 --max-retries=0 --task-timeout=600s
gcloud run jobs execute retailiq-bootstrap --region="$RETAILIQ_REGION" --wait
```

Bootstrap must be idempotent: existing role password is not reset unless rotation explicitly requested; seed-template verifies existing dataset version; migration advisory lock prevents overlapping owners. If migration fails, inspect job logs before deploying web traffic.

## 5. Firebase project, identity and frontend configuration

```bash
firebase login
firebase projects:addfirebase "$RETAILIQ_PROJECT"
firebase apps:create WEB RetailIQ --project "$RETAILIQ_PROJECT"
firebase apps:list --project "$RETAILIQ_PROJECT"
```

If already Firebase-enabled, reuse it. Record the returned web app ID in `RETAILIQ_WEB_APP_ID`; it is a public identifier, not a secret. Retrieve public web configuration:

```bash
export RETAILIQ_WEB_APP_ID='replace-with-returned-web-app-id'
firebase apps:sdkconfig WEB "$RETAILIQ_WEB_APP_ID" --project "$RETAILIQ_PROJECT"
```

In Firebase Console → Authentication → Sign-in method, enable Anonymous. Add the actual Hosting domains under authorized domains if absent. This account-owned provider activation is a documented console step; don't invent a CLI flag. Set API-key application/API restrictions appropriate for Firebase Auth; do not restrict away required identity endpoints. No Firestore database is required.

Generate `infra/api-env.yaml` containing strings: `APP_ENV: production`, `DEMO_MODE: "true"`, `DB_HOST: /cloudsql/<connection-name>`, `DB_NAME: retailiq`, `DB_USER: retailiq_app`, `GOOGLE_CLOUD_PROJECT`, `FIREBASE_PROJECT_ID`, `GOOGLE_CLOUD_LOCATION: global`, `GEMINI_PROVIDER: vertex_ai`, `GEMINI_MODEL` set to a currently supported and approved model ID, `SCENARIO_DATE: "2026-10-17"`, `APP_VERSION` set to Git SHA. Set `CORS_ORIGINS` to a JSON array of exact `https://<actual-project>.web.app` and `https://<actual-project>.firebaseapp.com` origins. No localhost in production; no wildcard origin. Optional custom domain must be explicitly added.

## 6. Deploy backend

```bash
gcloud run deploy retailiq-api --image="$RETAILIQ_IMAGE" \
  --region="$RETAILIQ_REGION" --service-account="$RETAILIQ_API_SA" \
  --execution-environment=gen2 --allow-unauthenticated --ingress=all \
  --add-cloudsql-instances="$RETAILIQ_SQL_CONNECTION" \
  --env-vars-file=infra/api-env.yaml \
  --set-secrets="DB_PASSWORD=retailiq-db-app-password:1" \
  --cpu=1 --memory=512Mi --concurrency=10 --max-instances=3 --min-instances=0 \
  --timeout=60 --port=8080
export RETAILIQ_API_URL="$(gcloud run services describe retailiq-api \
  --region="$RETAILIQ_REGION" --format='value(status.url)')"
curl --fail --silent --show-error "$RETAILIQ_API_URL/health/live"
curl --fail --silent --show-error "$RETAILIQ_API_URL/health/ready"
```

Public transport is required for Firebase browser calls; application endpoints still require valid Firebase bearer token and tenant authorization. Cloud Run IAM tokens and Firebase ID tokens are different. Do not require Cloud Run IAM authentication while expecting browser Firebase tokens to satisfy it. If organization policy blocks public services, a domain/IAP strategy needs an explicit architecture decision and judge access check.

CORS permits GET, POST, DELETE, OPTIONS; allowed headers `Authorization`, `Content-Type`, `Idempotency-Key`; expose request ID and `Retry-After`. Credentials/cookies are false because bearer tokens are used. OPTIONS returns 204 before auth and only for allowed origins. Requests from curl still require auth; CORS is not authorization.

## 7. Build and deploy frontend

Create `frontend/.env.production.local` with public `VITE_API_BASE_URL="$RETAILIQ_API_URL/api/v1"`, `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID`, `VITE_FIREBASE_APP_ID` from returned Firebase config. These values are bundled publicly; never include DB/Gemini credentials. API origin is fixed at build time, so changing it requires rebuild.

```bash
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run build
firebase init hosting --project "$RETAILIQ_PROJECT"
firebase deploy --only hosting --project "$RETAILIQ_PROJECT"
```

For init prompts: existing project; public directory `frontend/dist`; SPA rewrite yes; GitHub Actions no; overwrite `index.html` no. Generated `firebase.json` must specify public `frontend/dist`, ignore hidden/config/node_modules, rewrite `**` to `/index.html`, cache fingerprinted assets immutably and `index.html` no-cache, add `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` and `X-Robots-Tag: noindex`. Set CSP allowing self assets, actual API URL, Firebase Auth/token endpoints, no object embeds, `frame-ancestors 'none'`; test Auth and charts before tightening. No second frontend host and no App Hosting.

Hosting CLI prints actual public URL. Verify it; don't assume a custom site ID equals project ID. If actual domain differs, update CORS, redeploy backend and verify again. Record actual frontend/API URLs, image digest, Git SHA, migration head and model ID in `evidence/deployment.md`.

## 8. Public verification and operations

```bash
curl --fail --silent --show-error "https://${RETAILIQ_PROJECT}.web.app/"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="retailiq-api"' \
  --limit=30 --format=json
BASE_URL="https://${RETAILIQ_PROJECT}.web.app" API_BASE_URL="$RETAILIQ_API_URL/api/v1" \
  npx playwright test --project=chromium --grep '@public-smoke'
```

Use the actual Hosting URL if different. API-client validation: obtain a fresh Firebase anonymous ID token via Firebase client/Auth REST in the test harness; call `POST /demo/sessions` then `GET /products` and `POST /quotes` using token and fresh idempotency keys. Store token only in test process memory; never copy it into evidence. Browser and API-client tests both required. Verify live Gemini model probe under runtime identity using `app.cli probe-ai` as a separate Cloud Run job with API service account and same AI config, or through a real authenticated intent request; health 200 alone does not verify AI access.

Maintenance job uses migration identity and owner DB secret, command `python -m app.cli cleanup --expired-demo-only`. It deletes only expired synthetic workspaces, not template or unexpired state. Run manually after demo; scheduling is optional later. Never implement cleanup as an unauthenticated HTTP endpoint.

## Rollback, cost and troubleshooting

Before rollout capture previous revision and Firebase Hosting release. Roll back backend traffic with `gcloud run services update-traffic retailiq-api --region="$RETAILIQ_REGION" --to-revisions=PREVIOUS_REVISION=100` using the real previous revision name. Firebase Console Hosting release history supports rollback. Migrations are additive/compatible; restore a backup into a separate SQL instance if a destructive data issue occurs. Do not blindly downgrade a live schema.

| Symptom | Inspect / fix |
|---|---|
| Container never listens | `PORT=8080` binding, `0.0.0.0`, nonroot permissions, entrypoint expansion, missing dependency |
| Cloud SQL permission/socket error | `cloudsql.client`, instance attachment, connectionName, secret access, DB grants |
| SQL too many connections | Pool 3 + overflow 2, one worker, max instances 3; fix leaks before raising capacity |
| Gemini 403/404/429 | Vertex AI API, IAM, billing, model ID/global endpoint, quota; show fallback and exact blocker |
| Frontend fetch/CORS | Actual origin allowlist, OPTIONS headers, `VITE_API_BASE_URL` build value, Firebase token audience |
| Anonymous sign-in fails | Provider enabled, authorized domain, key restrictions, Auth quota |
| Build permission denied | Explicit build SA, registry writer, source/log bucket roles, operator `actAs` |
| Static 404 on deep link | SPA rewrite and `dist` path |
| Planning or receipt wrong | Dataset version, scenario date, incoming receipt states, inventory version; never fix by editing UI numbers |

Pricing changes; use official calculators/links rather than invented rupee quotes. Cost drivers: continuously provisioned SQL + disk/backups, token calls, Cloud Run CPU/memory/egress, build minutes, artifact/source/log storage, Hosting bandwidth. App quotas and max instances reduce exposure but do not impose a hard billing ceiling. After judging, operator decides whether to retain data or stop/delete paid demo resources; deletion is never an automatic recovery step. No public deployment URL exists for this specification-only phase.
