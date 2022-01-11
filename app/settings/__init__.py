"""Config of application"""
from .db import TortoiseSettings
from .app import AppSettings

tortoise_settings = TortoiseSettings.generate()
app_settings = AppSettings()