import os

# Basic
ALLOW_ORIGINS = ['*']
ALLOW_HEADERS = ['*']

# DATABASE
DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+asyncpg://main:main@localhost:5432/main')

# JWT
JWT_SECRET = os.getenv('JWT_SECRET', 'fake_secret')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')
ALGORITHM = ''


