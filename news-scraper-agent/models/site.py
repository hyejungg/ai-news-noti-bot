from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DateTimeField,
)
from pydantic import BaseModel
from typing import Optional
from utils.time_utils import get_datetime_kst


class Site(Document):
    name = StringField(required=True, db_field="name")
    url = StringField(required=True, db_field="url")
    keywords = ListField(StringField(), required=False, db_field="keywords")
    verified = BooleanField(required=True, default=False, db_field="verified")
    requestedBy = StringField(required=False, db_field="requestedBy")

    # timestamps 옵션 대신 createdAt과 updatedAt 필드를 직접 정의
    createdAt = DateTimeField(db_field="createdAt")
    updatedAt = DateTimeField(db_field="updatedAt")

    meta = {
        "collection": "sites",
        "indexes": [
            {"name": "name_1", "fields": ["name"]},
            {"name": "url_1", "fields": ["url"]},
        ],
        "auto_create_index_on_save": True,  # save 메서드 수행 시 0.26 버전 부터 True가 아니면 insert 불가
        "index_background": True,  # 인덱스를 백그라운드에서 인덱싱해야 하는지
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
