FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install

COPY ./ /app/

ENTRYPOINT ["/app/entrypoint.sh"]