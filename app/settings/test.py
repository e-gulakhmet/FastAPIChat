from app.settings import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    database_url = 'sqlite://:memory:'

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"