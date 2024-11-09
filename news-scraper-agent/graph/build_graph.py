from typing import Callable

from langchain.schema.runnable import RunnableParallel
from langchain_community.llms import FakeListLLM
from langgraph.graph import StateGraph, START, END

from agents import HtmlParserAgent, CrawlingAgent, FilteringAgent, MessageAgent
from graph import SiteState, State
from models.site import SiteDto
from service import get_sites

# FakeListLLM 설정
fake_responses = [
    "[]",
    "[]",
]
LLM = FakeListLLM(responses=fake_responses)  # FIXME 테스트 시 사용
# LLM = ChatOpenAI(model_name=config.MODEL_NAME)


def create_crawl_filter_sequence(LLM, site: SiteDto) -> Callable[[State], SiteState]:
    html_parser_agent = HtmlParserAgent()
    crawling_agent = CrawlingAgent(LLM, site=site)
    filtering_agent = FilteringAgent(LLM, site=site)

    def process_site(state: State) -> SiteState:
        initial_site_state = SiteState(
            crawling_result={}, filtering_result={}, parser_result=[]
        )
        state = html_parser_agent(
            initial_site_state
        )  # FIXME 어떤 상태를 넘길지는 구현 시 수정 필요
        state = crawling_agent(state)
        state = filtering_agent(state)
        return state

    return process_site


def parallel_crawl_filter(state: State) -> State:
    sites = state.sites

    parallel_sequences = {
        f"{site.name}": create_crawl_filter_sequence(LLM, site)
        for i, site in enumerate(sites)
    }

    parallel_runner = RunnableParallel(**parallel_sequences)
    results: dict[str, SiteState] = parallel_runner.invoke(state)

    filtered_results = {}
    for result in results.values():
        filtered_results.update(result.filtering_result)

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
