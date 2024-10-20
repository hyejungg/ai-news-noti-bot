from mongoengine import Document, StringField, ListField, BooleanField, DateTimeField
from utils import datetime_kst

class Site(Document):
    name = StringField(required=True)
    url = StringField(required=True)
    keywords = ListField(StringField(), required=False)
    verified = BooleanField(required=True, default=False)
    requested_by = StringField(required=False)

    # timestamps 옵션 대신 created_at과 updated_at 필드를 직접 정의
    created_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {
        'collection': 'sites',
        'indexes': [
            {'fields': ['name']},
            {'fields': ['url']},
        ],
        'auto_create_index': True,
        'index_background': True,
        'versionKey': False  # __v 필드 생성 방지
    }

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime_kst()
        self.updated_at = datetime_kst()
        return super(Site, self).save(*args, **kwargs)
