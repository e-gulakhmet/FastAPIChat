from fastapi import FastAPI

from models.users import User

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
