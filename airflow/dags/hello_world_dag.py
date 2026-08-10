from datetime import datetime
from airflow.decorators import dag, task


@dag(
    dag_id="hello_world_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example"],
)
def hello_world_pipeline():
    @task()
    def get_message():
        return "Hello"

    @task()
    def print_full_message(greeting: str):
        print(f"{greeting}, World!")

    greeting_text = get_message()
    print_full_message(greeting_text)


hello_world_pipeline()
