from mongoengine import connect
from env_config import config

def connect_db():
    try:
        if config.PROFILE == 'real':
            connect(host=config.MONGO_DB_REAL_URI)
        elif config.PROFILE == 'develop':
            connect(host=config.MONGO_DB_DEV_URI)
        else:
            connect(host=config.MONGO_DB_LOCAL_URI)

        print("MongoDB Connected ...")

        # 모델 import
        from models.site import Site
        from models.message import Message

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
