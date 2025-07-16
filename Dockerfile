FROM python:3.12-slim

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry install --no-dev

COPY . /app

CMD ["uvicorn","src/main:app","--host","0.0.0.0","80"]
