import os

DB_URL = os.getenv("DB_URL", 'postgresql://main:main@db/main_dev')
