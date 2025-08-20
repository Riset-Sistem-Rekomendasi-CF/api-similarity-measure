from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings) :
    DB_HOST : str
    DB_PORT : int
    DB_DATABASE : str
    DB_USERNAME : str
    DB_PASSWORD : str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
