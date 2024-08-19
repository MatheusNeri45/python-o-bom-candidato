FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

FROM python:3.12-slim AS base

COPY --from=builder /app /app
WORKDIR /app
EXPOSE 8000
ENV PATH "/app/.venv/bin:$PATH"
CMD ["fastapi", "run", "./python_o_bom_candidato/app.py", "--port", "8000"]
#CMD ["uvicorn", "app.python_o_bom_candidato.app:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "-m", "uvicorn", "app.python_o_bom_candidato.app:app", "--host", "0.0.0.0", "--port", "8000"]
