import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Animal Recognition API"
    tags = [tag["name"] for tag in schema.get("tags", [])]
    assert "animals" in tags, f"Expected 'animals' in tags, got {tags}"