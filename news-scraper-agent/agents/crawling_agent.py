import threading
import time
from config import config
from graph import SiteState, AgentResponse
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from models.site import SiteDto


class CrawlingAgent:
    crawling_prompt = config.CRAWLING_AGENT_PROMPT_EN or config.CRAWLING_AGENT_PROMPT_KO

    def __init__(
        self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None
    ):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.crawling_prompt
        )
        self.site = site
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    # ??: state가 SiteState로 되어있는데 실제로는 State가 옴
    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser

        # TODO prompt 및 input_variables 재구성 필요
        input_variables = {"site_name": self.site.name, "site_url": self.site.url}
        response = chain.invoke(input_variables)

        crawling_result = {
            "site_name": self.site.name,
            "site_url": self.site.url,
            "content": response,
        }

        end_time = time.time()
        print(
            f"Finished crawl for {self.site.name} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )

        new_state = state.model_copy(deep=True)
        new_state.site = self.site
        if new_state.prompts is None:
            new_state.prompts = []
        new_state.prompts.append(self.prompt)
        # ??: crawling_result는 dict인가? list인가? SiteState를 보면 list 타입인데 여기서는 dict를 넣고있음
        new_state.crawling_result = crawling_result

        return new_state
