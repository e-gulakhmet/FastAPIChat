from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import ALLOW_ORIGINS, ALLOW_HEADERS

import users.routers
import core.routers


app = FastAPI(title="FastAPIChat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=ALLOW_HEADERS,
)


app.include_router(users.routers.router, prefix='/users', tags=['users'])
app.include_router(core.routers.router, tags=['base'])
