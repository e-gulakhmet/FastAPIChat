from fastapi import FastAPI

from core.app_inits import init_middlewares, register_db, register_routers

app = FastAPI(title="FastAPIChat API")


init_middlewares(app)
register_db(app)
register_routers(app)
