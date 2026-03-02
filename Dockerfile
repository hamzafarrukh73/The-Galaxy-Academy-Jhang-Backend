# Stage 1: Build dependencies
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv export --format requirements-txt --no-dev > requirements.txt
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim
WORKDIR /app
# Install libpq for postgres support
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

# We use a shell script or multiple commands to migrate then start
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
