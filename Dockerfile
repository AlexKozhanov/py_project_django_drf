# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости Python
RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev,test --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ENV SECRET_KEY="django-insecure-=_hu2+5ccw!3cddtq6e4aqmc@624gf0$w5jiyj5qg!d-cp)xa6"
ENV CELERY_BROKER_URL="redis://localhost:6379/0"
ENV CELERY_BACKEND="redis://localhost:6379/0"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

