# Animal Recognition API

Animal Recognition API — это REST API для распознавания животных на изображениях. Оно использует модель CLIP для генерации эмбеддингов изображений, Qdrant для хранения и поиска похожих эмбеддингов, и Ollama для генерации текстовых описаний животных. API предоставляет эндпоинты для конвертации изображений в base64 и распознавания животных, а также веб-интерфейс для загрузки изображений и просмотра результатов.

## Особенности
- Конвертация изображений в base64 для обработки.
- Распознавание животных с использованием CLIP и Qdrant.
- Генерация описаний животных через Ollama.
- Интерактивная документация API через Swagger UI.
- Полное покрытие тестами с помощью `pytest`.
- Управление зависимостями через `uv` и контейнеризация с Docker.

## Требования
- Python 3.11+
- Docker и Docker Compose
- `uv` для управления зависимостями
- Доступ к GPU (рекомендуется для CLIP и Ollama)

## Структура проекта
```
animal-recognition-api/
├── app/
│   ├── api/                    # API-эндпоинты и модели
│   │   ├── __init__.py
│   │   ├── routes.py           # Маршруты FastAPI
│   │   └── models.py           # Pydantic-модели для запросов/ответов
│   ├── infrastructure/         # Интеграция с внешними сервисами
│   │   ├── __init__.py
│   │   ├── clip_model.py       # Обёртка для CLIP (transformers)
│   │   ├── qdrant_client.py    # Клиент для Qdrant
│   │   ├── ollama_client.py    # Клиент для Ollama
│   │   └── image_processor.py  # Обработка изображений (PIL)
│   ├── services/               # Бизнес-логика
│   │   ├── __init__.py
│   │   └── animal_recognition.py  # Сервис распознавания животных
│   ├── utils/                  # Утилиты
│   │   ├── __init__.py
│   │   ├── exceptions.py       # Пользовательские исключения
│   │   └── translations.py     # Перевод названий животных
│   └── main.py                 # Точка входа FastAPI
├── data/
│   └── animals10/              # Датасет изображений животных
├── templates/
│   └── index.html              # HTML-шаблон для веб-интерфейса
├── tests/                      # Юнит-тесты
│   ├── __init__.py
│   ├── conftest.py             # Фикстуры для pytest
│   ├── test_routes.py          # Тесты API-эндпоинтов
│   ├── test_models.py          # Тесты Pydantic-моделей
│   ├── test_animal_recognition.py  # Тесты сервиса
│   ├── test_image_processor.py # Тесты обработки изображений
│   ├── test_exceptions.py      # Тесты исключений
│   ├── test_translations.py    # Тесты переводов
│   ├── test_docs.py            # Тесты документации
│   └── fixtures/               # Тестовые данные
│       ├── cat.png             # Тестовое изображение
│       └── invalid_image.txt   # Некорректный файл
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Dockerfile для приложения и тестов
└── pyproject.toml              # Зависимости и настройки проекта
```

## Установка

### Локальная установка (без Docker)
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/animal-recognition-api.git
   cd animal-recognition-api
   ```
2. Установите `uv`:
   ```bash
   pip install uv==0.4.18
   ```
3. Установите зависимости:
   ```bash
   uv pip install -e .[dev]
   ```
4. Убедитесь, что Qdrant и Ollama запущены:
   - Qdrant: `docker run -p 6333:6333 qdrant/qdrant:latest`
   - Ollama: `docker run -p 11434:11434 ollama/ollama:latest`

### Установка с Docker
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/animal-recognition-api.git
   cd animal-recognition-api
   ```

## Запуск

### Запуск приложения
1. Запустите сервисы с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```
2. Проверьте, что API работает:
   ```bash
   curl http://localhost:8000/health
   # Ожидаемый ответ: {"status": "healthy"}
   ```
3. Откройте веб-интерфейс: `http://localhost:8000`
4. Документация API доступна по: `http://localhost:8000/docs`

### Запуск тестов
1. Пересоберите образы:
   ```bash
   docker-compose build
   ```
2. Запустите тесты:
   ```bash
   docker-compose run tests
   ```
3. Отчёт покрытия будет сохранён в `htmlcov/`. Откройте `htmlcov/index.html` в браузере.

## Использование

### Веб-интерфейс
1. Перейдите на `http://localhost:8000`.
2. Загрузите изображение через форму.
3. Просмотрите результаты распознавания и галерею животных.

### API
Используйте Swagger UI (`http://localhost:8000/docs`) для интерактивного тестирования или отправляйте запросы через `curl`.

#### Эндпоинт: Конвертация изображения в base64
```bash
curl -X POST -F "image=@tests/fixtures/cat.png" http://localhost:8000/image_to_base64
```
**Ответ**:
```json
{
  "base64_image": "data:image/png;base64,iVBORw0KGgo..."
}
```

#### Эндпоинт: Распознавание животного
```bash
curl -X POST http://localhost:8000/what_is_animal \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "query": "Какое это животное?",
    "timestamp": "2025-04-25T13:59:27.740855",
    "image": "data:image/png;base64,iVBORw0KGgo..."
  }'
```
**Ответ**:
```json
{
  "animal": "кошка",
  "description": "Кошка - это четвероногое с мягкой шерстью.",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "answer": "На изображении, вероятно, кошка.",
  "timestamp": "2025-04-25T13:59:27.740855",
  "similarities": [...]
}
```

## Тестирование
Проект покрыт юнит-тестами с помощью `pytest`. Тесты включают:
- Проверку API-эндпоинтов (`test_routes.py`).
- Валидацию Pydantic-моделей (`test_models.py`).
- Тестирование сервиса распознавания (`test_animal_recognition.py`).
- Проверку обработки изображений (`test_image_processor.py`).
- Тестирование исключений и переводов (`test_exceptions.py`, `test_translations.py`).
- Проверку OpenAPI-документации (`test_docs.py`).

Для запуска тестов локально:
```bash
uv pip install -e .[dev]
pytest -v --cov=app --cov-report=html
```

## Разработка

### Логирование
Логи приложения записываются в stdout/stderr. Просмотрите их:
```bash
docker-compose logs fastapi
```

## Лицензия
MIT License. См. [LICENSE](LICENSE) для подробностей.



