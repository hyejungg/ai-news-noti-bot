from config.log import logger
from models.message import Message
from models.message import MessageDto, MessageContentDto


def get_messages(target_titles: list[str]) -> list[MessageDto]:
    messages_document_list = list(
        Message.objects(
            status="SEND_MESSAGE_SUCCESS", messages__title__in=target_titles
        )
    )  # QuerySet을 리스트로 변환
    messages: list[MessageDto] = [
        MessageDto(
            type=message.type,
            status=message.status,
            messages=[
                MessageContentDto(**msg.to_mongo().to_dict())
                for msg in message.messages
            ],
            createdAt=message.createdAt.isoformat() if message.createdAt else None,
            updatedAt=message.updatedAt.isoformat() if message.updatedAt else None,
        )
        for message in messages_document_list
    ]
    logger.info(f"messages: {messages}")
    return messages
