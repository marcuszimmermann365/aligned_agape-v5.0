
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.middleware import add_middlewares
from api.health_router import router as health_router
from api.world_state_router import router as world_router
from api.world_catalog_router import router as cat_router

app = FastAPI(title="Agape V5.0 – Empirically Grounded Explorer")

add_middlewares(app)
app.include_router(health_router, prefix="/api")
app.include_router(world_router,  prefix="/api")
app.include_router(cat_router,    prefix="/api")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
