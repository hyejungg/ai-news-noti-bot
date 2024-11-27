from mongoengine import connect

from config.env_config import env
from config.log import logger
from models.message import Message
from models.site import Site


def connect_db():
    try:
        if env.PROFILE == "real":
            connect(host=env.MONGO_DB_REAL_URI)
        elif env.PROFILE == "develop":
            connect(host=env.MONGO_DB_DEV_URI)
        else:
            connect(host=env.MONGO_DB_LOCAL_URI)

        logger.info("MongoDB Connected ...")

        # 컬렉션 생성 확인
        Site.ensure_indexes()
        logger.info("Site Collection is ready!")
        Message.ensure_indexes()
        logger.info("Message Collection is ready!")

    except Exception as err:
        logger.error(f"MongoDB connect error: {err}")
        exit(1)


if __name__ == "__main__":
    connect_db()
