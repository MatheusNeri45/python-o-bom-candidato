FROM python:3.12-slim AS base

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

RUN poetry run pip install fastapi[standard]

RUN mkdir /app/o_bom_candidato_files

COPY . .

EXPOSE 8000

CMD ["poetry", "fastapi", "run", "./python_o_bom_candidato/app.py", "--port", "8000"]

