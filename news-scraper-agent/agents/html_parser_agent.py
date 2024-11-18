import json
from typing import TypedDict, Optional, Literal, NotRequired

import boto3

from config.log import logger
from graph.state import SiteState
from models.site import SiteDto


class ParsingLambdaRequestBody(TypedDict):
    url: str
    content_type: Literal["html"] | Literal["json"]
    selector: NotRequired[str]


class HtmlParserAgent:
    def __init__(self, site: SiteDto):
        self.site = site
        self.lambda_client = boto3.client("lambda", region_name="ap-northeast-2")

    def __call__(self, state: SiteState = None) -> SiteState:
        request_body = json.dumps(self.__create_payload())
        response = self.lambda_client.invoke(
            FunctionName="scraper-lambda",
            InvocationType="RequestResponse",
            Payload=request_body,
        )
        if response["StatusCode"] != 200:
            logger.error(response["FunctionError"])
            logger.error(response["LogResult"])
            raise Exception("Lambda 호출 실패")

        response_data: list[str] = json.loads(json.load(response["Payload"])["body"])[
            "result"
        ]
        logger.info(f"{self.site.name} 파싱 완료")
        state.parser_result[self.site.name] = "".join(response_data)
        return state

    def __create_payload(self) -> ParsingLambdaRequestBody:
        match url := self.site.url:
            case url if "news.hada.io" in url:
                return {
                    "url": url,
                    "content_type": "html",
                    "selector": "body > main > article > div.topics > div.topic_row",
                }
            case url if "aitimes.com" in url:
                return {
                    "url": url,
                    "content_type": "html",
                    "selector": "aside.side div.auto-article > div.item",
                }
            case url if "devocean.sk.com" in url:
                return {
                    "url": url,
                    "content_type": "html",
                    "selector": "div.sec-area > ul.sec-area-list01 > li:first-child > div a > h3.pc_view",
                }
            case url if "samsungsds.com" in url:
                return {
                    "url": url,
                    "content_type": "html",
                    "selector": ".cont_list .item strong.md_tit",
                }
            case _:
                logger.error(f"정의되지 않은 페이지 (url: ${url})")
                raise ValueError("정의되지 않은 페이지 입니다.")
