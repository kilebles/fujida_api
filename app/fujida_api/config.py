from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix=''
    )
    

config = Settings()  # type: ignore