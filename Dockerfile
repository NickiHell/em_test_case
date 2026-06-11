FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.14-slim AS runtime
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=src.config.settings

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/
COPY manage.py ./

RUN useradd -m web && chown -R web:web /app
USER web

EXPOSE 8000
CMD ["gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]