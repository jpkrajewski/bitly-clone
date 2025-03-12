from falcon import testing
import src.app
from unittest.mock import Mock
import pytest


@pytest.fixture()
def collection():
    mock = Mock()
    mock.find_one.return_value = None
    return mock


@pytest.fixture()
def client(collection):
    return testing.TestClient(src.app.create_app(collection))


def test_shorten_url(client):
    resp = client.simulate_post("/shorten", json={"url": "https://google.com"})
    assert resp.status == "200 OK"
    assert resp.json["url"] == "https://google.com"
    assert resp.json["short_url"] == "falconframework.org/r/eedcfc2484"


def test_redirect_url_not_found(client):
    resp = client.simulate_get("/r/eedcfc2484")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "URL not found"


def test_redirect_url_found(client, collection):
    collection.find_one.return_value = {
        "short_url": "eedcfc2484",
        "long_url": "https://google.com",
        "ip": "1.1.1.1",
        "user_agent": "Mozilla/5.0",
        "count": 1,
    }

    resp = client.simulate_get("/r/eedcfc2484")
    assert resp.status == "302 Found"
    assert resp.headers["Location"] == "https://google.com"
    assert collection.update_one.called
    assert collection.update_one.call_args[0][0] == {"short_url": "eedcfc2484"}
    assert collection.update_one.call_args[0][1] == {"$inc": {"count": 1}}


def test_telemetry_url_owner_not_found(client):
    resp = client.simulate_get("/telemetry/owner/eedcfc2484")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "Short URL eedcfc2484 not found"


def test_telemetry_url_owner_found(client, collection):
    collection.find_one.return_value = {
        "short_url": "eedcfc2484",
        "long_url": "https://google.com",
        "ip": "1.1.1",
        "user_agent": "Mozilla/5.0",
        "count": 1,
    }

    resp = client.simulate_get("/telemetry/owner/eedcfc2484")
    assert resp.status == "200 OK"
    assert resp.json["ip"] == "1.1.1"
    assert resp.json["user_agent"] == "Mozilla/5.0"


def test_telemetry_url_count_not_found(client):
    resp = client.simulate_get("/telemetry/count/eedcfc2484")
    assert resp.status == "404 Not Found"
    assert resp.json["error"] == "Short URL eedcfc2484 not found"


def test_telemetry_url_count_found(client, collection):
    collection.find_one.return_value = {
        "short_url": "eedcfc2484",
        "long_url": "https://google.com",
        "ip": "1.1.1",
        "user_agent": "Mozilla/5.0",
        "count": 1,
    }

    resp = client.simulate_get("/telemetry/count/eedcfc2484")
    assert resp.status == "200 OK"
    assert resp.json["count"] == 1
