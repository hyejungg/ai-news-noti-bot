from config.env_config import env
from config.log import ConsoleDataType, NewsScraperAgentLogger
from models.site import SiteDto
from pydantic import BaseModel, Field
from rich.table import Table


class SortedFilteringData(BaseModel):
    url: str
    title: str
    reason: str


class PageCrawlingData(BaseModel):
    url: str
    title: str


type SortedFilterResult = dict[str, list[SortedFilteringData]]
type CrawlingResult = dict[str, list[PageCrawlingData]]
type ParserResult = dict[str, list[str]]


class SiteState(BaseModel):
    crawling_result: CrawlingResult
    filtering_result: CrawlingResult
    parser_result: ParserResult
    sorted_result: SortedFilterResult

    def _get_print_table(self, title: str, columns: list[dict], data: dict) -> Table:
        """
        공통 테이블 출력 메서드.
        :param title: 테이블 제목.
        :param columns: 열 정의 리스트 (각 열의 이름, 스타일, overflow 등).
        :param data: 출력할 데이터 딕셔너리.
        """
        for site, results in data.items():
            table = Table(title=f"[{site}] {title}", title_justify="left")
            # 열 정의 추가
            for column in columns:
                table.add_column(**{k: v for k, v in column.items() if k != "key"})
            # 데이터 추가
            for idx, result in enumerate(results, start=1):
                if isinstance(result, str):
                    table.add_row(str(idx), result)
                else:
                    table.add_row(
                        str(idx),
                        *(
                            getattr(result, column["key"], "")
                            for column in columns
                            if "key" in column
                        ),
                    )
            return table

    def print_state(
        self,
        crawling_result: bool = False,
        filtering_result: bool = False,
        parser_result: bool = False,
        sorted_result: bool = False,
    ):
        logger = NewsScraperAgentLogger("PrintState")
        if parser_result:
            logger_name = "ParserResult"
            if env.PROFILE == "local":
                table = self._get_print_table(
                    title=logger_name,
                    columns=[
                        {"header": "idx", "no_wrap": True},
                        {
                            "header": "result",
                            "overflow": "fold",
                            "key": "result",
                            "max_width": 80,
                        },
                    ],
                    data=self.parser_result,
                )
                logger.console_print(ConsoleDataType.TABLE, table)
            else:
                logger.console_print(
                    ConsoleDataType.DICT, self.parser_result, logger_name
                )

        if crawling_result:
            logger_name = "CrawlingResult"
            if env.PROFILE == "local":
                table = self._get_print_table(
                    title=logger_name,
                    columns=[
                        {"header": "idx", "no_wrap": True},
                        {
                            "header": "url",
                            "overflow": "fold",
                            "key": "url",
                            "max_width": 80,
                        },
                        {
                            "header": "title",
                            "style": "magenta",
                            "overflow": "fold",
                            "key": "title",
                            "max_width": 80,
                        },
                    ],
                    data=self.crawling_result,
                )
                logger.console_print(ConsoleDataType.TABLE, table)
            else:
                dict_result = {
                    site: [item.model_dump() for item in items]
                    for site, items in self.crawling_result.items()
                }
                logger.console_print(ConsoleDataType.DICT, dict_result, logger_name)

        if filtering_result:
            logger_name = "FilteringResult"
            if env.PROFILE == "local":
                table = self._get_print_table(
                    title=logger_name,
                    columns=[
                        {"header": "idx", "no_wrap": True},
                        {
                            "header": "url",
                            "overflow": "fold",
                            "key": "url",
                            "max_width": 80,
                        },
                        {
                            "header": "title",
                            "style": "magenta",
                            "overflow": "fold",
                            "key": "title",
                            "max_width": 80,
                        },
                    ],
                    data=self.filtering_result,
                )
                logger.console_print(ConsoleDataType.TABLE, table)
            else:
                dict_result = {
                    site: [item.model_dump() for item in items]
                    for site, items in self.filtering_result.items()
                }
                logger.console_print(ConsoleDataType.DICT, dict_result, logger_name)

        if sorted_result:
            logger_name = "SortedResult"
            if env.PROFILE == "local":
                table = self._get_print_table(
                    title=logger_name,
                    columns=[
                        {"header": "idx", "no_wrap": True},
                        {
                            "header": "url",
                            "overflow": "fold",
                            "key": "url",
                            "max_width": 40,
                        },
                        {
                            "header": "title",
                            "style": "magenta",
                            "overflow": "fold",
                            "key": "title",
                            "max_width": 40,
                        },
                        {
                            "header": "reason",
                            "style": "cyan",
                            "overflow": "fold",
                            "key": "reason",
                            "max_width": 40,
                        },
                    ],
                    data=self.sorted_result,
                )
                logger.console_print(ConsoleDataType.TABLE, table)
            else:
                dict_result = {
                    site: [item.model_dump() for item in items]
                    for site, items in self.sorted_result.items()
                }
                logger.console_print(ConsoleDataType.DICT, dict_result, logger_name)


class State(BaseModel):
    sites: list[SiteDto]
    parallel_result: CrawlingResult


class AgentResponse(BaseModel):
    items: list[PageCrawlingData] = Field(
        description="List of agent response items (title, url)"
    )


class SortAgentResponse(BaseModel):
    items: list[SortedFilteringData] = Field(
        description="List of agent response items (title, url, reason)"
    )
