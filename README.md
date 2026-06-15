# capybara 🦫

## Set-up ⚙️

1. You must have `uv` installed. You can do so by:

```
pip install uv
```

2. Afterwards, you can set-up your environment by running:

```
uv venv # Initialise virtual environment
.venv\Scripts\activate # Activate virtual environment (Windows)
uv sync --all-extras # Install necessary dependencies into virtual environment
```

> [!NOTE]
> Alternatively, if you are using Linux to do your virtual environment, then you should do:
>
> ```
> python3 -m venv .venv
> source .venv/bin/activate
> uv sync --all-extras
> ```

3. You will also need to copy over the environmental variables required. To do so, you can run:

```
cp .env.example .env
```

### Docker 🐳

Additionally, for our project, we will require the use of Docker.

To install it, you may find the appropriate installation for your operating system at https://docs.docker.com/engine/install/.

## Airflow 💨

To run airflow, we are only able to run it on Linux/Mac.

To set-up the necessary tables, do:

```bash
airflow db migrate
```

Then, to run the airflow server, do:

```bash
airflow api-server -p 8080 -H localhost
```

From there, click the URL and login using the details found in the system messages.

> [!NOTE] For windows, we will need to install WSL (Windows Subsystem for Linux).
> This can be easily done by doing `wsl --install`.

### Docker 🐳

Alternatively, an easier way of using Airflow is via Docker.

The guide to do so can be found at https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html.

> [!NOTE] Before this, you must ensure that Docker is installed and is running in the background.

From the guide, the first step is to initialise the database, which is done so by doing:

```bash
docker compose up airflow-init
```

or the corresponding just command:

```bash
just airflow-setup
```

From there, you can build the Airflow docker image:

```bash
  docker compose build
```

or the corresponding just command:

```bash
just airflow-build
```

Then you can run the following to start up Airflow:

```bash
docker compose up
```

or the corresponding just command:

```bash
just airflow-up
```

To interact with the service, there are a few ways (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#accessing-the-environment).

One way would be to access the web UI interface at http://localhost:8080. The default account username is `airflow` with password `airflow`.

To tear down the Airflow Docker instance, you can do:

```bash
docker compose down -v --rmi all
```

or the corresponding just command:

```bash
just airflow-down
```

## Development 🛠️

For development, we have set up pre commit checks with ruff. To ensure that the pre commit checks are working, you must install them:

```shell
pre-commit install
```

Additionally, we will also use `just` commands to simplify some of our development works. For more information, you can refer to: https://github.com/casey/just.

To install it, you can do:

```shell
uv tool install rust-just
```

For the airflow server, you can run the server in development mode by doing:

```bash
airflow api-server -p 8080 -H localhost -d
```
