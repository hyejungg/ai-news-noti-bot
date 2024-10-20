from typing import Annotated, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import config
from graph.state import State, AgentResponse
import time
import threading

class FilteringAgent:
    filtering_prompt = config.FILTERING_AGENT_PROMPT_EN or config.FILTERING_AGENT_PROMPT_KO

    def __init__(self, llm: ChatOpenAI, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.filtering_prompt)
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    def __call__(self, state: State) -> State:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser
        input_variables = {"extract_site_info": state["crawling_results"]}
        response = chain.invoke(input_variables)

        end_time = time.time()
        print(f"Finished filtering for {State['site']['name']} on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds")

        new_state = state.copy()
        news_state["out_values"] = response
        new_state["filtering_results"] = response
        new_state["prompts"].append(self.prompt.format(**input_variables))

        return new_state
