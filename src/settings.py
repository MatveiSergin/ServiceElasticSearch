from pydantic_settings import BaseSettings, SettingsConfigDict
from sys import platform


class SettingsFactory:
    @staticmethod
    def get_settings():
        if platform.startswith("win"):
            return WindowsSettings()
        else:
            return LinuxSettings()

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    ELASTICSEARCH_URL: str
    XML_FILE_PATH: str

class WindowsSettings(Settings):
    model_config = SettingsConfigDict(env_file='.env')

class LinuxSettings(Settings):
    model_config = SettingsConfigDict(env_file='src/.env')

settings = SettingsFactory.get_settings()