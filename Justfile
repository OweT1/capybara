prudential: 
  uv run python -m src.policies.prudential.link_extraction
  uv run python -m src.policies.prudential.file_extraction

airflow-setup: 
  docker compose up airflow-init

airflow-build:
  docker compose build --no-cache

airflow-up:
  docker compose up -d

airflow-down:
  docker compose down -v --rmi all
