from app.settings.app import BaseAppSettings


class ProdAppSettings(BaseAppSettings):
    class Config(BaseAppSettings.Config):
        env_file = ".env"