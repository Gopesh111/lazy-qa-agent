from fastapi.testclient import TestClient

def test_analyze_video_endpoint_validation(client):
    """
    Tests that the endpoint rejects non-video file formats.
    """
    response = client.post(
        "/api/v1/analyze-video",
        files={"file": ("test_log.txt", b"dummy content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["detail"]

def test_health_check(client):
    """
    Simple status check to ensure the service is running.
    """
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["status"] == "active"