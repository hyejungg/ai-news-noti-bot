from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

load_dotenv()


class Environment(BaseSettings):
    # app
    PROFILE: str

    # db
    MONGO_DB_LOCAL_URI: str
    MONGO_DB_DEV_URI: str
    MONGO_DB_PROD_URI: str

    # kakaoworks
    KAWORK_WEBHOOK_LOCAL_URI: str
    KAWORK_WEBHOOK_DEV_URI: str
    KAWORK_WEBHOOK_PROD_URI: str

    # langsmith
    LANGCHAIN_ENDPOINT: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: Optional[str] = None

    # llm
    OPENAI_API_KEY: str

    # aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    ENABLE_MESSAGE_AGENT_LOG: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


env = Environment()
