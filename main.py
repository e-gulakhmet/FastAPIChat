from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings.common import ALLOW_ORIGINS, ALLOW_HEADERS

from models.users import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=ALLOW_HEADERS,
)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
