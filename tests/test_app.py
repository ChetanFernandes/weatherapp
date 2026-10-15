import app


def test_homepage_returns_index_template():
    client = app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Search" in response.data
    assert b"enter city" in response.data


def test_weatherdata_uses_openweather_response(monkeypatch):
    client = app.app.test_client()

    class DummyResponse:
        def json(self):
            return {"name": "London", "weather": []}

    captured = {}

    def fake_get(url, params=None):
        captured["url"] = url
        captured["params"] = params
        return DummyResponse()

    monkeypatch.setattr(app.requests, "get", fake_get)

    response = client.post(
        "/weatherapp",
        data={"city": "London", "appid": "abc123", "units": "metric"},
    )

    assert response.status_code == 200
    assert b"London" in response.data
    assert captured["url"] == "https://api.openweathermap.org/data/2.5/weather"
    assert captured["params"] == {"q": "London", "appid": "abc123", "units": "metric"}
