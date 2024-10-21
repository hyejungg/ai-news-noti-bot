from typing import List, Dict, Any
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class SiteState(TypedDict):
    site: Dict[str, Any]
    prompts: List[Dict[str, Any]]
    crawling_result: Dict[str, Any]
    filtering_result: Dict[str, Any]

class State(TypedDict):
    sites: List[Dict[str, Any]]
    parallel_results: Dict[str, Any]
    send_messages: List[Dict[str, Any]]

class AgentResponseItem(BaseModel):
    title: str = Field(description="Title of the agent response item")
    url: str = Field(description="URL of the agent response item")

class AgentResponse(BaseModel):
    items: List[AgentResponseItem] = Field(description="List of agent response items")
