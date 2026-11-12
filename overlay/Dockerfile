FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc libc6-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir "poetry==1.4.2" \
    && poetry install --no-dev --no-ansi --no-root \
    && pip install --no-cache-dir --force-reinstall "psycopg2-binary==2.9.9"

COPY . ./

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn --host=0.0.0.0 --port=8000 app.main:app"]
