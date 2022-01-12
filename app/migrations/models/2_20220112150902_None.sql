-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20)  UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "password_hash" VARCHAR(128),
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
