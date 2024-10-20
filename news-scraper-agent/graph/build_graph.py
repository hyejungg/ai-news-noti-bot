from langchain_openai import ChatOpenAI
from config import config
from langgraph.graph import StateGraph, START, END
from langchain.schema.runnable import RunnableParallel
from langchain.schema.runnable import RunnableSequence
from agents import CrawlingAgent, FilteringAgent, MessageAgent
from graph import State
from service import get_sites

LLM = ChatOpenAI(model_name=config.MODEL_NAME)

def create_crawl_filter_sequence(LLM, site):
    crawling_agent = CrawlingAgent(LLM, site=site)
    filtering_agent = FilteringAgent(LLM)

    return {
        "parallel_results": RunnableSequence(crawling_agent, filtering_agent)
    }

def parallel_crawl_filter(state: State) -> State:
    sites = state["sites"]

    parallel_sequences = {
        f"site_{i}": create_crawl_filter_sequence(LLM, site)
        for i, site in enumerate(sites)
    }

    parallel_runner = RunnableParallel(**parallel_sequences)
    results = parallel_runner.invoke(state)

    new_state = state.copy()
    new_state["parallel_results"] = results

    return new_state

def build_graph():
    builder = StateGraph(State)
    initial_state = {
        "sites": [],
        "out_values": [],
        "prompts": [],
        "crawling_results": [],
        "filtering_result": [],
        "send_messages": []
    }

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
