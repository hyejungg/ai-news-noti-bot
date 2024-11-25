import threading
import time

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config import defaultPrompt
from config.log import logger
from graph.state import (
    SiteState,
    AgentResponse,
)
from models.site import SiteDto


class CrawlingAgent:
    crawling_prompt = (
        defaultPrompt.CRAWLING_AGENT_PROMPT_EN or defaultPrompt.CRAWLING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.crawling_prompt
        )
        self.site = site

    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        formatted_prompt = self.crawling_prompt.format(
            site_name=self.site.name,
            site_url=self.site.url,
            parser_result=state.parser_result[self.site.name],
        )

        llm_with_structured_output = self.llm.with_structured_output(AgentResponse)
        response: AgentResponse = llm_with_structured_output.invoke(formatted_prompt)

        end_time = time.time()
        logger.info(
            f"Finished crawl for {self.site.name} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )
        state.crawling_result[self.site.name] = response.items

        return state
