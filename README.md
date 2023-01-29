# Меню на FastAPI


# Технологии:
    Python 3.10
    FastAPI
    PostgreSQL
    Pytest
    Docker (docker-compose)

# Запуск и работа с проектом

1. Клонировать репозиторий к себе на локальную машину:

```git clone git@github.com:kiselev-pavel-dev/fastapi_menu_cafe.git```

2. Перейти в директорию с проектом:

```cd fastapi_menu_cafe```

3. Создать и активировать виртуальное окружение:

```python -m venv venv```
```source venv/scripts/activate```

4. Установить зависимости:

```pip install -r requirements.txt```

5. Создать и наполнить файл .env:
```
POSTGRES_DB=postgres
POSTGRES_DB_TESTS=tests
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
PGUSER=postgres

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```
6. Если запускаете проект локально, то в файле src/settings.py укажите:

```settings = Settings(docker_mode=False)```

Если через docker, то:

```settings = Settings(docker_mode=True)```

7. Запустить проект:

```docker-compose up -d --build```

8. Для запуска тестов выполните комманду:

```docker-compose -f docker-compose.tests.yaml up -d --build```

Документация по API доступна по ссылке http://127.0.0.1:8000/docs

Автор:

Павел Киселев
