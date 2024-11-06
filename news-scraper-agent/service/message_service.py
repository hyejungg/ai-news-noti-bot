from typing import Any
from models import Message


def get_messages(target_titles: list[str]) -> list[dict[str, Any]]:
    messages = list(
        Message.objects(
            status="SEND_MESSAGE_SUCCESS", messages__title__in=target_titles
        )
    )  #  # QuerySet을 리스트로 변환
    print(f"messages: {messages}")
    return messages
