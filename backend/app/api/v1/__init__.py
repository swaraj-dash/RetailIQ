from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.shopping import router as shopping_router
from app.api.v1.orders import router as orders_router
from app.api.v1.transfers import router as transfers_router
from app.api.v1.purchase_orders import router as po_router
from app.api.v1.returns import router as returns_router
from app.api.v1.events import router as events_router
from app.api.v1.planning import router as planning_router
from app.api.v1.catalog_ops import router as catalog_ops_router
from app.api.v1.outcomes import router as outcomes_router

api_v1_router = APIRouter()

# Health endpoints mounted at root (unprefixed) per contract, but also included
api_v1_router.include_router(sessions_router)
api_v1_router.include_router(catalog_router)
api_v1_router.include_router(inventory_router)
api_v1_router.include_router(shopping_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(transfers_router)
api_v1_router.include_router(po_router)
api_v1_router.include_router(returns_router)
api_v1_router.include_router(events_router)
api_v1_router.include_router(planning_router)
api_v1_router.include_router(catalog_ops_router)
api_v1_router.include_router(outcomes_router)
