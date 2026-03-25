# FastAPI application entry point.
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.database import async_session
from app.services.seed import run_all_seeds

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed platforms and skills on startup
    async with async_session() as db:
        await run_all_seeds(db)
    yield


app = FastAPI(
    title="Agent Hunt API",
    description="AI Agent job market analysis — JD collection, parsing, and cross-market insights",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
