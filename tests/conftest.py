import os

import pytest
from tortoise import Tortoise

from app.initializer import init_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():

    init_db(app)
    yield
    await Tortoise._drop_databases()
