import os

import pytest
from falcon import testing
from urlshortner.app import create_app


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["URLSHORT_REPO_TYPE"] = "memory"


@pytest.fixture(scope="function")
def client():
    return testing.TestClient(create_app())


def test_shorten_url(client):
    resp = client.simulate_post("/shorten", json={"url": "https://google.com"})
    assert resp.status == "200 OK"
    assert resp.json["url"] == "https://google.com"
    assert resp.json[
        "short_url"] == "http://falconframework.org/r/eedcfc24841d2b296d3e"


def test_redirect_url_not_found(client):
    resp = client.simulate_get("/r/eedcfc24841d2b296d3e")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "URL not found"


def test_redirect_url_found(client):
    resp = client.simulate_post("/shorten", json={"url": "https://google.com"})
    assert resp.status == "200 OK"

    resp = client.simulate_get("/r/eedcfc24841d2b296d3e")
    assert resp.status == "302 Found"
    assert resp.headers["Location"] == "https://google.com"


def test_telemetry_url_owner_not_found(client):
    resp = client.simulate_get("/telemetry/owner/eedcfc24841d2b296d3e")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "Short URL eedcfc24841d2b296d3e not found"


def test_telemetry_url_owner_found(client):
    resp = client.simulate_post("/shorten", json={"url": "https://google.com"})
    assert resp.status == "200 OK"

    resp = client.simulate_get("/telemetry/owner/eedcfc24841d2b296d3e")
    assert resp.status == "200 OK"
    assert resp.json["ip"] == "127.0.0.1"
    assert resp.json["user_agent"] == "falcon-client/4.0.2"


def test_telemetry_url_count_not_found(client):
    resp = client.simulate_get("/telemetry/count/eedcfc24841d2b296d3e")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "Short URL eedcfc24841d2b296d3e not found"


def test_telemetry_url_count_found(client):
    resp = client.simulate_post("/shorten", json={"url": "https://google.com"})
    assert resp.status == "200 OK"

    resp = client.simulate_get("/telemetry/count/eedcfc24841d2b296d3e")
    assert resp.status == "200 OK"
    assert resp.json["count"] == 0
