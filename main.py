from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from models.users import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
