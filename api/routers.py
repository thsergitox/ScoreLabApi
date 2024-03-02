from api.endpoints.questionnaires import router as questionnaires_router
from api.endpoints.users import router as users_router

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(questionnaires_router, prefix = "/questionnaires", tags = ["Questionnaires"])
api_router.include_router(users_router, prefix = "/users", tags = ["Users"])
