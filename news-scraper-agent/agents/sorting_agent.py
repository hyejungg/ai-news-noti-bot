from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config.log import NewsScraperAgentLogger
from config.prompt_config import DefaultPromptTemplate
from decorations.log_time import log_time_agent_method
from graph.state import SiteState, SortAgentResponse, SortedFilteringData
from models.site import SiteDto


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
            formatted_prompt = self.prompt.format(
                filtering_result=state.filtering_result[self.site.name]
            )

            llm_with_structured_output = self.llm.with_structured_output(
                SortAgentResponse
            )
            response: SortAgentResponse = llm_with_structured_output.invoke(
                formatted_prompt
            )

            state.sorted_result[self.site.name] = response.items
        except Exception as e:
            self.logger.error(f"Error occurred while sorting {self.site.name}: {e}")
            self.logger.warning(f"Skip sorting {self.site.name}")
            state.sorted_result[self.site.name] = [
                SortedFilteringData(url=result.url, title=result.title, reason="")
                for result in state.filtering_result[self.site.name]
            ]

        state.print_state(sorted_result=True)
        return state
