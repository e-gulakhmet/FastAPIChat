from fastapi import FastAPI

from db import init_db
from models.users import User

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
