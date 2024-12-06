import json

import pytest

from src import app
from src.used_type import RequestBody


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


def test_devocean():
    resp = app.handler({
        "url": "https://devocean.sk.com/blog/index.do?techType=NEWS",
        "content_type": "html",
        "selector": "div.sec-area > ul.sec-area-list01 > li:first-child > div a > h3.pc_view"
    }, "")
    data = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "result" in data
    assert data["result"] is not None

def test_sds():
    resp = app.handler({
        "url": "https://www.samsungsds.com/kr/insights/index.html?moreCnt=0&backTypeId=&category=&reqArtId=1282554",
        "content_type": "html",
        "selector": ".cont_list .item strong.md_tit"
    }, "")
    data = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "result" in data
    assert data["result"] is not None
