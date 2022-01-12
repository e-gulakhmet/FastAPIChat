from app.settings import AppSettings


class ProdAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = ".env"