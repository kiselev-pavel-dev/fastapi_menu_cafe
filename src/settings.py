from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_DB_TESTS: str
    docker_mode: bool = True
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = "./.env"


settings = Settings(docker_mode=False)
