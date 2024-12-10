import json
import logging
import time

import boto3
from pydantic import BaseModel
from tenacity import retry, wait_fixed, stop_after_attempt, RetryCallState

from config.log import NewsScraperAgentLogger


class ScraperLambdaResponseBody(BaseModel):
    statusCode: int
    body: dict


class LambdaResponse(BaseModel):
    StatusCode: int
    ResponseMetadata: dict
    Payload: ScraperLambdaResponseBody
    ExecutedVersion: str


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


def log_after_retry():
    def log_after(retry_state: RetryCallState):
        if retry_state.outcome.failed:
            lambda_invoker: LambdaInvoker = retry_state.args[
                0
            ]  # invoke 함수의 첫번째 파라미터 (self)
            lambda_invoker.logger.error(f"{retry_state.outcome.exception()}")

    return log_after


class LambdaInvoker:
    def __init__(self):
        self.client = boto3.client("lambda", region_name="ap-northeast-2")
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)

    @retry(
        wait=wait_fixed(wait=3),  # 초
        stop=stop_after_attempt(max_attempt_number=3),
        before=log_before_retry(max_retry=3),
        after=log_after_retry(),
    )
    def invoke(
        self,
        logging_name: str = None,
        **kwargs,
    ) -> dict:
        name = logging_name if logging_name else "Lambda invocation"
        start = time.time()
        self.logger.info(f"Started {name} ")

        response = self.parse_response(self.client.invoke(**kwargs))

        self.raise_if_error(response)

        end = time.time()
        self.logger.info(f"Finished {name} ({end - start:.2f}s)")
        return response.Payload.body

    def parse_response(self, response: dict):
        try:
            payload = json.load(response["Payload"])
            body = json.loads(payload["body"])
        except Exception as e:
            logging.exception("Failed to parse response")
            raise e

        return LambdaResponse(
            StatusCode=response["StatusCode"],
            ResponseMetadata=response["ResponseMetadata"],
            Payload=ScraperLambdaResponseBody(
                statusCode=payload["statusCode"], body=body
            ),
            ExecutedVersion=response["ExecutedVersion"],
        )

    def raise_if_error(self, payload: LambdaResponse):
        if payload.StatusCode != 200 or payload.Payload.statusCode != 200:
            body = payload.Payload.body
            raise Exception(f"Lambda 호출 실패 [message={body['message']}]")
