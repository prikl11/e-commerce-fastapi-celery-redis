from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    access_secret_key: str
    refresh_secret_key: str

    algorithm: str
    access_token_expires_minutes: int

    postgres_user: str
    postgres_password: str
    postgres_db: str

    celery_broker_url: str
    celery_result_backend: str

    mail_server: str
    mail_port: int
    mail_from: str
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool

    stripe_secret_key: str
    stripe_webhook_secret: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()