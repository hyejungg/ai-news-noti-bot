from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langfuse.decorators import observe
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv
import json
import os
import operator

load_dotenv(verbose=True)

# 상태 정의
class State(TypedDict):
    aggregate: Annotated[List[str], operator.add]
    fanout_values: Annotated[List[Dict[str, Any]], operator.add]
    which: str
    prompts: Annotated[List[str], operator.add]
    crawling_results: Annotated[List[Dict[str, Any]], operator.add]

# 크롤링 에이전트의 output 포맷을 정의
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
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.crawling_prompt)  # 변경된 부분
        self.site = site
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    @observe(as_type="crawling-generate")
    def __call__(self, state: State) -> Dict[str, Any]:
        chain = self.prompt | self.llm | self.parser
        input_variables = {
            "site_name": self.site['name'],
            "site_url": self.site['url'],
            "site_additional_info": self.site['info']
        }
        response = chain.invoke(input_variables)  # 변경된 부분

        crawling_result = {
            "site_name": self.site["name"],
            "site_url": self.site["url"],
            "content": json.dumps(response)
        }

        return {
            "fanout_values": [crawling_result],
            "prompts": [self.prompt.format(**input_variables)],  # 변경된 부분
            "crawling_results": [crawling_result]
        }

# 필터링 에이전트
class FilteringAgent:
    filtering_prompt = os.getenv('FILTERING_AGENT_PROMPT_EN') or os.getenv('FILTERING_AGENT_PROMPT_KO')

    def __init__(self, llm: ChatOpenAI, prompt: str = None):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt if prompt else self.filtering_prompt)  # 변경된 부분
        self.parser = JsonOutputParser(pydantic_object=AgentResponse)

    @observe(as_type="filtering-generate")
    def __call__(self, state: State) -> Dict[str, Any]:
        chain = self.prompt | self.llm | self.parser
        input_variables = {"extract_site_info": state["crawling_results"]}
        response = chain.invoke(input_variables)  # 변경된 부분

        return {
            "fanout_values": [{
                "extract_site_info": state["crawling_results"],
                "content": json.dumps(response)
            }],
            "prompts": [self.prompt.format(**input_variables)]  # 변경된 부분
        }

# 라우팅 함수
@observe()
def route_to_crawlers(state: State) -> List[str]:
    return state["which"].split(",")

@observe()
def main():
    llm = ChatOpenAI(model_name="chatgpt-4o-latest")

    builder = StateGraph(State)

    # 시작 노드 추가
    builder.add_node("start", lambda x: {"aggregate": ["Starting crawl"]})
    builder.add_edge(START, "start")

    # TODO 우선 임시로 배열로 구성
    sites = [
        {"name": "긱뉴스", "url": "https://news.hada.io/new", "info": "최신 10개 항목의 title과 url들"},
#         {"name": "데보션", "url": "https://devocean.sk.com/blog/techBoardDetail.do?ID=166905&boardType=techToday&searchData=&searchDataMain=&page=&subIndex=&searchText=&techType=NEWS&searchDataSub=%27", "info": ""},
        {"name": "AI 타임즈", "url": "https://www.aitimes.com/news/articleList.html?sc_section_code=S1N24&view_type=sm", "info": "많이 본 기사 10개의 제목과 url들"},
        {"name": "ZDnet", "url": "https://zdnet.co.kr/news/?lstcode=0020&page=1", "info": "컴퓨팅 인기 뉴스 항목의 타이틀 과 URL 들"},
#         {"name": "삼성 SDS", "url": "https://www.samsungsds.com/kr/insights/index.html?moreCnt=0&backTypeId=&category=&reqArtId=1282554", "info": "해당 페이지의 기사 제목과 url"}
    ]

    # 크롤링 노드 추가
    for i, site in enumerate(sites):
        node_name = f"crawler_{i}_{site["name"]}"
        builder.add_node(node_name, CrawlingAgent(llm, site=site))

    # 필터링 노드 추가
    builder.add_node("filter", FilteringAgent(llm))

    # 시작에서 크롤러 노드로 엣지 추가
    crawler_nodes = [f"crawler_{i}_{site['name']}" for i, site in enumerate(sites)]
    builder.add_conditional_edges("start", route_to_crawlers, {node: node for node in crawler_nodes})

    # 크롤러에서 필터링 노드로 엣지 추가
    for node in crawler_nodes:
        builder.add_edge(node, "filter")

    # 필터링 결과 전달
    builder.add_edge("filter", END)

    # 그래프 실행
    graph = builder.compile()
    result = graph.invoke({
        "which": ",".join(crawler_nodes)
    })
    return result

if __name__ == "__main__":
    try:
        result = main()
        print(result)
        exit(1) # 종료
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(-1) # 종료

