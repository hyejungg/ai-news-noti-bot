from mongoengine import connect
from config import config

from models import Site, Message


def connect_db():
    try:
        if config.PROFILE == "real":
            connect(host=config.MONGO_DB_REAL_URI)
        elif config.PROFILE == "develop":
            connect(host=config.MONGO_DB_DEV_URI)
        else:
            connect(host=config.MONGO_DB_LOCAL_URI)

        print("MongoDB Connected ...")

        # 컬렉션 생성 확인
        Site.ensure_indexes()
        print("Site Collection is ready!")
        Message.ensure_indexes()
        print("Message Collection is ready!")

    except Exception as err:
        print(f"MongoDB connect error: {err}")
        exit(1)


if __name__ == "__main__":
    connect_db()
