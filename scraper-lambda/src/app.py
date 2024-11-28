import json
import requests

from typing import get_type_hints, get_args
from playwright.sync_api import sync_playwright, ElementHandle, TimeoutError as PlaywrightTimeoutError
from used_type import RequestBody


def error(msg: str, status: int) -> dict:
    return {
        "statusCode": status,
        "body": json.dumps(
            {
                "message": msg,
            },
            ensure_ascii=False,
        ),
    }


def success(result: list) -> dict:
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "result": result,
            },
            ensure_ascii=False,
        ),
    }


def handler(event, context) -> dict:
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    # body check
    body: dict = event
    # url, content_type, selector
    url = body.get("url")
    content_type = body.get("content_type")
    selector = body.get("selector")

    if url is None:
        return error("url is required", 400)
    if content_type is None:
        return error("content_type is required", 400)
    if content_type not in get_args(get_type_hints(RequestBody)["content_type"]):
        return error(f"Invalid content type: {content_type}", 400)

    if content_type == "json":
        try:
            response = requests.get(url, timeout=10)  # 10초 타임아웃
            response.raise_for_status()  # HTTP 오류 확인 -> 발생 시 RequestException으로 catch
            return success(response.json())
        except requests.Timeout:
            return error("Request timed out while fetching JSON", 408)
        except requests.RequestException as e:
            return error(f"Request failed: {str(e)}", 400)

    elif content_type == "html":
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--single-process",
                        "--disable-gpu",
                    ],
                    headless=True,
                )
                page = browser.new_page()
                page.goto(url, timeout=80000) # 80초
                page.wait_for_load_state("networkidle", timeout=80000) # 80초
                page_content = page.content()
                result = [page_content]
                if selector:
                    selected: list[ElementHandle] = page.query_selector_all(selector)
                    if len(selected) == 0:
                        return error(f"Element not found with {selector}", 400)
                    result = list(map(lambda x: x.evaluate("(element) => element.outerHTML"), selected))
                browser.close()
            return success(result)
        except PlaywrightTimeoutError:
            return error("HTML rendering timed out", 408)
        except Exception as e:
            return error(f"An unexpected error occurred: {str(e)}", 500)

    else:
        return error(f"Invalid content type: {content_type}", 400)
