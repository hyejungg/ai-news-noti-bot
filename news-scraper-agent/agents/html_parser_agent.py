import json
import re
from typing import TypedDict, Literal, NotRequired

import boto3

from config.log import create_logger
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
        self.logger = create_logger(self.__class__.__name__)

    def __call__(self, state: SiteState = None) -> SiteState:
        request_body = json.dumps(self.__create_payload())
        try:
            response = self.lambda_client.invoke(
                FunctionName="scraper-lambda",
                InvocationType="RequestResponse",
                Payload=request_body,
            )
            if response["StatusCode"] != 200:
                self.logger.error(response["FunctionError"])
                self.logger.error(response["LogResult"])
                raise Exception("Lambda 호출 실패")

            response_data: list[str] = json.loads(
                json.load(response["Payload"])["body"]
            )["result"]
            if self.site.name == "데보션":
                response_data = self.__parse_devocean_detail(response_data)

            self.logger.info(f"{self.site.name} 파싱 완료")

            state.parser_result[self.site.name] = response_data
        except Exception as e:
            self.logger.error(f"Error occurred while parsing {self.site.name}: {e}")
            state.parser_result[self.site.name] = []
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
                    "selector": ".header-line",
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
                self.logger.error(f"정의되지 않은 페이지 (url: ${url})")
                raise ValueError("정의되지 않은 페이지 입니다.")

    def __parse_devocean_detail(self, result: list[str]):
        title_html = result[0]
        pattern = r"onclick=\"goDetail\(this,'(\d+)',event\)"

        matched = re.search(pattern, title_html)
        if not matched:
            raise ValueError(f"{self.site.name} 파싱 실패")

        detail_page = (
            f"https://devocean.sk.com/blog/techBoardDetail.do?ID={matched.group(1)}"
        )

        body = json.dumps(
            {
                "url": detail_page,
                "content_type": "html",
                "selector": ".toastui-editor-contents",
            }
        )
        response = self.lambda_client.invoke(
            FunctionName="scraper-lambda",
            InvocationType="RequestResponse",
            Payload=body,
        )

        if response["StatusCode"] != 200:
            self.logger.error(response["FunctionError"])
            self.logger.error(response["LogResult"])
            raise Exception("Lambda 호출 실패")

        response_data: list[str] = json.loads(json.load(response["Payload"])["body"])[
            "result"
        ]
        self.logger.info(f"{self.site.name} 상세 페이지 파싱 완료")

        return response_data
