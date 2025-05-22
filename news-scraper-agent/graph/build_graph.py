from typing import Callable

from langchain.schema.runnable import RunnableParallel
from langchain_community.llms import FakeListLLM
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from agents.crawling_agent import CrawlingAgent
from agents.filtering_agent import FilteringAgent
from agents.html_parser_agent import HtmlParserAgent
from agents.message_agent import MessageAgent
from agents.sorting_agent import SortingAgent
from graph.state import SiteState, State, PageCrawlingData
from models.site import SiteDto
from service.site_service import get_sites

# FakeListLLM 설정
fake_responses = [
    "[]",
    "[]",
]
# llm = FakeListLLM(responses=fake_responses)  # FIXME 테스트 시 사용
llm = ChatOpenAI(model="gpt-4o")


def create_crawl_filter_sequence(
    site: SiteDto,
    html_parser_agent_instance: HtmlParserAgent,
    crawling_agent_instance: CrawlingAgent,
    filtering_agent_instance: FilteringAgent,
    sorting_agent_instance: SortingAgent,
) -> Callable[[State], SiteState]:
    def process_site(state: State) -> SiteState:
        initial_site_state = SiteState(
            crawling_result={}, filtering_result={}, parser_result={}, sorted_result={}
        )
        # Pass site to the __call__ method of each agent
        current_site_state = html_parser_agent_instance(
            site=site, state=initial_site_state
        )
        current_site_state = crawling_agent_instance(
            site=site, state=current_site_state
        )
        current_site_state = filtering_agent_instance(
            site=site, state=current_site_state
        )
        current_site_state = sorting_agent_instance(
            site=site, state=current_site_state
        )
        return current_site_state

    return process_site


def parallel_crawl_filter(
    state: State,
    html_parser_agent_instance: HtmlParserAgent,
    crawling_agent_instance: CrawlingAgent,
    filtering_agent_instance: FilteringAgent,
    sorting_agent_instance: SortingAgent,
) -> State:
    sites = state.sites

    parallel_sequences = {
        f"{site.name}": create_crawl_filter_sequence(
            site,
            html_parser_agent_instance,
            crawling_agent_instance,
            filtering_agent_instance,
            sorting_agent_instance,
        )
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
    html_parser_agent = HtmlParserAgent()
    crawling_agent = CrawlingAgent(llm=llm)
    filtering_agent = FilteringAgent(llm=llm)
    sorting_agent = SortingAgent(llm=llm)

    builder = StateGraph(State)

    # init node
    builder.add_node("start", lambda x: initial_state)
    builder.add_node("get_sites", get_sites)
    builder.add_node(
        "parallel_crawl_filter",
        lambda state: parallel_crawl_filter(
            state,
            html_parser_agent,
            crawling_agent,
            filtering_agent,
            sorting_agent,
        ),
    )
    builder.add_node("send_message", MessageAgent())

    # connect edge
    builder.add_edge(START, "start")
    builder.add_edge("start", "get_sites")
    builder.add_edge("get_sites", "parallel_crawl_filter")
    builder.add_edge("parallel_crawl_filter", "send_message")
    builder.add_edge("send_message", END)

    # graph run
    return builder.compile()
