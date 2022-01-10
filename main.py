from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import get_settings

import users.routers
import core.routers

app = FastAPI(title="FastAPIChat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=get_settings().allow_headers,
)


app.include_router(users.routers.router, prefix='/users', tags=['users'])
app.include_router(core.routers.router, tags=['base'])
