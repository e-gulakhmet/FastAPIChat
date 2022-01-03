import os

DATABASE_URL = os.getenv("DB_URL", 'postgresql://main:main@db/main_dev')
