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

from utils import get_datetime_kst


class MessageContent(EmbeddedDocument):
    name = StringField(required=False)
    title = StringField(required=False)
    url = StringField(required=False)


class Message(Document):
    type = StringField(required=True)
    status = StringField(required=True)
    messages = ListField(EmbeddedDocumentField(MessageContent))

    # timestamps 옵션 대신 createdAt과 updatedAt 필드를 직접 정의
    createdAt = DateTimeField()
    updatedAt = DateTimeField()

    meta = {
        "collection": "messages",
        "indexes": [
            {
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
