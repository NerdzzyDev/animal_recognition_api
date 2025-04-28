import pytest
from app.services.animal_recognition import AnimalRecognitionService
from app.utils.exceptions import ImageProcessingError, EmbeddingGenerationError, QdrantError, OllamaError, \
    TranslationError
from datetime import datetime


def test_recognize_animal_success(animal_recognition_service, test_image_base64, mocker):
    mocker.patch.object(
        animal_recognition_service.clip_model,
        "generate_embedding",
        return_value=[0.1] * 512
    )
    mocker.patch.object(
        animal_recognition_service.qdrant_client,
        "search_similar",
        return_value=[{"id": 1, "metadata": {"animal_name": "cat"}, "score": 0.9}]
    )
    mocker.patch.object(
        animal_recognition_service.ollama_client,
        "generate_description",
        return_value="A small feline."
    )

    response = animal_recognition_service.recognize_animal(
        base64_image=test_image_base64,
        user_id="123e4567-e89b-12d3-a456-426614174000",
        query="Какое это животное?",
        timestamp=datetime.now()
    )

    assert response.animal == "кошка"
    assert response.description == "A small feline."
    assert response.user_id == "123e4567-e89b-12d3-a456-426614174000"


def test_recognize_animal_invalid_image(animal_recognition_service):
    with pytest.raises(ImageProcessingError) as exc_info:
        animal_recognition_service.recognize_animal(
            base64_image="invalid-base64-string",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            query="Какое это животное?",
            timestamp=datetime.now()
        )
    assert "Invalid base64" in str(exc_info.value)

