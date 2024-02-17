from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str
    db_url: str
    secret: str = 'notasecretatall'
    token_lifetime: int = 3600  # in seconds
    kafka_url: str = 'localhost:9092'
    transaction_topic: str = 'transactions'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()  # type: ignore[call-arg]
