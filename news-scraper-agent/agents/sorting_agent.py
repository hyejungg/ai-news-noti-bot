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
    title: str


class SortingResponse(BaseModel):
    class Item(BaseModel):
        id: int
        reason: str

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
            # 모델에게 보내기위해 id를 추가한 리스트
            filtering_results_with_id: list[SortRequestItem] = []
            # 모델 응답으로 원본 데이터를 찾기위한 딕셔너리
            filtering_results_map: dict[int, PageCrawlingData] = {}

            for idx, item in enumerate(state.filtering_result[self.site.name], start=1):
                data_id = idx
                filtering_results_with_id.append(
                    SortRequestItem(id=data_id, title=item.title)
                )
                filtering_results_map[data_id] = PageCrawlingData(
                    title=item.title, url=item.url
                )

            sort_result: list[SortingResponse.Item] = self.__request_sort(
                filtering_results_with_id
            )

            sorted_result = []
            for item in sort_result:
                result_item = filtering_results_map[item.id]
                result_item.reason = item.reason
                sorted_result.append(result_item)

            state.sorted_result[self.site.name] = sorted_result
        except Exception as e:
            self.logger.error(f"Error occurred while sorting {self.site.name}: {e}")
            self.logger.warning(f"Skip sorting {self.site.name}")

            state.sorted_result[self.site.name] = [
                PageCrawlingData(url=item.url, title=item.title, reason=item.reason)
                for item in state.filtering_result[self.site.name]
            ]

        state.print_state(sorted_result=True)
        return state

    def __request_sort(
        self, filtering_result: list[SortRequestItem]
    ) -> list[SortingResponse.Item]:
        formatted_prompt = self.prompt.format(filtering_result=filtering_result)

        llm_with_structured_output = self.llm.with_structured_output(SortingResponse)
        response: SortingResponse = llm_with_structured_output.invoke(formatted_prompt)

        return response.items
