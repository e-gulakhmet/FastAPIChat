from app.settings.app import BaseAppSettings


class TestAppSettings(BaseAppSettings):
    debug: bool = True

    database_url = 'sqlite://:memory:'

    class Config(BaseAppSettings.Config):
        env_file = ".env"