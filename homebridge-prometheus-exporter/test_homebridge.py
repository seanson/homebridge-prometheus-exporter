import pytest
import responses
from datetime import datetime
from freezegun import freeze_time


from homebridge import HomeBridge


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@freeze_time("2022-01-01")
def test_api_login(mocked_responses):
    hb = HomeBridge("http://localhost:8080", "foo", "bar")
    mocked_responses.post(
        "http://localhost:8080/api/auth/login",
        json={"access_token": "abc123", "expires_in": 1},
        status=201,
    )
    hb._auth()
    assert hb.session.headers["Authorization"] == "Bearer abc123"
    assert hb.token_expiry == datetime(2022, 1, 1, 0, 0, 1)


@freeze_time("2022-01-01", auto_tick_seconds=1)
def test_api_login_expiry(mocked_responses):
    hb = HomeBridge("http://localhost:8080", "foo", "bar")
    mocked_responses.post(
        "http://localhost:8080/api/auth/login",
        json={"access_token": "abc123", "expires_in": 1},
        status=201,
    )
    mocked_responses.post(
        "http://localhost:8080/api/auth/login",
        json={"access_token": "newtoken", "expires_in": 1},
        status=201,
    )
    hb._auth()
    hb._auth()
    assert hb.session.headers["Authorization"] == "Bearer newtoken"
    assert hb.token_expiry == datetime(2022, 1, 1, 0, 0, 8)


def test_api(mocked_responses):
    hb = HomeBridge("http://localhost:8080", "foo", "bar")
    mocked_responses.post(
        "http://localhost:8080/api/auth/login",
        json={"access_token": "abc123", "expires_in": 100},
        status=201,
    )
    mocked_responses.get("http://localhost:8080/api/accessories", status=200, json={})
    hb._auth()
    accessories = hb.get_accessories()
    assert accessories == {}
