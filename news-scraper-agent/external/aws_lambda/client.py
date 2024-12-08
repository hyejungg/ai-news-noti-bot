import time

import boto3

from config.log import NewsScraperAgentLogger


class LambdaInvoker:
    def __init__(self):
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)

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
