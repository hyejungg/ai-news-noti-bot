import time

import boto3
from tenacity import retry, wait_fixed, stop_after_attempt

from config.log import NewsScraperAgentLogger


class LambdaInvoker:
    def __init__(self):
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)
        self.invoke = retry(
            wait=wait_fixed(3),
            stop=stop_after_attempt(3),
            before=self.__log_before_retry()
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

    def __log_before_retry(self):
        def log_before(retry_state):
            if retry_state.attempt_number > 1:  # 첫 시도는 로깅하지 않음
                self.logger.info(
                    f"Retrying Invoke lambda... {retry_state.attempt_number - 1}/{2}"
                )

        return log_before
