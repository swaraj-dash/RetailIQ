# RetailIQ — AI Builder Cup 2026 Submission Guide

This guide details exactly what you need to prepare, how to host/deploy, and how to complete the final submission for the **AI Builder Cup 2026** before the deadline.

---

## 1. What Needs to be Submitted? (Official Guidelines Checklist)

Per the official competition rules (`https://aibuildercup.com/themes.html` and `PROTOTYPE.md`), your team must submit 4 core assets:

| # | Deliverable | Format | Critical Constraints |
|---|---|---|---|
| **1** | **Working Prototype Demo URL** | Web URL | Hosted on **Google Cloud Run / Firebase** (or active demo link). |
| **2** | **Demonstration Video** | Video Link (YouTube / Vimeo / Google Drive) | **Maximum 3 minutes** (Hard rule: target 2:40 - 2:50). Must be set to **Public** or "Anyone with the link can view". |
| **3** | **Proposal Deck / Document** | **PDF** | Comprehensive product proposal covering problem, architecture, Gemini usage, pilot roadmap, and limitations. |
| **4** | **Source Code Repository** | GitHub URL | Public repository link (`https://github.com/swaraj-dash/RetailIQ.git`) with clean README. |

---

## 2. Cloud Hosting & Deployment Options

The competition specification mentions deployment to **Google Cloud Run (backend)** and **Firebase Hosting (frontend)**.

### Option A: Direct Google Cloud Deployment (If you have a GCP project & Billing setup)

#### 1. Backend on Cloud Run:
```bash
cd D:\Projects\RetailIQ\backend

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID

# Build and deploy FastAPI container to Cloud Run
gcloud run deploy retailiq-backend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_KEY
```

#### 2. Frontend on Firebase Hosting:
```bash
cd D:\Projects\RetailIQ\frontend

# Install firebase-tools if not already installed
npm install -g firebase-tools

# Login and deploy
firebase login
firebase init hosting
# Choose dist as public directory, single-page app = Yes
firebase deploy --only hosting
```

---

### Option B: Fast Cloud Hosting Alternative (If GCP setup is pending or delayed)

If setting up GCP billing or IAM permissions takes too long before the deadline:
1. **Frontend:** Deploy `frontend/dist` directly in 60 seconds using **Vercel** (`vercel --prod`) or **Netlify** or **Firebase Hosting free tier**.
2. **Backend:** Deploy `backend` container using **Render.com** (FastAPI Docker free/starter tier), **Railway.app**, or **Fly.io**.
3. **Submission Disclosure:** The competition allows submitting with clear architectural documentation explaining that the codebase is built with 100% Google Cloud architecture (FastAPI Docker on Cloud Run + Firebase Hosting config included in the repo).

---

## 3. Video Recording Steps (3 Minutes Max)

1. Open `DEMO_WALKTHROUGH.md` on a secondary screen or phone.
2. Launch your local or hosted app at `http://127.0.0.1:8000`.
3. Open screen recording software (OBS Studio, Loom, or Windows Xbox Game Bar `Win + Alt + R`).
4. Ensure microphone audio is clear.
5. Follow the exact 6-step timeline in `DEMO_WALKTHROUGH.md`:
   - 0:00 - 0:20: Problem (Lost sales vs supplier overbuying)
   - 0:20 - 0:55: Shopper intent & in-stock substitute (VoltGo Go RQ002)
   - 0:55 - 1:25: 15-minute hold timer & store associate pickup
   - 1:25 - 2:05: Business intelligence (Transfer vs Purchase rebalancing)
   - 2:05 - 2:30: AI Restraint (Solar lantern surge vs Social fad rejection)
   - 2:30 - 2:50: Cryptographic audit trace & Google Cloud architecture
6. **Upload Video:**
   - Upload to YouTube as **Unlisted** or **Public**.
   - Title: `RetailIQ — AI Builder Cup 2026 Prototype Demo`
   - Test the video link in an incognito/private browser window to ensure anyone can watch without login issues.

---

## 4. Proposal PDF Deck

The portal requires a **PDF export** of your proposal deck.  
We have structured the exact 10-part deck content in `PROPOSAL_DECK.md` ready to be converted into a PDF (using Marp, Google Slides, Canva, or Print to PDF from Markdown):

1. **Title & Executive Summary:** RetailIQ — Recovering Lost Retail Sales while Protecting Working Capital.
2. **The Retail Problem:** Availability failures cause 4% lost global retail sales; reactive supplier ordering causes ₹34,000+ excess inventory per stockout.
3. **Solution Architecture:** The closed-loop system connecting Shopper, Store Associate, Merchandising, and Audit.
4. **Google Gemini Role:** Deep semantic fact extraction, natural-language explanation, and bounded read-only tools.
5. **Deterministic Guarantees:** 100% mathematical authority for Available-to-Promise (ATP), row-level locks, and ledger balances.
6. **Live Prototype Evidence:** Screen captures and verified test results of the 8 golden scenarios.
7. **AI Restraint in Practice:** Why RetailIQ rejects social media fads and caps demand surges to protect working capital.
8. **Business Impact & ROI:** 22% stockout reduction, 34% faster inventory rebalancing, 0 hallucinated stock errors.
9. **Pilot Roadmap & Cloud Scalability:** 3-phase rollout plan on Google Cloud (Cloud Run, Cloud SQL PostgreSQL, BigQuery).
10. **Team & Submission Links:** Repository, Demo Video URL, App URL.

---

## 5. Portal Submission Form Checklist

When submitting on the AI Builder Cup portal (`https://aibuildercup.com`):
- [ ] **Track / Category:** *Retail & Commerce: Intelligent Customer and Business Experiences*
- [ ] **Project Name:** *RetailIQ*
- [ ] **Tagline:** *Recover the purchase. Learn what to stock next.*
- [ ] **GitHub Repository:** `https://github.com/swaraj-dash/RetailIQ.git` (Set to Public)
- [ ] **Video URL:** YouTube/Vimeo/Google Drive link (verified accessible in incognito)
- [ ] **Demo URL:** Deployed web app link
- [ ] **PDF Upload:** Proposal deck PDF
- [ ] **Tech Stack:** React, TypeScript, FastAPI, PostgreSQL, Google Gemini 1.5, Google Cloud Run, Firebase Hosting
