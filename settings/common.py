import os

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+asyncpg://main:main@localhost:5432/main')
