from zoneinfo import ZoneInfo

import requests
from config import config
from datetime import datetime

from graph.state import CrawlingResult
from config.log import logger
from type.kakaowork_message import (
    KakaoworkMessageRequest,
    HeaderBlock,
    DividerBlock,
    ButtonBlock,
    ButtonActionBlock,
    TextBlock,
    InnerTextBlock,
    SectionBlock,
    InnerTextUrlBlock,
)

HTTP_METHOD_POST = "POST"
HTTP_CONTENT_TYPE = "application/json"

WEBHOOK_URL_MAP = {
    "real": config.KAWORK_WEBHOOK_REAL_URI,
    "dev": config.KAWORK_WEBHOOK_DEV_URI,
    "local": config.KAWORK_WEBHOOK_LOCAL_URI,
}


class KakaoworkMessageBuilder:
    def __init__(self):
        # none
        pass

    @staticmethod
    def send_message(request: KakaoworkMessageRequest) -> int:
        webhook_url = WEBHOOK_URL_MAP.get(config.PROFILE)
        try:
            response = requests.post(
                webhook_url,
                headers={"Content-Type": "application/json"},
                data=request.model_dump_json(),
            )
            return response.status_code
        except requests.RequestException as e:
            logger.error(f"Error sending message: {e}")
            return 500  # 에러 상태 코드 반환

    @staticmethod
    def build(unique_site_news_dict: CrawlingResult) -> KakaoworkMessageRequest:
        has_empty_list = any(
            len(page_crawling_data_list) == 0
            for site_name, page_crawling_data_list in unique_site_news_dict.items()
        )
        logger.info(f"has_empty_list: {has_empty_list}")

        today = datetime.now(tz=ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

        blocks = [HeaderBlock(text=f"📢 {today} AI 소식", style="blue")]
        if has_empty_list:
            blocks.append(
                TextBlock(
                    inlines=[
                        InnerTextBlock(text="오늘은 소식이 없어요! 😅", bold=False)
                    ]
                )
            )
        else:
            for site_name, site_data in unique_site_news_dict.items():
                if len(site_data) == 0:
                    continue

                blocks.append(
                    TextBlock(
                        text=site_name,
                        inlines=[InnerTextBlock(text=site_name, bold=True)],
                    )
                )
                inlines = []
                for idx, item in enumerate(site_data):
                    if item.title and item.url:
                        is_last_item = idx == len(site_data) - 1
                        # 가독성을 위해 각 뉴스별 마지막 기사는 구분선(\n) 한 개 더 추가
                        title = (
                            f"{item.title}\n" if is_last_item else f"{item.title}\n\n"
                        )
                        inlines.append(InnerTextUrlBlock(text=title, url=item.url))
                blocks.append(SectionBlock(content=TextBlock(inlines=inlines)))
                blocks.append(DividerBlock())

        blocks.append(
            ButtonBlock(
                text="사이트 추가하기",
                action=ButtonActionBlock(
                    value="https://d1qbk7p5aewspc.cloudfront.net/index.html"
                ),
            )
        )

        return KakaoworkMessageRequest(text=f"📢 {today} AI 소식", blocks=blocks)
