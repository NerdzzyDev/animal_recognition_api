import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.exceptions import ImageProcessingError

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Галерея животных" in response.text

def test_image_to_base64_success(client, test_image):
    response = client.post(
        "/image_to_base64",
        files={"image": ("test.png", test_image, "image/png")}
    )
    assert response.status_code == 200
    assert "base64_image" in response.json()

def test_image_to_base64_invalid_file(client, invalid_image):
    response = client.post(
        "/image_to_base64",
        files={"image": ("test.txt", invalid_image, "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid content type" in response.json()["detail"]

def test_what_is_animal_success(client, test_image_base64, mocker):
    mocker.patch(
        "app.services.animal_recognition.AnimalRecognitionService.recognize_animal",
        return_value={
            "animal": "кошка",
            "description": "A small feline.",
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "answer": "На изображении, вероятно, кошка.",
            "timestamp": "2025-04-25T13:59:27.740855",
            "similarities": [{"id": 1, "metadata": {"animal_name": "cat"}, "score": 0.9}]
        }
    )
    response = client.post(
        "/api/what_is_animal",
        json={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "query": "Какое это животное?",
            "timestamp": "2025-04-25T13:59:27.740855",
            "image": test_image_base64
        }
    )
    assert response.status_code == 200
    assert "animal" in response.json()

def test_what_is_animal_invalid_base64(client):
    response = client.post(
        "/api/what_is_animal",
        json={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "query": "Какое это животное?",
            "timestamp": "2025-04-25T13:59:27.740855",
            "image": "invalid-base64-string"
        }
    )
    assert response.status_code == 400
    assert "Invalid base64" in response.json()["detail"]
