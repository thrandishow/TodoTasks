FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --only main --no-interaction --no-root

COPY . .

ENV PYTHONPATH=/app

CMD ["poetry","run","uvicorn","src.main:app","--host","0.0.0.0","--port","5000"]
