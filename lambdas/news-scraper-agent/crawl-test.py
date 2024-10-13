from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langfuse.decorators import observe
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv

import time
import threading
import json
import os
import operator

load_dotenv(verbose=True)

# 상태 정의
class State(TypedDict):
    out_values: Annotated[List[Dict[str, Any]], operator.add]
    prompts: Annotated[List[str], operator.add]
    crawling_results: Annotated[List[Dict[str, Any]], operator.add]

# 에이전트의 output 포맷을 정의
class AgentResponseItem(BaseModel):
    title: str = Field(description="Title of the agent response item")
    url: str = Field(description="URL of the agent response item")

class AgentResponse(BaseModel):
    items: List[AgentResponseItem] = Field(description="List of agent response items")

# 크롤링 에이전트
class CrawlingAgent:
    crawling_prompt = os.getenv('CRAWLING_AGENT_PROMPT_EN') or os.getenv('CRAWLING_AGENT_PROMPT_KO')

    def __init__(self, llm: ChatOpenAI, site: Dict[str, str], prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.crawling_prompt)
        self.site = site
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    @observe(as_type="crawling-generate")
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()

        chain = self.prompt | self.llm | self.parser
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

        return crawling_result

# 필터링 에이전트
class FilteringAgent:
    filtering_prompt = os.getenv('FILTERING_AGENT_PROMPT_EN') or os.getenv('FILTERING_AGENT_PROMPT_KO')

    def __init__(self, llm: ChatOpenAI, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.filtering_prompt)
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    @observe(as_type="filtering-generate")
    def __call__(self, state: State) -> Dict[str, Any]:
        chain = self.prompt | self.llm | self.parser
        input_variables = {"extract_site_info": state["crawling_results"]}
        response = chain.invoke(input_variables)

        return {
            "out_values": [response],
            "prompts": [self.prompt.format(**input_variables)],
            "crawling_results": state["crawling_results"]
        }

def process_crawler_results(results: Dict[str, Any]) -> Dict[str, Any]:
    out_values = []
    prompts = []
    crawling_results = []

    for result in results.values():
        out_values.append(result['content'])
        crawling_results.append(result)

    return {
        "out_values": out_values,
        "prompts": prompts,
        "crawling_results": crawling_results
    }

@observe()
def main():
    llm = ChatOpenAI(model_name="chatgpt-4o-latest")

    builder = StateGraph(State)

    # 시작 노드 추가
    builder.add_node("start", lambda x: {"out_values": [], "prompts": [], "crawling_results": []})
    builder.add_edge(START, "start")

    sites = [
        {"name": "긱뉴스", "url": "https://news.hada.io/new", "info": "최신 10개 항목의 title과 url들"},
        {"name": "AI 타임즈", "url": "https://www.aitimes.com/news/articleList.html?sc_section_code=S1N24&view_type=sm", "info": "많이 본 기사 10개의 제목과 url들"},
        {"name": "ZDnet", "url": "https://zdnet.co.kr/news/?lstcode=0020&page=1", "info": "컴퓨팅 인기 뉴스 항목의 타이틀 과 URL 들"},
    ]

    # 크롤링 노드 추가 (RunnableParallel 사용)
    crawlers = {f"crawler_{i}": CrawlingAgent(llm, site=site) for i, site in enumerate(sites)}
    parallel_crawlers = RunnableParallel(**crawlers)
    builder.add_node("crawlers", parallel_crawlers | process_crawler_results)

    # 필터링 노드 추가
    builder.add_node("filter", FilteringAgent(llm))

    # 엣지 추가
    builder.add_edge("start", "crawlers")
    builder.add_edge("crawlers", "filter")
    builder.add_edge("filter", END)

    # 그래프 실행
    graph = builder.compile()
    initial_state = {
        "out_values": [],
        "prompts": [],
        "crawling_results": []
    }
    result = graph.invoke(initial_state)
    return result

if __name__ == "__main__":
    try:
        result = main()
        print(result)
        exit(0)  # 성공적으로 종료
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)  # 오류로 인한 종료
