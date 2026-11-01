from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapter.input.api.v1.auth_router import router as auth_router
from app.adapter.input.api.v1.health_router import router as health_router
from core.config import settings

app = FastAPI(title="Nepal Legal RAG - User API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
