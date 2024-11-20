from typing import Callable

from langchain.schema.runnable import RunnableParallel
from langchain_community.llms import FakeListLLM
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from agents.crawling_agent import CrawlingAgent
from agents.filtering_agent import FilteringAgent
from agents.html_parser_agent import HtmlParserAgent
from agents.message_agent import MessageAgent
from agents.sorting_agent import SortingAgent
from graph.state import SiteState, State, SortedFilteringData, PageCrawlingData
from models.site import SiteDto
from service import get_sites

# FakeListLLM 설정
fake_responses = [
    "[]",
    "[]",
]
# llm = FakeListLLM(responses=fake_responses)  # FIXME 테스트 시 사용


def create_crawl_filter_sequence(site: SiteDto) -> Callable[[State], SiteState]:
    # html_parser_agent = HtmlParserAgent()
    # crawling_agent = CrawlingAgent(site=site)
    filtering_agent = FilteringAgent(
        ChatOpenAI(model_name="gpt-4o-mini"), site=site
    )
    sorting_agent = SortingAgent(
        ChatOpenAI(model_name="gpt-4o-mini"), site=site
    )

    def process_site(state: State) -> SiteState:
        initial_site_state = SiteState(
            crawling_result={}, filtering_result={}, parser_result=[], sorted_result={}
        )
        # TODO 우선 필터링 에이전트만 동작 확인을 위해 주석, merge 전에 주석 풀기
        # state = html_parser_agent(
        #     initial_site_state
        # )  # FIXME 어떤 상태를 넘길지는 구현 시 수정 필요
        # state = crawling_agent(state)
        state = filtering_agent(initial_site_state)
        state = sorting_agent(state)
        return state

    return process_site


def parallel_crawl_filter(state: State) -> State:
    sites = state.sites

    parallel_sequences = {
        f"{site.name}": create_crawl_filter_sequence(site)
        for i, site in enumerate(sites)
    }

    parallel_runner = RunnableParallel(**parallel_sequences)
    results: dict[str, SiteState] = parallel_runner.invoke(state)

    filtered_results = {}
    for site_name, result in results.items():
        exclusive_reason_results = [
            PageCrawlingData(url=item.url, title=item.title)
            for item in result.sorted_result[site_name]
        ]
        filtered_results[site_name] = exclusive_reason_results

    state.parallel_result = filtered_results

    return state


def build_graph(initial_state: State):
    builder = StateGraph(State)

    # init node
    builder.add_node("start", lambda x: initial_state)
    builder.add_node("get_sites", get_sites)
    builder.add_node("parallel_crawl_filter", parallel_crawl_filter)
    builder.add_node("send_message", MessageAgent())

    # connect edge
    builder.add_edge(START, "start")
    builder.add_edge("start", "get_sites")
    builder.add_edge("get_sites", "parallel_crawl_filter")
    builder.add_edge("parallel_crawl_filter", "send_message")
    builder.add_edge("send_message", END)

    # graph run
    return builder.compile()
