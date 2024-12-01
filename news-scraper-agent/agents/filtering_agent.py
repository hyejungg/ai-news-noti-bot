from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from agents.components.LangChainLLMCaller import LangChainLLMCallerWithStructure
from config.log import create_logger
from config.prompt_config import DefaultPromptTemplate
from decorations.log_time import log_time_agent_method
from graph.state import SiteState, AgentResponse
from models.site import SiteDto


class FilteringAgent:
    filtering_prompt = (
        DefaultPromptTemplate.FILTERING_AGENT_PROMPT_EN
        or DefaultPromptTemplate.FILTERING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.logger = create_logger(self.__class__.__name__)
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.filtering_prompt
        )
        self.llm_caller = LangChainLLMCallerWithStructure(
            caller_instance=self,
            llm=llm,
            output_structure=AgentResponse,
        )

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
            formatted_prompt = self.prompt.format(
                crawling_result=state.crawling_result[self.site.name]
            )

            response = self.llm_caller.invoke(formatted_prompt)

            state.filtering_result[self.site.name] = response.items
        except Exception as e:
            self.logger.error(f"Error occurred while filtering {self.site.name}: {e}")
            state.filtering_result[self.site.name] = []

        state.print_state(filtering_result=True)
        return state
