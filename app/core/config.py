from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str
    db_url: str
    secret: str = 'notasecretatall'
    token_lifetime: int = 3600  # in seconds

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
