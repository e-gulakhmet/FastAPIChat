import os


ALLOW_ORIGINS = ['*']
ALLOW_HEADERS = ['*']
DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+asyncpg://main:main@localhost:5432/main')
