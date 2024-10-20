from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
import operator
from pydantic import BaseModel, Field

class State(TypedDict):
    sites: Annotated[List[Dict[str, Any]], operator.add]
    out_values: Annotated[List[Dict[str, Any]], operator.add]
    prompts: Annotated[List[str], operator.add]

    crawling_result: Annotated[List[Dict[str, Any]], operator.add]
    filtering_result: Annotated[List[Dict[str, Any]], operator.add]
    send_messages: Annotated[List[Dict[str, Any]], operator.add]

class AgentResponseItem(BaseModel):
    title: str = Field(description="Title of the agent response item")
    url: str = Field(description="URL of the agent response item")

class AgentResponse(BaseModel):
    items: List[AgentResponseItem] = Field(description="List of agent response items")
