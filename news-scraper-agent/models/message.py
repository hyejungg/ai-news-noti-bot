from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField
from utils import datetime_kst

class MessageContent(EmbeddedDocument):
    name = StringField(required=False)
    title = StringField(required=False)
    url = StringField(required=False)

class Message(Document):
    type = StringField(required=True)
    status = StringField(required=True)
    messages = ListField(EmbeddedDocumentField(MessageContent))

    # timestamps 옵션 대신 created_at과 updated_at 필드를 직접 정의
    created_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {
        'collection': 'messages',
        'indexes': [
            {'fields': ['created_at'], 'expireAfterSeconds': 60 * 60 * 24 * 180}  # 180일 후 만료
        ],
        'versionKey': False  # __v 필드 생성 방지
    }

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime_kst()
        self.updated_at = datetime_kst()
        return super(Message, self).save(*args, **kwargs)
