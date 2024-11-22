import json
import unittest

from langchain_openai import ChatOpenAI

from agents.crawling_agent import CrawlingAgent
from config.log import logger
from graph.state import SiteState
from models.site import SiteDto


class CrawlingAgentTest(unittest.TestCase):
    def setUp(self):
        self.gpt_4o_mini = ChatOpenAI(model_name="gpt-4o-mini")
        self.geek_news = SiteDto(
            name="긱뉴스",
            url="https://news.hada.io/new",
            verified=True,
            keywords=[],
            createdAt=None,
            updatedAt=None,
            requestedBy="",
        )

    def test_GN(self):
        site = self.geek_news
        crawling_agent = CrawlingAgent(llm=self.gpt_4o_mini, site=site)

        with open("./fixtures/crawling_agent_test_gn.json", "r") as f:
            parser_result = json.load(f)

        state_before = SiteState(
            filtering_result={},
            crawling_result={},
            parser_result={site.name: parser_result},
            sorted_result={},
        )
        state_after = crawling_agent(state_before)

        for v in state_after.crawling_result[site.name]:
            logger.info(v)

        self.assertIn(site.name, state_after.crawling_result)  # 키가 존재해야 함
        self.assertIsInstance(
            state_after.crawling_result[site.name], list
        )  # 값이 리스트여야 함
        self.assertGreater(
            len(state_after.crawling_result[site.name]), 0
        )  # 리스트 길이가 0보다 커야 함


if __name__ == "__main__":
    unittest.main()
