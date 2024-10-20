from typing import List, Dict, Any
from models.message import Message

def get_messages(target_titles: List[str]) -> List[Dict[str, Any]]:
    messages = list(Message.objects(status="SEND_MESSAGE_SUCCESS", messages__title__in=target_titles)) #  # QuerySet을 리스트로 변환
    print(f"messages: {messages}")
    return messages

