import json

import pytest

from src import app
from src.used_type import RequestBody


def get_api_gw_event(body: RequestBody) -> dict:
    return {
        "body": json.dumps(body),
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_static_page():
    resp = app.handler({
        "url": "https://d1qbk7p5aewspc.cloudfront.net/test/test_static.html",
        "content_type": "html",
        "selector": "#content-section > section.products > div:nth-child(2) > span",
    }, "")
    data = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "result" in data
    assert data["result"][0] == '<span class="price">$25</span>'


def test_render_page():
    resp = app.handler({
        "url": "https://d1qbk7p5aewspc.cloudfront.net/test/test_render.html",
        "content_type": "html",
        "selector": "#content-section > section.products > div:nth-child(2) > span",
    }, "")
    data = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "result" in data
    assert data["result"][0] == '<span class="price">$25</span>'


def test_json():
    resp = app.handler({
        "url": "https://jsonplaceholder.typicode.com/users/1",
        "content_type": "json",
    }, "")
    data = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "result" in data
    assert data["result"]["username"] == "Bret"