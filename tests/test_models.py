import pytest
from pydantic import ValidationError
from app.api.models import AnimalRequest, AnimalResponse, ImageToBase64Response
from datetime import datetime
from uuid import UUID

@pytest.mark.unit
def test_image_to_base64_response():
    """Тестирует валидацию ImageToBase64Response."""
    model = ImageToBase64Response(base64_image="data:image/png;base64,iVBORw0KGgo...")
    assert model.base64_image == "data:image/png;base64,iVBORw0KGgo..."

@pytest.mark.unit
def test_animal_request_valid():
    """Тестирует валидацию корректного AnimalRequest."""
    data = {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "query": "Какое это животное?",
        "timestamp": "2025-04-25T13:59:27.740855",
        "image": "data:image/png;base64,iVBORw0KGgo..."
    }
    model = AnimalRequest(**data)
    assert model.user_id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert model.query == "Какое это животное?"

@pytest.mark.unit
def test_animal_request_invalid_uuid():
    """Тестирует обработку некорректного UUID в AnimalRequest."""
    data = {
        "user_id": "invalid-uuid",
        "query": "Какое это животное?",
        "timestamp": "2025-04-25T13:59:27.740855",
        "image": "data:image/png;base64,iVBORw0KGgo..."
    }
    with pytest.raises(ValidationError):
        AnimalRequest(**data)

@pytest.mark.unit
def test_animal_response_valid():
    """Тестирует валидацию корректного AnimalResponse."""
    data = {
        "animal": "кошка",
        "description": "Кошка - это четвероногое с мягкой шерстью.",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "answer": "На изображении, вероятно, кошка.",
        "timestamp": datetime.utcnow(),
        "similarities": [
            {
                "id": "b3ed7bd5-8b28-4843-9853-6d4302798511",
                "score": 0.81,
                "metadata": {"animal_name": "cat", "is_reference": True},
                "description": "Кошка - это четвероногое с мягкой шерстью."
            }
        ]
    }
    model = AnimalResponse(**data)
    assert model.animal == "кошка"
    assert len(model.similarities) == 1