# Базовый образ
FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Установка uv
RUN pip install uv

# Копирование pyproject.toml для установки зависимостей
COPY pyproject.toml .

# Установка основных и разработческих зависимостей с помощью uv
RUN uv pip install --system -e . && uv pip install --system -e .[dev]

# Копирование исходного кода
COPY app ./app
COPY templates ./templates
COPY tests ./tests

# Установка переменной окружения для Python
ENV PYTHONPATH=/app

# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]