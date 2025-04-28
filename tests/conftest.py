import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.image_processor import ImageProcessor
from app.services.animal_recognition import AnimalRecognitionService
from app.utils.translations import translate_animal_name
import base64
import logging

# Настройка логирования для диагностики
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    """Фикстура для FastAPI TestClient."""
    logger.info("Creating TestClient")
    return TestClient(app)

@pytest.fixture
def image_processor():
    """Фикстура для ImageProcessor."""
    logger.info("Creating ImageProcessor")
    return ImageProcessor()

@pytest.fixture
def animal_recognition_service(mocker):
    """Фикстура для AnimalRecognitionService с замоканными зависимостями."""
    logger.info("Creating AnimalRecognitionService with mocks")
    mocker.patch("app.infrastructure.clip_model.CLIPModelWrapper")
    mocker.patch("app.infrastructure.qdrant_client.QdrantClientWrapper")
    mocker.patch("app.infrastructure.ollama_client.OllamaClientWrapper")
    return AnimalRecognitionService()

@pytest.fixture
def test_image():
    """Фикстура для тестового изображения (cat.png)."""
    image_path = os.path.join(os.path.dirname(__file__), "fixtures/cat.png")
    logger.info(f"Loading test image from {image_path}")
    if not os.path.exists(image_path):
        pytest.fail(f"Test image not found at {image_path}")
    with open(image_path, "rb") as f:
        return f.read()

@pytest.fixture
def test_image_base64(test_image):
    """Фикстура для тестового изображения в формате base64."""
    logger.info("Encoding test image to base64")
    base64_string = base64.b64encode(test_image).decode("utf-8")
    return f"data:image/png;base64,{base64_string}"

@pytest.fixture
def invalid_image():
    """Фикстура для некорректного файла."""
    invalid_path = os.path.join(os.path.dirname(__file__), "fixtures/invalid_image.txt")
    logger.info(f"Loading invalid image from {invalid_path}")
    if not os.path.exists(invalid_path):
        pytest.fail(f"Invalid image not found at {invalid_path}")
    with open(invalid_path, "rb") as f:
        return f.read()