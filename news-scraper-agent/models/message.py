from typing import Optional

from mongoengine import (
    Document,
    StringField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
)
from pydantic import BaseModel

from utils.time_utils import get_datetime_kst


class MessageContent(EmbeddedDocument):
    name = StringField(required=False, db_field="name")
    title = StringField(required=False, db_field="title")
    url = StringField(required=False, db_field="url")


class Message(Document):
    type = StringField(required=True, db_field="type")
    status = StringField(required=True, db_field="status")
    messages = ListField(EmbeddedDocumentField(MessageContent))

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
