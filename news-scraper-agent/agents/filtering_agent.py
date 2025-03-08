from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel

from config.log import NewsScraperAgentLogger
from config.prompt_config import DefaultPromptTemplate
from decorations.log_time import log_time_agent_method
from graph.state import SiteState, PageCrawlingData
from models.site import SiteDto


class FilterRequestItem(BaseModel):
    id: int
    title: str


class FilteringResponse(BaseModel):
    items: list[int]


class FilteringAgent:
    filtering_prompt = (
        DefaultPromptTemplate.FILTERING_AGENT_PROMPT_EN
        or DefaultPromptTemplate.FILTERING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.filtering_prompt
        )
        self.llm = llm

    @log_time_agent_method
    def __call__(self, state: SiteState) -> SiteState:
        if (
            not state.crawling_result[self.site.name]
            or len(state.crawling_result[self.site.name]) == 0
        ):
            self.logger.warning(f"No data to filter for {self.site.name}")
            state.filtering_result[self.site.name] = []
            return state

        try:
            # 모델에게 보내기위해 id를 추가한 리스트
            crawling_results_with_id: list[FilterRequestItem] = []
            # 모델 응답으로 원본 데이터를 찾기위한 딕셔너리
            crawling_results_map: dict[int, PageCrawlingData] = {}

            for idx, item in enumerate(state.crawling_result[self.site.name], start=1):
                data_id = idx
                crawling_results_with_id.append(
                    FilterRequestItem(id=data_id, title=item.title)
                )
                crawling_results_map[data_id] = PageCrawlingData(
                    title=item.title, url=item.url
                )

            formatted_prompt = self.prompt.format(
                crawling_result=crawling_results_with_id
            )

            llm_with_structured_output = self.llm.with_structured_output(
                FilteringResponse
            )
            response: FilteringResponse = llm_with_structured_output.invoke(
                formatted_prompt
            )

            filtering_result = [
                crawling_results_map[item_id] for item_id in response.items
            ]
            state.filtering_result[self.site.name] = filtering_result
        except Exception as e:
            self.logger.error(f"Error occurred while filtering {self.site.name}: {e}")
            state.filtering_result[self.site.name] = []

        state.print_state(filtering_result=True)
        return state
