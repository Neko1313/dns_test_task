#!/bin/sh
# entrypoint.sh

# Проверка переменной окружения и запуск соответствующих команд
if [ "$IS_TEST" = "1" ]; then
    echo "Running in test mode"
    # Запуск команд для тестового режима
    alembic upgrade head && pytest -v -s tests/
else
    echo "Running in production mode"
    # Запуск команд для продуктивного режима
    alembic upgrade head && cd src && uvicorn main:app --reload --host 0.0.0.0 --port 5000
fi
