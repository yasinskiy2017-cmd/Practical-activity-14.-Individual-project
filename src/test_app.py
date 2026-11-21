from app import app


def test_health_endpoint():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"


def test_history_endpoint():
    client = app.test_client()
    resp = client.get("/history")
    assert resp.status_code == 200
    assert "items" in resp.get_json()


def test_invalid_url_rejected():
    client = app.test_client()
    resp = client.get("/check?url=ftp://example.com")
    assert resp.status_code == 400
