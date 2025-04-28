import pytest
from app.utils.translations import translate_animal_name

@pytest.mark.unit
def test_translate_animal_name_known():
    """Тестирует перевод известного животного."""
    assert translate_animal_name("cat") == "кошка"
    assert translate_animal_name("DOG") == "собака"

@pytest.mark.unit
def test_translate_animal_name_unknown():
    """Тестирует перевод неизвестного животного."""
    assert translate_animal_name("unknown") == "unknown"