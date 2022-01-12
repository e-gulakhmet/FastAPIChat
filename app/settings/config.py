from functools import lru_cache
from typing import Dict, Type

from app.settings import AppSettings
from app.settings.base import AppEnvTypes, BaseAppSettings
from app.settings.dev import DevAppSettings
from app.settings.prod import ProdAppSettings
from app.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
