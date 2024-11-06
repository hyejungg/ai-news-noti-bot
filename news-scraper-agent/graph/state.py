from typing import Any
from pydantic import BaseModel, Field

from models.site import SiteDto


class CrawlingResult(BaseModel):
    url: str
    title: str


class FilteringResult(BaseModel):
    url: str
    title: str


class ParallelResult(BaseModel):
    url: str
    title: str


class SiteState(BaseModel):
    site: dict[str, Any]
    prompts: list[dict[str, Any]]
    crawling_result: list[CrawlingResult]
    filtering_result: list[FilteringResult]


class State(BaseModel):
    sites: list[SiteDto]
    parallel_results: list[ParallelResult]
    send_messages: list[dict[str, Any]]


class AgentResponseItem(BaseModel):
    title: str = Field(description="Title of the agent response item")
    url: str = Field(description="URL of the agent response item")


class AgentResponse(BaseModel):
    items: list[AgentResponseItem] = Field(description="List of agent response items")
