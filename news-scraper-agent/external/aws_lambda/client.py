import time

import boto3
from tenacity import retry, wait_fixed, stop_after_attempt, RetryCallState

from config.log import NewsScraperAgentLogger


def log_before_retry(max_retry: int):
    def log_before(retry_state: RetryCallState):
        lambda_invoker: LambdaInvoker = retry_state.args[
            0
        ]  # invoke 함수의 첫번째 파라미터 (self)
        logging_name: str = retry_state.kwargs.get("logging_name", "")
        if retry_state.attempt_number > 1:
            lambda_invoker.logger.info(
                f"Retrying Invoke lambda {logging_name}... {retry_state.attempt_number - 1}/{max_retry - 1}"
            )

    return log_before


class LambdaInvoker:
    def __init__(self):
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)

    @retry(
        wait=wait_fixed(wait=3),  # 초
        stop=stop_after_attempt(max_attempt_number=3),
        before=log_before_retry(max_retry=3),
    )
    def invoke(
        self,
        logging_name: str = None,
        **kwargs,
    ):
        name = logging_name if logging_name else "Lambda invocation"
        start = time.time()
        self.logger.info(f"Started {name} ")

        response = self.client.invoke(**kwargs)

        end = time.time()
        self.logger.info(f"Finished {name} ({end - start:.2f}s)")
        return response
