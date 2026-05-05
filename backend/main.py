from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from config.database import engine, Base
from contextlib import asynccontextmanager

# Import ALL models so SQLAlchemy registers them
from models import user, api, api_key  # noqa: F401

# Import routers
from routes.auth import router as auth_router
from routes.apis import router as apis_router
from routes.gateway import router as gateway_router
from routes.billing import router as billing_router
from routes.payments import router as payments_router

# Import gateway middleware
from middleware.gateway import gateway_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MeterFlow",
    description="Usage-based API billing platform",
    version="0.5.0",
    lifespan=lifespan
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gateway Middleware
app.middleware("http")(gateway_middleware)

# Routers
app.include_router(auth_router)
app.include_router(apis_router)
app.include_router(gateway_router)
app.include_router(billing_router)
app.include_router(payments_router)


@app.get("/health")
async def health():
    return {
        "status":  "ok",
        "env":     settings.APP_ENV,
        "version": "0.5.0"
    }