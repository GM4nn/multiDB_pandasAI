from fastapi import APIRouter, Depends
#
# routes
from src.routes.chat import router as ChatRouter

api_router = APIRouter()

api_router.include_router(
    ChatRouter,
    tags=["Chat"],
    prefix="/chat",
)
