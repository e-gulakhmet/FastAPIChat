from fastapi import APIRouter


router = APIRouter(prefix='/core', tags=['core'])


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}