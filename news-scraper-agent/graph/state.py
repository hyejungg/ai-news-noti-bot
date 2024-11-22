from pydantic import BaseModel, Field

from models.site import SiteDto


class SortedFilteringData(BaseModel):
    url: str
    title: str
    reason: str


class PageCrawlingData(BaseModel):
    url: str
    title: str


type SortedFilterResult = dict[str, list[SortedFilteringData]]
type CrawlingResult = dict[str, list[PageCrawlingData]]
type ParserResult = dict[str, list[str]]


class SiteState(BaseModel):
    crawling_result: CrawlingResult
    filtering_result: CrawlingResult
    parser_result: ParserResult
    sorted_result: SortedFilterResult


class State(BaseModel):
    sites: list[SiteDto]
    parallel_result: CrawlingResult


class AgentResponse(BaseModel):
    items: list[PageCrawlingData] = Field(
        description="List of agent response items (title, url)"
    )


class SortAgentResponse(BaseModel):
    items: list[SortedFilteringData] = Field(
        description="List of agent response items (title, url, reason)"
    )
