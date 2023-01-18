# Меню на FastAPI


# Технологии:
    Python 3.10
    FastAPI 
    PostgreSQL
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

5. Перейти в категорию app:

```cd app```

6. Создать и наполнить файл .env:
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

7. Запустить проект:

```uvicorn main:app --reload```

Документация по API доступна по ссылке http://127.0.0.1:8000/docs

Автор:

Павел Киселев





