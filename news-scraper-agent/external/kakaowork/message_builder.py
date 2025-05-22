from zoneinfo import ZoneInfo

from datetime import datetime
from typing import List

from graph.state import CrawlingResult, PageCrawlingData
from external.kakaowork.message_blocks import (
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


class KakaoworkMessageBuilder:
    """Utility class for creating Kakaowork message payloads."""

    @staticmethod
    def _build_site_blocks(
        site_name: str, site_data: List[PageCrawlingData]
    ) -> List[HeaderBlock | TextBlock | DividerBlock | SectionBlock | ButtonBlock]:
        """Return blocks representing a single site's news list."""

        blocks: list = [
            TextBlock(
                text=site_name,
                inlines=[InnerTextBlock(text=site_name, bold=True)],
            )
        ]

        inlines = [
            InnerTextUrlBlock(
                text=f"{item.title}\n" if idx == len(site_data) - 1 else f"{item.title}\n\n",
                url=item.url,
            )
            for idx, item in enumerate(site_data)
            if item.title and item.url
        ]

        if inlines:
            blocks.append(SectionBlock(content=TextBlock(inlines=inlines)))
            blocks.append(DividerBlock())

        return blocks

    @staticmethod
    def build(unique_site_news_dict: CrawlingResult) -> KakaoworkMessageRequest:
        """Create a message body from a dictionary of site news."""

        has_news = any(len(data) > 0 for data in unique_site_news_dict.values())

        today = datetime.now(tz=ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

        blocks = [HeaderBlock(text=f"📢 {today} AI 소식", style="blue")]
        if not has_news:
            blocks.append(
                TextBlock(
                    inlines=[InnerTextBlock(text="오늘은 소식이 없어요! 😅", bold=False)]
                )
            )
        else:
            for site_name, site_data in unique_site_news_dict.items():
                if not site_data:
                    continue

                blocks.extend(KakaoworkMessageBuilder._build_site_blocks(site_name, site_data))

        blocks.append(
            ButtonBlock(
                text="사이트 추가하기",
                action=ButtonActionBlock(
                    value="https://d1qbk7p5aewspc.cloudfront.net/index.html"
                ),
            )
        )

        return KakaoworkMessageRequest(text=f"📢 {today} AI 소식", blocks=blocks)
