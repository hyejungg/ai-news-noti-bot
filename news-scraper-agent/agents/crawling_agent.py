from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config.log import NewsScraperAgentLogger
from config.prompt_config import DefaultPromptTemplate
from decorations.log_time import log_time_agent_method
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
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.crawling_prompt
        )
        self.site = site
        self.llm = llm

    @log_time_agent_method
    def __call__(self, state: SiteState) -> SiteState:
        if (
            state.parser_result[self.site.name] is None
            or len(state.parser_result[self.site.name]) == 0
        ):
            self.logger.warning(f"No data to crawl for {self.site.name}")
            state.crawling_result[self.site.name] = []
            return state

        try:
            compressed_parser_result = list(
                map(self.__strip_attributes, state.parser_result[self.site.name])
            )

            formatted_prompt = self.crawling_prompt.format(
                site_name=self.site.name,
                site_url=self.site.url,
                parser_result=compressed_parser_result,
            )

            llm_with_structured_output = self.llm.with_structured_output(AgentResponse)
            response: AgentResponse = llm_with_structured_output.invoke(
                formatted_prompt
            )

            state.crawling_result[self.site.name] = response.items
        except Exception as e:
            self.logger.error(f"Error occurred while crawling {self.site.name}: {e}")
            state.crawling_result[self.site.name] = []

        state.print_state(crawling_result=True)
        return state

    @staticmethod
    def __strip_attributes(html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all():
            tag.attrs = {k: v for k, v in tag.attrs.items() if k == "href"}  # href 유지

        return str(soup)
