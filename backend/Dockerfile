FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

# Separate layer for deps so app-code changes don't bust the dependency cache.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

ENV DJANGO_SETTINGS_MODULE=backend.settings.production
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
