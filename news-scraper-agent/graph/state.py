from typing import Any
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class CrawlingResult(TypedDict):
    url: str
    title: str


class FilteringResult(TypedDict):
    url: str
    title: str


class ParallelResult(TypedDict):
    url: str
    title: str


class SiteState(TypedDict):
    site: dict[str, Any]
    prompts: list[dict[str, Any]]
    crawling_result: list[CrawlingResult]
    filtering_result: list[FilteringResult]


class State(TypedDict):
    sites: list[dict[str, Any]]
    parallel_results: list[ParallelResult]
    send_messages: list[dict[str, Any]]


class AgentResponseItem(BaseModel):
    title: str = Field(description="Title of the agent response item")
    url: str = Field(description="URL of the agent response item")


class AgentResponse(BaseModel):
    items: list[AgentResponseItem] = Field(description="List of agent response items")
