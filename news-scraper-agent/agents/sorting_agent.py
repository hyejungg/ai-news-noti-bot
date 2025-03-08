from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from config.log import NewsScraperAgentLogger
from config.prompt_config import DefaultPromptTemplate
from decorations.log_time import log_time_agent_method
from graph.state import (
    SiteState,
    PageCrawlingData,
)
from models.site import SiteDto


class SortRequestItem(BaseModel):
    id: int
    url: str
    title: str


class SortResponse(BaseModel):
    class Item(BaseModel):
        id: int = Field(description="id of the item")
        reason: str = Field(
            description="simplified reason why this item is sorted in Korean"
        )

    items: list[Item]


class SortingAgent:
    sorting_prompt = (
        DefaultPromptTemplate.SORTING_AGENT_PROMPT_EN
        or DefaultPromptTemplate.SORTING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.sorting_prompt
        )
        self.llm = llm

    @log_time_agent_method
    def __call__(self, state: SiteState) -> SiteState:
        if (
            not state.filtering_result[self.site.name]
            or len(state.filtering_result[self.site.name]) == 0
        ):
            self.logger.warning(f"No data to sort for {self.site.name}")
            state.sorted_result[self.site.name] = []
            return state

        try:
            # 필터링 결과 가져옴
            filtering_result = state.filtering_result[self.site.name]

            # 필터링 결과에 id를 부여
            filtering_results_with_id: list[SortRequestItem] = []
            for idx, item in enumerate(filtering_result, start=1):
                filtering_results_with_id.append(
                    SortRequestItem(id=idx, url=item.url, title=item.title)
                )

            sort_result: list[SortResponse.Item] = self.__request_sort(
                filtering_results_with_id
            )

            def sort_by_id(sort_request_item: SortRequestItem) -> int:
                for element in sort_result:
                    if element.id == sort_request_item.id:
                        return sort_result.index(element)
                return 0

            # id를 기준으로 필터링 결과를 정렬
            filtering_results_with_id.sort(key=sort_by_id)

            result: list[PageCrawlingData] = [
                PageCrawlingData(**filtering_result.model_dump())
                for filtering_result in filtering_results_with_id
            ]

            state.sorted_result[self.site.name] = result
        except Exception as e:
            self.logger.error(f"Error occurred while sorting {self.site.name}: {e}")
            self.logger.warning(f"Skip sorting {self.site.name}")

            state.sorted_result[self.site.name] = [
                PageCrawlingData(url=item.url, title=item.title)
                for item in state.filtering_result[self.site.name]
            ]

        state.print_state(sorted_result=True)
        return state

    def __request_sort(
        self, filtering_result: list[SortRequestItem]
    ) -> list[SortResponse.Item]:
        formatted_prompt = self.prompt.format(filtering_result=filtering_result)

        llm_with_structured_output = self.llm.with_structured_output(SortResponse)
        response: SortResponse = llm_with_structured_output.invoke(formatted_prompt)

        return response.items
