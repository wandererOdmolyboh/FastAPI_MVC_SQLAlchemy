from pydantic.v1 import BaseSettings

from .config import DB_USER, DB_PASS, DB_HOST, DB_NAME


class Settings(BaseSettings):
    PROJECT_NAME: str = "Test Task"
    DATABASE_URL: str | None = \
        f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    class Config:
        env_file = "../.env"
        case_sensitive = True


settings = Settings()
