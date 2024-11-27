from typing import Optional

from mongoengine import Document, StringField, ListField, BooleanField, DateTimeField
from pydantic import BaseModel

from utils.time_utils import get_datetime_kst


class Site(Document):
    name = StringField(required=True)
    url = StringField(required=True)
    keywords = ListField(StringField(), required=False)
    verified = BooleanField(required=True, default=False)
    requestedBy = StringField(required=False)

    # timestamps 옵션 대신 createdAt과 updatedAt 필드를 직접 정의
    createdAt = DateTimeField()
    updatedAt = DateTimeField()

    meta = {
        "collection": "sites",
        "indexes": [
            {"fields": ["name"]},
            {"fields": ["url"]},
        ],
        "auto_create_index": True,
        "index_background": True,
        "versionKey": False,  # __v 필드 생성 방지
    }

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = get_datetime_kst()
        self.updatedAt = get_datetime_kst()
        return super(Site, self).save(*args, **kwargs)


class SiteDto(BaseModel):
    name: str
    url: str
    keywords: list[str]
    verified: bool
    requestedBy: str
    createdAt: Optional[str]
    updatedAt: Optional[str]
