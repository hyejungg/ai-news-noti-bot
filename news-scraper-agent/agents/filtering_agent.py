import threading
import time
from config import config
from graph import SiteState, AgentResponse
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser


class FilteringAgent:
    filtering_prompt = (
        config.FILTERING_AGENT_PROMPT_EN or config.FILTERING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.filtering_prompt
        )
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    def __call__(self, state: SiteState) -> SiteState:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser

        # TODO prompt 및 input_variables 재구성 필요
        input_variables = {"extract_site_info": state["crawling_result"]}
        response = chain.invoke(input_variables)

        end_time = time.time()
        print(
            f"Finished filtering on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )

        new_state = state.copy()
        new_state.setdefault("prompts", []).append(self.prompt)
        new_state["filtering_result"] = response

        return new_state
