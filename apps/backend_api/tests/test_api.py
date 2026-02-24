import pytest
from fastapi.testclient import TestClient
from apps.backend_api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Smart House Recommendation API"}
    assert "x-process-time" in response.headers

def test_metrics_header():
    """Verify middleware adds API response time to headers for analytics"""
    response = client.get("/")
    assert "x-process-time" in response.headers
    process_time = float(response.headers["x-process-time"])
    assert process_time >= 0.0

def test_error_handling_invalid_route():
    response = client.get("/invalid_route")
    assert response.status_code == 404

def test_api_performance_dummy():
    """Simulate API performance logging metrics validation"""
    response = client.get("/")
    assert response.status_code == 200
    assert float(response.headers["x-process-time"]) < 2.0  # basic SLA check
