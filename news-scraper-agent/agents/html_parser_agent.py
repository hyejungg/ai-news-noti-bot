from typing import Annotated, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import config
from graph import State
import time
import threading


# TODO 아래 코드 작성하기
class HtmlParserAgent:
    def __init__(self):
        # none
        pass

    def __call__(self, state: State = None) -> State:  # FIXME 수정 필요
        # FIXME
        # html parser
        pass
