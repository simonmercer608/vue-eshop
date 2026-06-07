from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "vue_eshop"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    cart_ttl_seconds: int = 60 * 60 * 24 * 7

    class Config:
        env_file = ".env"


settings = Settings()
