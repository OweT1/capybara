great-eastern:
  uv run python -m src.policies.great_eastern.link_extraction
  uv run python -m src.policies.great_eastern.file_extraction

airflow-setup: 
  docker compose up airflow-init

airflow-build:
  docker compose build --no-cache

airflow-up:
  docker compose up -d

airflow-down:
  docker compose down -v --rmi all
