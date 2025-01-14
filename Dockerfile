FROM python:3.13-slim

ARG POETRY_VERSION=2.0.1

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /opt/service

COPY pyproject.toml poetry.lock /opt/service/
COPY app /opt/service/app/

RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
