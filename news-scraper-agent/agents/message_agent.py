from typing import Annotated, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import config
from graph import State
import time
import threading

# TODO 아래 코드 작성하기
class MessageAgent:
    def __init__(self):
        # none
        pass

    def __call__(self, state: State) -> State:
        # FIXME 이 agent 에서 아래 기능을 다 수행해도 되고, 각 기능을 agent 로 구성해도 될 듯?
        # db 접근하여 현재까지 전송 성공한 메시지 가져오기
        # State 의 filtering_results 와 현재까지 전송한 성공 메시지 중 title 이 같은 메시지 필터링
        # 카카오워크에 메시지 전송
        pass
