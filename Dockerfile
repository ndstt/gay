FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1

RUN pip install --no-cache-dir "uv==0.7.*"

COPY pyproject.toml .
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .

RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "ingest_pipeline"]
