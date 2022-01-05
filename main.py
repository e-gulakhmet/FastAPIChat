from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings.common import ALLOW_ORIGINS, ALLOW_HEADERS

from routers import users, base


app = FastAPI(title="FastAPIChat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=ALLOW_HEADERS,
)


app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(base.router, tags=['base'])
