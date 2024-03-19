from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str = 'Fake Bank API'
    db_url: str
    secret: str = 'notasecretatall'
    token_lifetime: int = 36000  # in seconds
    enable_kafka: bool = True
    kafka_url: str = 'localhost:9092'
    transaction_topic: str = 'transactions'
    notifications_topic: str = 'notifications'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()  # type: ignore[call-arg]
