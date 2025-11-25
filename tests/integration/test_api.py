import pytest
import time
from fastapi.testclient import TestClient


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()
    assert "version" in response.json()


def test_generate_article_creates_job(client):
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "best productivity tools for remote teams",
            "target_word_count": 800,
            "language": "en"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "job_id" in data
    assert "status" in data
    assert data["status"] in ["pending", "running"]


def test_get_job_returns_details(client):
    create_response = client.post(
        "/api/v1/generate",
        json={
            "topic": "best productivity tools",
            "target_word_count": 500
        }
    )
    
    job_id = create_response.json()["job_id"]
    
    get_response = client.get(f"/api/v1/jobs/{job_id}")
    
    assert get_response.status_code == 200
    data = get_response.json()
    
    assert data["job_id"] == job_id
    assert "status" in data
    assert "topic" in data
    assert data["topic"] == "best productivity tools"


def test_get_nonexistent_job_returns_404(client):
    response = client.get("/api/v1/jobs/nonexistent-job-id")
    assert response.status_code == 404


def test_generate_article_validation(client):
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "ab",
            "target_word_count": 100
        }
    )
    
    assert response.status_code == 422


def test_generate_article_with_custom_word_count(client):
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "productivity tools",
            "target_word_count": 2000,
            "language": "en"
        }
    )
    
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    
    job_response = client.get(f"/api/v1/jobs/{job_id}")
    assert job_response.json()["target_word_count"] == 2000

