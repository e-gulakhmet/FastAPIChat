from fastapi import FastAPI, APIRouter

from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent


app = FastAPI(title="FastApiChat API", openapi_url="/openapi.json")

api_router = APIRouter()
