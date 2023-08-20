from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.handlers import user_router


app = FastAPI(title="Learn app")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)