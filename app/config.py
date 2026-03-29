from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_hostname: str = Field("localhost", env="DATABASE_HOSTNAME")
    database_port: str = Field("5432", env="DATABASE_PORT")
    database_password: str = Field("1234", env="DATABASE_PASSWORD")
    db_name: str = Field("postgres", env="DATABASE_NAME")
    database_username: str = Field("postgres", env="DATABASE_USERNAME")
    secret_key: str = Field("some_secret", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        case_sensitive = False
        env_file = ".env"

settings = Settings()
