from config.env_config import env
from config.log import create_logger
from external.kakaowork.client import KakaoworkClient
from graph.state import State, CrawlingResult, PageCrawlingData
from models.message import Message
from models.message import MessageContent, MessageContentDto
from service.message_service import get_messages
from external.kakaowork.message_builder import KakaoworkMessageBuilder

MESSAGE_TYPE = "KAKAOWORK"
SEND_MESSAGE_SUCCESS = "SEND_MESSAGE_SUCCESS"
SEND_MESSAGE_FAIL = "SEND_MESSAGE_FAIL"


class MessageAgent:
    def __init__(self):
        self.logger = create_logger(self.__class__.__name__)

    def __call__(self, state: State) -> None:
        self.logger.info("messageAgent 시작")
        parallel_result = state.parallel_result.copy()

        # 1. db 조회를 위해 list[PageCrawlingData]로 변환
        flatten_parallel_result = [
            page_crawling_data
            for page_crawling_data_list in parallel_result.values()
            for page_crawling_data in page_crawling_data_list
        ]
        self.logger.info(
            f"flatten_parallel_result (len: {len(flatten_parallel_result)}): {flatten_parallel_result}"
        )

        # 2. title만 뽑아서 db 전체 조회해서 이미 보낸 뉴스가 있는지 확인
        target_titles: set[str] = {
            item.title for item in flatten_parallel_result if item.title is not None
        }
        self.logger.info(f"target_titles (len: {len(target_titles)}):  {target_titles}")
        messages = get_messages(list(target_titles))

        # 3. db에서 가져온 messages 중 messages 필드의 title만 추출
        duplicate_message_titles: set[str] = {
            message.title
            for doc in messages
            for message in doc.messages
            if message.title
        }
        self.logger.info(
            f"duplicate_message_titles (len: {len(duplicate_message_titles)}): {duplicate_message_titles}"
        )

        # 4. 중복된 title 제거하여 unique한 뉴스 제목만 추출
        unique_news_titles = target_titles - duplicate_message_titles
        self.logger.info(
            f"unique_news_titles (len: {len(unique_news_titles)}): {unique_news_titles}"
        )

        # 5. 원본 딕셔너리(parallel_result)에서 중복된 value 제거한 새로운 딕셔너리 생성
        unique_parallel_result: CrawlingResult = {
            site_name: [
                PageCrawlingData(title=item.title, url=item.url)
                for item in site_data
                if item.title in unique_news_titles
            ]
            for site_name, site_data in parallel_result.items()
        }
        self.logger.info(
            f"unique_parallel_result (len: {len(unique_parallel_result)}): {unique_parallel_result}"
        )

        # 6. unique_parallel_result를 카카오워크 메세지로 생성
        request = KakaoworkMessageBuilder().build(unique_parallel_result)
        status_code = KakaoworkClient(env.PROFILE).send_message(request)
        status = SEND_MESSAGE_SUCCESS if status_code == 200 else SEND_MESSAGE_FAIL

        # 7. 성공/실패 여부를 db에 기록
        message_dto_list = [
            MessageContentDto(name=site_name, title=data.title, url=data.url)
            for site_name, page_crawling_data in unique_parallel_result.items()
            for data in page_crawling_data
        ]
        message_contents = [
            MessageContent(**dto.model_dump()) for dto in message_dto_list
        ]
        message = Message(
            type=MESSAGE_TYPE,
            status=status,
            messages=message_contents,
        )
        message.save()
