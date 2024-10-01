from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    ELASTICSEARCH_URL: str
    XML_FILE_PATH: str
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()