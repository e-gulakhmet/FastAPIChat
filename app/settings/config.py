from functools import lru_cache
from typing import Dict, Type

from app.settings.app import BaseAppSettings, AppEnvTypes
from app.settings.dev import DevAppSettings
from app.settings.prod import ProdAppSettings
from app.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[BaseAppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_settings() -> BaseAppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
