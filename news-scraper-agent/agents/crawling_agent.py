from typing import Annotated, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import config
from graph.state import State, AgentResponse
import time
import threading

class CrawlingAgent:
    crawling_prompt = config.CRAWLING_AGENT_PROMPT_EN or config.CRAWLING_AGENT_PROMPT_KO

    def __init__(self, llm: ChatOpenAI, site: Dict[str, str], prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.crawling_prompt)
        self.site = site
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    def __call__(self, state: State) -> State:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser
        # TODO prompt 및 input_variables 재구성 필요
        input_variables = {
            "site_name": self.site['name'],
            "site_url": self.site['url'],
            "site_additional_info": self.site['info']
        }
        response = chain.invoke(input_variables)

        crawling_result = {
            "site_name": self.site["name"],
            "site_url": self.site["url"],
            "content": response
        }

        end_time = time.time()
        print(f"Finished crawl for {self.site['name']} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds")

        new_state = state.copy()
        news_state["out_values"] = crawling_result
        new_state["crawling_result"].append(crawling_result)

        return new_state
