from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_NAME_TEST: str
    docker_mode: bool = True

    class Config:
        env_file = "./.env"


settings = Settings(docker_mode=True)
