import threading
import time

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config.log import logger
from config.prompt_config import defaultPrompt
from graph.state import SiteState, AgentResponse
from models.site import SiteDto


class FilteringAgent:
    filtering_prompt = (
        defaultPrompt.FILTERING_AGENT_PROMPT_EN
        or defaultPrompt.FILTERING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.llm = llm
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.filtering_prompt
        )

    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        formatted_prompt = self.prompt.format(
            crawling_result=state.crawling_result[self.site.name]
        )
        llm_with_structured_output = self.llm.with_structured_output(AgentResponse)
        response: AgentResponse = llm_with_structured_output.invoke(formatted_prompt)

        end_time = time.time()
        logger.info(
            f"Finished filtering on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )
        state.filtering_result[self.site.name] = response.items

        return state
