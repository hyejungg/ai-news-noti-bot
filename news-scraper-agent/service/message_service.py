from config.log import logger
from models import Message
from models.message import MessageDto


def get_messages(target_titles: list[str]) -> list[MessageDto]:
    messages_document_list = list(
        Message.objects(
            status="SEND_MESSAGE_SUCCESS", messages__title__in=target_titles
        )
    )  # QuerySet을 리스트로 변환
    messages: list[MessageDto] = [
        MessageDto(
            **{
                "type": message.type,
                "status": message.status,
                "message": [MessageDto(**{**message.messages.to_mongo().to_dict()})],
                "createdAt": message.createdAt or None,
                "updatedAt": message.updatedAt or None,
            }
        )
        for message in messages_document_list
    ]
    logger.info(f"messages: {messages}")
    return messages
