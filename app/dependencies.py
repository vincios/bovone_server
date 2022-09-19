from functools import lru_cache

from sqlalchemy.orm import Session

from .config import Settings
from .database import SessionLocal


def get_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()  # https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache
def get_settings() -> Settings:
    return Settings()
