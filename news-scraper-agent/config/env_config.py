from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Environment(BaseSettings):
    # app
    PROFILE: str

    # db
    MONGO_DB_LOCAL_URI: str
    MONGO_DB_DEV_URI: str
    MONGO_DB_REAL_URI: str

    # kakaoworks
    KAWORK_WEBHOOK_LOCAL_URI: str
    KAWORK_WEBHOOK_DEV_URI: str
    KAWORK_WEBHOOK_REAL_URI: str

    # langsmith
    LANGCHAIN_ENDPOINT: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: Optional[str] = None

    # llm
    OPENAI_API_KEY: str

    # aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


env = Environment()
