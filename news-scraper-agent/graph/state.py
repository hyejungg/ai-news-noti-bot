from pydantic import BaseModel, Field

from models.site import SiteDto


class PageCrawlingData(BaseModel):
    url: str
    title: str


type CrawlingResult = dict[str, list[PageCrawlingData]]
type ParserResult = dict[str, list[str]]


class SiteState(BaseModel):
    crawling_result: CrawlingResult
    filtering_result: CrawlingResult
    parser_result: ParserResult


class State(BaseModel):
    sites: list[SiteDto]
    parallel_result: CrawlingResult


class AgentResponse(BaseModel):
    items: list[PageCrawlingData] = Field(description="List of agent response items")
