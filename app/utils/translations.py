import logging


class TranslationError(Exception):
    pass


def translate_animal_name(animal_name: str, target_language: str = "ru") -> str:
    """
    Переводит имя животного на указанный язык.

    Args:
        animal_name: Название животного на английском.
        target_language: Целевой язык перевода (например, 'ru' для русского).

    Returns:
        Переведённое имя животного.

    Raises:
        TranslationError: Если перевод не найден.
    """
    logger = logging.getLogger(__name__)

    # Простой словарь переводов для демонстрации
    translations = {
        "cat": {"ru": "кошка", "en": "cat"},
        "dog": {"ru": "собака", "en": "dog"},
        "horse": {"ru": "лошадь", "en": "horse"},
    }

    try:
        if animal_name.lower() not in translations:
            logger.warning(f"No translation found for animal: {animal_name}")
            return animal_name  # Возвращаем исходное имя, если перевод не найден
        translated_name = translations[animal_name.lower()].get(target_language, animal_name)
        logger.info(f"Translated {animal_name} to {translated_name} for language {target_language}")
        return translated_name
    except Exception as e:
        logger.error(f"Failed to translate animal name: {str(e)}")
        raise TranslationError(f"Failed to translate {animal_name}: {str(e)}")