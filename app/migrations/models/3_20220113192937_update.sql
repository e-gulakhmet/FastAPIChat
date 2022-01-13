-- upgrade --
ALTER TABLE "users" RENAME COLUMN "password_hash" TO "hashed_password";
-- downgrade --
ALTER TABLE "users" RENAME COLUMN "hashed_password" TO "password_hash";
