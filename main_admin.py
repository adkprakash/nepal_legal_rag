from fastapi import FastAPI

from app.adapter.input.api.v1.health_router import router as health_router

app = FastAPI(title="Nepal Legal RAG - Admin API")

app.include_router(health_router)
