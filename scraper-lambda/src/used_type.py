from typing import TypedDict, Literal, NotRequired


class RequestBody(TypedDict):
    url: str
    content_type: Literal["html", "json"]
    selector: NotRequired[str]
