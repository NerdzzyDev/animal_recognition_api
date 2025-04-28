import pytest
from app.utils.exceptions import AppError, ImageProcessingError, EmbeddingGenerationError, QdrantError, OllamaError

@pytest.mark.unit
def test_app_error():
    """Тестирует базовый класс AppError."""
    error = AppError(message="Test error", error_code="TEST_ERROR", details={"key": "value"})
    assert error.message == "Test error"
    assert error.error_code == "TEST_ERROR"
    assert error.details == {"key": "value"}
    assert str(error) == "TEST_ERROR: Test error, Details: {'key': 'value'}"

@pytest.mark.unit
def test_image_processing_error():
    """Тестирует ImageProcessingError."""
    error = ImageProcessingError(
        message="Invalid image",
        error_code="INVALID_IMAGE",
        details={"content_type": "text/plain"}
    )
    assert error.error_code == "INVALID_IMAGE"
    assert str(error) == "INVALID_IMAGE: Invalid image, Details: {'content_type': 'text/plain'}"

@pytest.mark.unit
def test_embedding_generation_error():
    """Тестирует EmbeddingGenerationError."""
    error = EmbeddingGenerationError(message="CLIP failure")
    assert error.error_code == "EMBEDDING_GENERATION_ERROR"
    assert str(error) == "EMBEDDING_GENERATION_ERROR: CLIP failure"

@pytest.mark.unit
def test_qdrant_error():
    """Тестирует QdrantError."""
    error = QdrantError(
        message="Qdrant failure",
        details={"point_id": "123"}
    )
    assert error.error_code == "QDRANT_ERROR"
    assert str(error) == "QDRANT_ERROR: Qdrant failure, Details: {'point_id': '123'}"

@pytest.mark.unit
def test_ollama_error():
    """Тестирует OllamaError."""
    error = OllamaError(
        message="Ollama failure",
        error_code="OLLAMA_FAILURE",
        details={"animal_name": "cat"}
    )
    assert error.error_code == "OLLAMA_FAILURE"
    assert str(error) == "OLLAMA_FAILURE: Ollama failure, Details: {'animal_name': 'cat'}"