from config.env_config import env
from config.log import ConsoleDataType, NewsScraperAgentLogger
from decorations.log_time import log_time_agent_method
from external.kakaowork.client import KakaoworkClient
from external.kakaowork.message_builder import KakaoworkMessageBuilder
from graph.state import State, CrawlingResult, PageCrawlingData
from models.message import Message
from models.message import MessageContent, MessageContentDto
from rich.table import Table
from service.message_service import get_messages

MESSAGE_TYPE = "KAKAOWORK"
SEND_MESSAGE_SUCCESS = "SEND_MESSAGE_SUCCESS"
SEND_MESSAGE_FAIL = "SEND_MESSAGE_FAIL"


class MessageAgent:
    def __init__(self):
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)

    @log_time_agent_method
    def __call__(self, state: State) -> None:
        parallel_result = state.parallel_result.copy()

        # 1. db 조회를 위해 list[PageCrawlingData]로 변환
        flatten_parallel_result = [
            page_crawling_data
            for page_crawling_data_list in parallel_result.values()
            for page_crawling_data in page_crawling_data_list
        ]

        # 2. title만 뽑아서 db 전체 조회해서 이미 보낸 뉴스가 있는지 확인
        target_titles: set[str] = {
            item.title for item in flatten_parallel_result if item.title is not None
        }
        messages = get_messages(list(target_titles))

        # 3. db에서 가져온 messages 중 messages 필드의 title만 추출
        duplicate_message_titles: set[str] = {
            message.title
            for doc in messages
            for message in doc.messages
            if message.title
        }

        # 4. 중복된 title 제거하여 unique한 뉴스 제목만 추출
        unique_news_titles = target_titles - duplicate_message_titles

        # 5. 원본 딕셔너리(parallel_result)에서 중복된 value 제거한 새로운 딕셔너리 생성
        unique_parallel_result: CrawlingResult = {
            site_name: [
                PageCrawlingData(title=item.title, url=item.url)
                for item in site_data
                if item.title in unique_news_titles
            ]
            for site_name, site_data in parallel_result.items()
        }

        if env.ENABLE_MESSAGE_AGENT_LOG:
            self.logger.console_print(
                ConsoleDataType.TABLE,
                self._get_parallel_result_table(unique_parallel_result),
            )

        # 6. unique_parallel_result를 카카오워크 메세지로 생성
        request = KakaoworkMessageBuilder().build(unique_parallel_result)
        status_code = KakaoworkClient(env.PROFILE).send_message(request)
        status = SEND_MESSAGE_SUCCESS if status_code == 200 else SEND_MESSAGE_FAIL

        # 7. 성공/실패 여부를 db에 기록
        try:
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
        except Exception as e:
            self.logger.exception(f"Failed to save message. reason=({e})")
            raise e

    def _get_parallel_result_table(self, result: CrawlingResult) -> Table:
        table = Table(title="unique_parallel_result", title_justify="left")
        table.add_column("idx", no_wrap=True)
        table.add_column("site_name", style="cyan", no_wrap=True)
        table.add_column("url", overflow="fold")
        table.add_column("title", style="magenta", overflow="fold")
        for idx_1, (site_name, page_crawling_data) in enumerate(
            result.items(), start=1
        ):
            for idx_2, item in enumerate(page_crawling_data, start=1):
                table.add_row(str(idx_1 + idx_2 - 1), site_name, item.url, item.title)
        return table
