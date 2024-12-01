import threading
import time

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config.log import default_logger
from config.prompt_config import DefaultPromptTemplate
from graph.state import (
    SiteState,
    AgentResponse,
)
from models.site import SiteDto


class CrawlingAgent:
    crawling_prompt = (
        DefaultPromptTemplate.CRAWLING_AGENT_PROMPT_EN
        or DefaultPromptTemplate.CRAWLING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.crawling_prompt
        )
        self.site = site

    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        if (
            state.parser_result[self.site.name] is None
            or len(state.parser_result[self.site.name]) == 0
        ):
            default_logger.warning(f"No data to crawl for {self.site.name}")
            state.crawling_result[self.site.name] = []
            return state

        try:
            formatted_prompt = self.crawling_prompt.format(
                site_name=self.site.name,
                site_url=self.site.url,
                parser_result=state.parser_result[self.site.name],
            )

            llm_with_structured_output = self.llm.with_structured_output(AgentResponse)
            response: AgentResponse = llm_with_structured_output.invoke(
                formatted_prompt
            )

            end_time = time.time()
            default_logger.info(
                f"Finished crawl for {self.site.name} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
            )
            state.crawling_result[self.site.name] = response.items
        except Exception as e:
            default_logger.error(f"Error occurred while crawling {self.site.name}: {e}")
            state.crawling_result[self.site.name] = []

        return state
