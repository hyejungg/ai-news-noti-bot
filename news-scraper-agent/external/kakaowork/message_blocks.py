from typing import Optional, Literal

from pydantic import BaseModel


# block 내부에서 추가로 사용되는 Block
class InnerTextBlock(BaseModel):
    type: str = "styled"
    text: str
    bold: Optional[bool] = False
    color: Literal["red", "blue", "gray", "default"] = "default"


class InnerTextUrlBlock(BaseModel):
    type: str = "link"
    text: str
    url: str


class ButtonActionBlock(BaseModel):
    type: Literal[
        "call_modal",
        "exclusive",
        "open_external_app",
        "open_inapp_browser",
        "open_system_browser",
        "submit_action",
    ] = "open_system_browser"
    name: str = "button"
    value: str


class SectionAccessoryBlock(BaseModel):
    type: str = "image_link"
    url: str


# 기본 Block
class HeaderBlock(BaseModel):
    type: str = "header"
    text: str
    style: Literal["red", "blue", "yellow", "white"] = "white"


class DividerBlock(BaseModel):
    type: str = "divider"


class ButtonBlock(BaseModel):
    type: str = "button"
    text: str
    style: Literal["danger", "primary", "default"] = "default"
    action: ButtonActionBlock


class TextBlock(BaseModel):
    type: str = "text"
    text: str = "text sample"
    inlines: list[InnerTextBlock | InnerTextUrlBlock]


class SectionBlock(BaseModel):
    type: str = "section"
    content: TextBlock
    accessory: Optional[SectionAccessoryBlock] = None


class KakaoworkMessageRequest(BaseModel):
    text: str = "카카오워크 메시지"
    blocks: list[HeaderBlock | TextBlock | DividerBlock | SectionBlock | ButtonBlock]
