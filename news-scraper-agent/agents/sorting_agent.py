from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel

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
    items: list[int]


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
            filtering_result = state.filtering_result[self.site.name]
            filtering_result_request = []
            for idx, item in enumerate(filtering_result, start=1):
                filtering_result_request.append(
                    SortRequestItem(id=idx, url=item.url, title=item.title)
                )

            sort_result = list(
                map(lambda x: x.id, self.request_sort(filtering_result_request))
            )

            result: list[PageCrawlingData] = list(
                map(
                    lambda x: PageCrawlingData(
                        url=x.url,
                        title=x.title,
                    ),
                    sorted(
                        filtering_result_request,
                        key=lambda x: sort_result.index(x.id),
                    ),
                )
            )

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

    def request_sort(self, filtering_result: list[SortRequestItem]) -> list[int]:
        formatted_prompt = self.prompt.format(filtering_result=filtering_result)

        llm_with_structured_output = self.llm.with_structured_output(SortResponse)
        response: SortResponse = llm_with_structured_output.invoke(formatted_prompt)

        return response.items
