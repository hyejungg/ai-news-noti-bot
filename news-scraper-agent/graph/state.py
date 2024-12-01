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

    def print_state(
        self,
        crawling_result: bool = False,
        filtering_result: bool = False,
        parser_result: bool = False,
        sorted_result: bool = False,
    ):
        console = Console()
        if parser_result:
            for site, results in self.parser_result.items():
                table = Table(title=f"[{site}] ParserResult")
                table.add_column("idx", no_wrap=True)
                table.add_column("result", no_wrap=True)
                for idx, result in enumerate(results, start=1):
                    table.add_row(str(idx), result)
                console.print(table)

        if crawling_result:
            for site, results in self.crawling_result.items():
                table = Table(title=f"[{site}] CrawlingResult")
                table.add_column("idx", no_wrap=True)
                table.add_column("url", no_wrap=True)
                table.add_column("title", style="magenta")
                for idx, result in enumerate(results, start=1):
                    table.add_row(str(idx), result.url, result.title)
                console.print(table)

        if filtering_result:
            for site, results in self.filtering_result.items():
                table = Table(title=f"[{site}] FilteringResult")
                table.add_column("idx", no_wrap=True)
                table.add_column("url", no_wrap=True)
                table.add_column("title", style="magenta")
                for idx, result in enumerate(results, start=1):
                    table.add_row(str(idx), result.url, result.title)
                console.print(table)

        if sorted_result:
            for site, results in self.sorted_result.items():
                table = Table(title=f"[{site}] SortedResult")
                table.add_column("idx", no_wrap=True)
                table.add_column("url", no_wrap=True)
                table.add_column("title", style="magenta")
                table.add_column("reason", style="cyan")
                for idx, result in enumerate(results, start=1):
                    table.add_row(str(idx), result.url, result.title, result.reason)
                console.print(table)


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
