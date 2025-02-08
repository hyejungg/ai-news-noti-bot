from mongoengine import (
    Document,
    StringField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    ObjectIdField,
)
from pydantic import BaseModel
from typing import Optional
from utils.time_utils import get_datetime_kst


class MessageContent(EmbeddedDocument):
    _id = ObjectIdField(required=True, db_field="_id")  # _id 필드 추가
    name = StringField(required=False, db_field="name")
    title = StringField(required=False, db_field="title")
    url = StringField(required=False, db_field="url")


class Message(Document):
    _id = ObjectIdField(required=True, db_field="_id")  # _id 필드 추가
    type = StringField(required=True, db_field="type")
    status = StringField(required=True, db_field="status")
    messages = ListField(EmbeddedDocumentField(MessageContent), db_field="messages")

    # timestamps 옵션 대신 createdAt과 updatedAt 필드를 직접 정의
    createdAt = DateTimeField(db_field="createdAt")
    updatedAt = DateTimeField(db_field="updatedAt")

    meta = {
        "collection": "messages",
        "indexes": [
            {
                "name": "createdAt_1",
                "fields": ["createdAt"],
                "expireAfterSeconds": 60 * 60 * 24 * 180,
            }  # 180일 후 만료
        ],
        "auto_create_index_on_save": True,  # save 메서드 수행 시 0.26 버전 부터 True가 아니면 insert 불가
        "index_background": True,  # 인덱스를 백그라운드에서 인덱싱해야 하는지
        "versionKey": False,  # __v 필드 생성 방지
    }

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = get_datetime_kst()
        self.updatedAt = get_datetime_kst()
        return super(Message, self).save(*args, **kwargs)


class MessageContentDto(BaseModel):
    name: str
    title: str
    url: str


class MessageDto(BaseModel):
    type: str
    status: str
    messages: list[MessageContentDto]
    createdAt: Optional[str]
    updatedAt: Optional[str]
