# RetailIQ — Rapid Google Cloud Run & Firebase Deployment Guide
## AI Builder Cup 2026 · Working Prototype Submission

This guide provides the exact steps to deploy the RetailIQ functional prototype to **Google Cloud Run** and **Firebase Hosting**.

---

### Why Cloud Run is the Recommended Deployment Option
RetailIQ is architected with a **production-ready multi-stage container** (`Dockerfile`):
- **Stage 1**: Builds the React 18 / Vite frontend into optimized static assets.
- **Stage 2**: Packages the Python 3.12 FastAPI backend, mounts the static frontend at `/`, and exposes port `8080`.
- **Result**: A single, self-contained Cloud Run service serves both the interactive UI and the real-time AI/inventory APIs from one public HTTPS endpoint.

---

## 🚀 Option A: Google Cloud Shell (Fastest & Zero Setup — 3 Minutes)

Because Google Cloud Shell runs directly in your browser with `gcloud`, `git`, and `docker` pre-installed and authenticated, this is the fastest, zero-friction route.

### Step 1: Open Google Cloud Shell
1. Open your browser and navigate to: **[https://shell.cloud.google.com](https://shell.cloud.google.com)**
2. Select your Google Cloud project (ensure Billing is enabled).

### Step 2: Clone the Repository
Run the following in the Cloud Shell terminal:
```bash
git clone https://github.com/swaraj-dash/RetailIQ.git
cd RetailIQ
```

### Step 3: Deploy to Cloud Run with 1 Command
```bash
gcloud run deploy retailiq \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY"
```
*(Replace `YOUR_GEMINI_API_KEY` with your Google AI Studio or Vertex AI Gemini API key. If left blank, RetailIQ gracefully runs with its fact-grounded fallback).*

### Step 4: Verify Deployment
When the deployment finishes, Cloud Run outputs your live service URL:
```
Service URL: https://retailiq-xxxxxxxx-el.a.run.app
```
Test the live health endpoints:
```bash
curl https://retailiq-xxxxxxxx-el.a.run.app/health/ready
curl https://retailiq-xxxxxxxx-el.a.run.app/api/v1/planning/dashboard
```
Open `https://retailiq-xxxxxxxx-el.a.run.app` in any browser to interact with the full live prototype!

---

## 💻 Option B: Deploy Locally from Your Machine

If you prefer to deploy directly from your local terminal:

### Step 1: Install Google Cloud SDK (if not already installed)
In PowerShell:
```powershell
winget install Google.CloudSDK
```
*(Or download the installer from [https://cloud.google.com/sdk/docs/install-sdk](https://cloud.google.com/sdk/docs/install-sdk))*.

### Step 2: Authenticate and Set Project
Close and reopen your terminal, then run:
```powershell
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID
```

### Step 3: Enable Necessary APIs
```powershell
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### Step 4: Build and Deploy to Cloud Run
From the root of `D:\Projects\RetailIQ`:
```powershell
gcloud run deploy retailiq --source . --region asia-south1 --allow-unauthenticated --port 8080
```

---

## 🔥 Option C: Deploy Frontend to Firebase Hosting (Optional)

If you wish to use a `*.web.app` domain for the frontend with Firebase Hosting:

1. **Re-authenticate Firebase CLI**:
   ```powershell
   firebase.cmd login --reauth
   ```
2. **Build the production frontend**:
   ```powershell
   cd frontend
   npm run build
   cd ..
   ```
3. **Deploy to Firebase Hosting**:
   ```powershell
   firebase.cmd deploy --only hosting
   ```
   *(The included `firebase.json` automatically routes `/api/**` calls to your Cloud Run service).*

---

## 📋 What to Submit in the Hackathon Portal

Once deployed, provide the following in your **AI Builder Cup 2026** submission form:

1. **Live Prototype URL**: `https://retailiq-xxxxxxxx-el.a.run.app` (or your Firebase URL)
2. **GitHub Repository**: `https://github.com/swaraj-dash/RetailIQ`
3. **Demo Video Link**: (YouTube / Loom / Google Drive link recorded using `docs/FINAL_DEMO_VIDEO_FLOW_AND_TRANSCRIPT.md`)
4. **Architecture Presentation**: Available directly inside your deployed app at `/presentation` or `/architecture`.
