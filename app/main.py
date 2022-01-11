from fastapi import FastAPI

from app.settings import app_settings
from app.initializer import init

app = FastAPI(title=app_settings.name)

init(app)
