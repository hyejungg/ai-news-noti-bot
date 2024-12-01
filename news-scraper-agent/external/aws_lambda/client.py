import logging
import time

import boto3

from config.log import create_logger


class LambdaInvoker:
    def __init__(self, name: str = None, logger: logging.Logger = None):
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = (
            logger
            if logger is not None
            else create_logger(name if name else self.__class__.__name__)
        )

    def invoke(
        self,
        *args,
        logging_name: str = None,
        **kwargs,
    ):
        name = logging_name if logging_name else "Lambda invocation"

        start = time.time()
        self.logger.info(f"Started {name} ")
        response = self.client.invoke(*args, **kwargs)
        end = time.time()
        self.logger.info(f"Finished {name} ({end - start:.2f}s)")
        return response
