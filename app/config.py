from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = "./.env"
