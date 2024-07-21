import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    SYNC_SERVER_API_URL: str = "http://109.61.16.225:8000"
    CHANNEL: str = "1"
    ITERATION_CYCLE_TIME: int = 3

    class Config:
        env_file = os.environ.get("ENV_FILE_PATH", ".env")


settings = Settings()
