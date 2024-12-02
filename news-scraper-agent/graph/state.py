import rich.table
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from models.site import SiteDto


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

    def _print_table(self, title: str, columns: list[dict], data: dict):
        """
        공통 테이블 출력 메서드.
        :param title: 테이블 제목.
        :param columns: 열 정의 리스트 (각 열의 이름, 스타일, overflow 등).
        :param data: 출력할 데이터 딕셔너리.
        """
        console = Console()
        for site, results in data.items():
            table = Table(title=f"[{site}] {title}")
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
            console.print(table)

    def print_state(
        self,
        crawling_result: bool = False,
        filtering_result: bool = False,
        parser_result: bool = False,
        sorted_result: bool = False,
    ):
        if parser_result:
            self._print_table(
                title="ParserResult",
                columns=[
                    {"header": "idx", "no_wrap": True},
                    {"header": "result", "overflow": "fold", "key": "result"},
                ],
                data=self.parser_result,
            )

        if crawling_result:
            self._print_table(
                title="CrawlingResult",
                columns=[
                    {"header": "idx", "no_wrap": True},
                    {"header": "url", "overflow": "fold", "key": "url"},
                    {
                        "header": "title",
                        "style": "magenta",
                        "overflow": "fold",
                        "key": "title",
                    },
                ],
                data=self.crawling_result,
            )

        if filtering_result:
            self._print_table(
                title="FilteringResult",
                columns=[
                    {"header": "idx", "no_wrap": True},
                    {"header": "url", "overflow": "fold", "key": "url"},
                    {
                        "header": "title",
                        "style": "magenta",
                        "overflow": "fold",
                        "key": "title",
                    },
                ],
                data=self.filtering_result,
            )

        if sorted_result:
            self._print_table(
                title="SortedResult",
                columns=[
                    {"header": "idx", "no_wrap": True},
                    {"header": "url", "overflow": "fold", "key": "url"},
                    {
                        "header": "title",
                        "style": "magenta",
                        "overflow": "fold",
                        "key": "title",
                    },
                    {
                        "header": "reason",
                        "style": "cyan",
                        "overflow": "fold",
                        "key": "reason",
                    },
                ],
                data=self.sorted_result,
            )


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
