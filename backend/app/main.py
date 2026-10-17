import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.services.seed import seed_database, verify_seed
from app.api.v1.health import router as health_router
from app.api.v1 import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and seed
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ws = seed_database(db)
        verification = verify_seed(db, ws.id)
        print(f"[RetailIQ] Workspace initialized: {ws.id}. Seed verified: {verification['all_counts_match']}")
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous Retail Intelligence Platform: Recover the purchase. Learn what to stock next.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unprefixed Health Endpoints (per contract API01, API02)
app.include_router(health_router)

# Versioned API Router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Generate lightweight original demo SVG illustrations for products
@app.get("/images/{filename}")
def get_product_image(filename: str):
    sku = filename.replace(".svg", "")
    colors = {
        "POWER": "#2563EB",
        "LIGHTING": "#F59E0B",
        "AUDIO": "#8B5CF6",
        "ACCESSORIES": "#10B981"
    }
    import re
    num_match = re.search(r'\d+', sku)
    num = int(num_match.group(0)) if num_match else 1

    if 1 <= num <= 4:
        cat = "POWER"
    elif 5 <= num <= 10:
        cat = "LIGHTING"
    elif (11 <= num <= 15) or num == 21:
        cat = "AUDIO"
    else:
        cat = "ACCESSORIES"

    color = colors.get(cat, "#3B82F6")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="100%" height="100%">
  <rect width="300" height="300" fill="#F8FAFC" rx="16"/>
  <circle cx="150" cy="130" r="60" fill="{color}" opacity="0.15"/>
  <rect x="110" y="90" width="80" height="80" rx="12" fill="{color}" opacity="0.85"/>
  <text x="150" y="138" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">{sku}</text>
  <text x="150" y="210" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#334155" text-anchor="middle">{cat}</text>
  <text x="150" y="235" font-family="system-ui, sans-serif" font-size="11" fill="#94A3B8" text-anchor="middle">Product illustration</text>
</svg>"""
    return Response(content=svg, media_type="image/svg+xml")

from fastapi.responses import FileResponse, RedirectResponse

docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
if os.path.exists(docs_dir):
    arch_dir = os.path.join(docs_dir, "architecture")
    if os.path.exists(arch_dir):
        app.mount("/architecture", StaticFiles(directory=arch_dir, html=True), name="architecture")
        app.mount("/docs/architecture", StaticFiles(directory=arch_dir, html=True), name="architecture_docs")

    @app.get("/presentation")
    @app.get("/presentation/")
    def presentation_page():
        pres_file = os.path.join(docs_dir, "RetailIQ_Architecture_and_Workflows_Presentation.html")
        if os.path.exists(pres_file):
            return FileResponse(pres_file, media_type="text/html")
        return RedirectResponse("/architecture/")

    @app.get("/proposal")
    @app.get("/proposal/")
    def proposal_page():
        prop_file = os.path.join(docs_dir, "RetailIQ_Proposal_Deck.html")
        if os.path.exists(prop_file):
            return FileResponse(prop_file, media_type="text/html")
        return RedirectResponse("/docs/RetailIQ_Proposal_Deck.pdf")

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    @app.get("/")
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "tagline": "Recover the purchase. Learn what to stock next.",
            "version": "1.0.0",
            "docs_url": "/docs",
            "health_url": "/health/ready",
            "is_demo": True
        }
