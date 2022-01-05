from fastapi import APIRouter


router = APIRouter(tags=['base'])


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}