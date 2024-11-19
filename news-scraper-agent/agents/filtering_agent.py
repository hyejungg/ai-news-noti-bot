import threading
import time

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from config import config
from graph.state import SiteState, AgentResponse
from models.site import SiteDto


class FilteringAgent:
    filtering_prompt = (
        config.FILTERING_AGENT_PROMPT_EN or config.FILTERING_AGENT_PROMPT_KO
    )

    def __init__(self, llm: BaseLanguageModel, site: SiteDto, prompt: str = None):
        self.llm = llm
        self.site = site
        self.prompt = PromptTemplate.from_template(
            prompt if prompt else self.filtering_prompt
        )

    def __call__(self, state: SiteState) -> SiteState:
        # TODO 임시로 crawling_result 생성. merge 전에 state.crawling_results 초기화 하는 부분 삭제하기!!
        start_time = time.time()
        state.crawling_result = {
            self.site.name: [
                {
                    "title": "Rust 프로그래밍을 시작하고싶으신 분들을 위한 무료책",
                    "url": "https://github.com/gurugio",
                },
                {
                    "title": "PageFind - 정적 페이지를 위한 검색 라이브러리",
                    "url": "https://pagefind.app",
                },
                {
                    "title": "Maxun - 오픈소스 노-코드 웹 데이터 추출 플랫폼",
                    "url": "https://github.com/getmaxun",
                },
                {
                    "title": "신한캐피탈, 이유없이 창업자에게 15%의 연이자로 투자금 반환 소송을 걸다",
                    "url": "https://medium.com/@lionha",
                },
                {
                    "title": "Show GN: 리액트 컴포넌트 소스코드를 찾아주는 크롬 확장 프로그램",
                    "url": "https://chromewebstore.google.com",
                },
                {
                    "title": "GN⁺: 보이스피싱범의 시간을 낭비하는 AI 할머니 데이지",
                    "url": "https://news.virginmediao2.co.uk",
                },
                {
                    "title": "Cacheable - Keyv 기반 Node.js용 캐싱 패키지",
                    "url": "https://github.com/jaredwray",
                },
                {
                    "title": "jiti 2.0 - Node.js에 런타임 TypeScript와 ESM 구문 지원",
                    "url": "https://github.com/unjs",
                },
                {"title": "dns query의 여정", "url": "https://frogred8.github.io"},
                {
                    "title": "GN⁺: Spin 3.0 – WASM 앱 구축 및 실행을 위한 오픈 소스 툴링",
                    "url": "https://www.fermyon.com",
                },
                {
                    "title": "새로운 AI 시대에 Palantir가 주는 교훈",
                    "url": "https://www.8vc.com",
                },
                {
                    "title": "고성과자(High Performer)를 무시하지 마세요",
                    "url": "https://hbr.org",
                },
                {
                    "title": "Google Web AI Summit 2024 요약: 개발자를 위한 클라이언트 측 AI",
                    "url": "https://developers.googleblog.com",
                },
                {
                    "title": "Visprex - CSV를 위한 인-브라우저 데이터 시각화 오픈소스",
                    "url": "https://github.com/visprex",
                },
                {
                    "title": "lukacho/ui - 깔끔한 애니메이션을 지원하는 UI 컴포넌트 라이브러리",
                    "url": "https://ui.lukacho.com",
                },
                {"title": "Web Locks API", "url": "https://developer.mozilla.org"},
                {
                    "title": "Firecrawl - 웹사이트 전체를 LLM에서 사용가능하게 만드는 도구",
                    "url": "https://github.com/mendableai",
                },
                {
                    "title": "rip2 - 더 안전한 Rust 기반 rm",
                    "url": "https://github.com/MilesCranmer",
                },
                {
                    "title": "Show GN: 고양이도 발로 코딩한다는 'MOUSE' AI 서비스.",
                    "url": "https://openfree-mouse.hf.space",
                },
                {
                    "title": "2025 디자인 트렌드 예측: 크리에이티브 리더들의 인사이트",
                    "url": "https://www.creativeboom.com",
                },
                {
                    "title": "GN⁺: IronCalc – 오픈소스 스프레드시트 엔진",
                    "url": "https://ironcalc.com",
                },
                {
                    "title": "GN⁺: 빅테크에서 프로젝트를 Ship 하는 방법",
                    "url": "https://seangoedecke.com",
                },
                {
                    "title": "Integuru - 내부 API를 리버스 엔지니어링 해서 외부용 통합 코드를 생성하는 AI에이전트",
                    "url": "https://github.com/Integuru-AI",
                },
            ]
        }

        formatted_prompt = self.prompt.format(crawling_result=state.crawling_result[self.site.name])
        llm_with_structured_output = self.llm.with_structured_output(AgentResponse)
        response:AgentResponse = llm_with_structured_output.invoke(formatted_prompt)

        end_time = time.time()
        print(
            f"Finished filtering on thread {threading.get_ident()}. Time taken: {end_time - start_time:.2f} seconds"
        )
        state.filtering_result[self.site.name] = response.items

        return state
