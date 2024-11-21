import os

from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config:
    # app
    PROFILE = os.getenv("PROFILE")

    # db
    MONGO_DB_LOCAL_URI = os.getenv("MONGO_DB_LOCAL_URI")
    MONGO_DB_DEV_URI = os.getenv("MONGO_DB_DEV_URI")
    MONGO_DB_REAL_URI = os.getenv("MONGO_DB_REAL_URI")

    # kakaoworks
    KAWORK_WEBHOOK_LOCAL_URI = os.getenv("KAWORK_WEBHOOK_LOCAL_URI")
    KAWORK_WEBHOOK_DEV_URI = os.getenv("KAWORK_WEBHOOK_DEV_URI")
    KAWORK_WEBHOOK_REAL_URI = os.getenv("KAWORK_WEBHOOK_REAL_URI")

    # langsmith
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

    # llm
    MODEL_NAME = os.getenv("MODEL_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # crawling llm agent prompt
    CRAWLING_AGENT_PROMPT_EN = os.getenv("CRAWLING_AGENT_PROMPT_EN")
    CRAWLING_AGENT_PROMPT_KO = os.getenv("CRAWLING_AGENT_PROMPT_KO")

    # filtering llm agent prompt
    FILTERING_AGENT_PROMPT_EN = os.getenv("FILTERING_AGENT_PROMPT_EN")
    FILTERING_AGENT_PROMPT_KO = os.getenv("FILTERING_AGENT_PROMPT_KO")

    # sorting llm agent prompt
    SORTING_AGENT_PROMPT_EN = os.getenv("SORTING_AGENT_PROMPT_EN")
    SORTING_AGENT_PROMPT_KO = os.getenv("SORTING_AGENT_PROMPT_KO")


config = Config()
