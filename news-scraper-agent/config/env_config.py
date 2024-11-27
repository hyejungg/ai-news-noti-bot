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
    MODEL_NAME: str
    OPENAI_API_KEY: str

    # crawling llm agent prompt
    CRAWLING_AGENT_PROMPT_EN: str
    CRAWLING_AGENT_PROMPT_KO: str

    # filtering llm agent prompt
    FILTERING_AGENT_PROMPT_EN: str
    FILTERING_AGENT_PROMPT_KO: str

    # sorting llm agent prompt
    SORTING_AGENT_PROMPT_EN: str
    SORTING_AGENT_PROMPT_KO: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


env = Environment()
