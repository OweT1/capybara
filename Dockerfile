# Airflow image
FROM apache/airflow:3.2.2

# Working directory
WORKDIR /opt/airflow

# Get uv and sync dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY pyproject.toml uv.lock ./

USER airflow
RUN uv sync --frozen --no-cache