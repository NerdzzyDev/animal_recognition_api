from typing import Optional, Any


class AppError(Exception):
    """Базовый класс для всех пользовательских исключений приложения."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        """
        Инициализирует исключение с сообщением, кодом ошибки и дополнительными деталями.

        Args:
            message (str): Сообщение об ошибке.
            error_code (Optional[str]): Код ошибки для идентификации (например, 'INVALID_IMAGE').
            details (Optional[Any]): Дополнительные данные об ошибке (например, имя файла, ID).
        """
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Возвращает строковое представление ошибки с кодом и деталями."""
        details_str = f", Details: {self.details}" if self.details else ""
        return f"{self.error_code}: {self.message}{details_str}"


class TranslationError(AppError):
    pass


class ImageProcessingError(AppError):
    """Исключение для ошибок обработки изображений (декодирование, валидация, конвертация)."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        """
        Инициализирует исключение для ошибок обработки изображений.

        Args:
            message (str): Сообщение об ошибке.
            error_code (Optional[str]): Код ошибки (например, 'INVALID_BASE64').
            details (Optional[Any]): Дополнительные данные (например, content_type).
        """
        super().__init__(message, error_code or "IMAGE_PROCESSING_ERROR", details)


class EmbeddingGenerationError(AppError):
    """Исключение для ошибок генерации эмбеддингов с помощью CLIP."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        """
        Инициализирует исключение для ошибок генерации эмбеддингов.

        Args:
            message (str): Сообщение об ошибке.
            error_code (Optional[str]): Код ошибки (например, 'CLIP_MODEL_FAILURE').
            details (Optional[Any]): Дополнительные данные (например, модель).
        """
        super().__init__(message, error_code or "EMBEDDING_GENERATION_ERROR", details)


class QdrantError(AppError):
    """Исключение для ошибок работы с Qdrant (хранение, поиск эмбеддингов)."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        """
        Инициализирует исключение для ошибок Qdrant.

        Args:
            message (str): Сообщение об ошибке.
            error_code (Optional[str]): Код ошибки (например, 'QDRANT_STORE_FAILURE').
            details (Optional[Any]): Дополнительные данные (например, point_id).
        """
        super().__init__(message, error_code or "QDRANT_ERROR", details)


class OllamaError(AppError):
    """Исключение для ошибок работы с Ollama (генерация описаний)."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        """
        Инициализирует исключение для ошибок Ollama.

        Args:
            message (str): Сообщение об ошибке.
            error_code (Optional[str]): Код ошибки (например, 'OLLAMA_GENERATION_FAILURE').
            details (Optional[Any]): Дополнительные данные (например, animal_name).
        """
        super().__init__(message, error_code or "OLLAMA_ERROR", details)
