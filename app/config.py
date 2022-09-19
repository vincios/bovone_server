import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    data_csv_file_path: str | None

    class Config:
        env_file = "debug.env" if os.environ.get("BOVONE_DEBUG", False) else ".env"
