import logging
import time

import boto3
from tenacity import retry, wait_fixed, stop_after_attempt

from config.log import create_logger


class LambdaInvoker:
    def __init__(
        self, name: str = None, logger: logging.Logger = None, max_retry: int = 3
    ):
        logger_name = name if name else self.__class__.__name__
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = logger if logger is not None else create_logger(logger_name)
        self.max_retry = max_retry
        self.invoke = retry(
            wait=wait_fixed(3),
            stop=stop_after_attempt(max_retry),
            before=self.__log_before_retry(logging_name=logger_name),
        )(self.invoke)

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

    def __log_before_retry(self, logging_name: str = None):
        def log_before(retry_state):
            if retry_state.attempt_number > 1:  # 첫 시도는 로깅하지 않음
                self.logger.info(
                    f"Retrying Invoke lambda {logging_name}... {retry_state.attempt_number}/{self.max_retry}"
                )

        return log_before
