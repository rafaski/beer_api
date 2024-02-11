FROM python:3.11-slim-bullseye

ENV POETRY_VERSION="1.4.2"

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml* /app/

RUN poetry config virtualenvs.create false && poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn",  "app.main:app", "--host","0.0.0.0", "--port", "8080", "--no-access-log"]