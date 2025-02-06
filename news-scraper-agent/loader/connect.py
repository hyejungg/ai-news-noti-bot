from config.env_config import env
from config.log import NewsScraperAgentLogger
from mongoengine import connect

logger = NewsScraperAgentLogger()


def connect_db():
    try:
        if env.PROFILE == "prod":
            connect(host=env.MONGO_DB_PROD_URI)
        elif env.PROFILE == "develop":
            connect(host=env.MONGO_DB_DEV_URI)
        else:
            connect(host=env.MONGO_DB_LOCAL_URI)

        logger.info(f"MongoDB connected. phase={env.PROFILE}")

    except Exception as err:
        logger.error(f"MongoDB connect error: {err}")
        exit(1)


if __name__ == "__main__":
    connect_db()
