import threading
import time
from config import defaultPrompt
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from graph.state import PageCrawlingData, SiteState, AgentResponse
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
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser

        # TODO prompt 및 input_variables 재구성 필요
        input_variables = {"site_name": self.site.name, "site_url": self.site.url}
        response: list[PageCrawlingData] = chain.invoke(input_variables)
        end_time = time.time()
        print(
            f"Finished crawl for {self.site.name} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )
        state.crawling_result[self.site.name] = response

        return state
