import threading
import time

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import JsonOutputParser

from config import config
from graph.state import SiteState, SortAgentResponse, SortedFilteringData
from models.site import SiteDto


class SortingAgent:
    sorting_prompt = config.SORTING_AGENT_PROMPT_EN or config.SORTING_AGENT_PROMPT_KO

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.llm = llm
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.sorting_prompt
        )
        self.parser = JsonOutputParser(pydantic_object=SortAgentResponse)

    def __call__(self, state: SiteState) -> SiteState:
        # TODO 임시로 filtering_result 생성. merge 전에 state.filtering_result 초기화 하는 부분 삭제하기!!
        start_time = time.time()
        state.filtering_result = {
            self.site.name: [
                {
                    "title": "GN⁺: 보이스피싱범의 시간을 낭비하는 AI 할머니 데이지",
                    "url": "https://news.virginmediao2.co.uk",
                },
                {
                    "title": "Google Web AI Summit 2024 요약: 개발자를 위한 클라이언트 측 AI",
                    "url": "https://developers.googleblog.com",
                },
                {
                    "title": "Firecrawl - 웹사이트 전체를 LLM에서 사용가능하게 만드는 도구",
                    "url": "https://github.com/mendableai",
                },
                {
                    "title": "Show GN: 고양이도 발로 코딩한다는 'MOUSE' AI 서비스.",
                    "url": "https://openfree-mouse.hf.space",
                },
                {
                    "title": "Integuru - 내부 API를 리버스 엔지니어링 해서 외부용 통합 코드를 생성하는 AI에이전트",
                    "url": "https://github.com/Integuru-AI",
                },
            ]
        }

        chain = self.prompt | self.llm | self.parser
        input_variables = {"filtering_result": state.filtering_result[self.site.name]}
        response: list = chain.invoke(input_variables)

        end_time = time.time()
        print(
            f"Finished sorting on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )
        state.sorted_result[self.site.name] = [
            SortedFilteringData(**item) for item in response
        ]

        return state
