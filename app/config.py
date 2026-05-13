from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RevenueOps AI for Hospitality"
    environment: str = "local"
    demo_tenant_id: str = "hotel-group-alpha"
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
