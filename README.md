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
> Alternatively, if you are using MacOS/Linux to do your virtual environment, then you should do:
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

To run airflow, we have 2 methods: Airflow Server (direct) or Docker.

### Airflow Server 🌐

For this, we are only able to run it on Linux/Mac.

1.  Set-up the necessary tables:

```bash
airflow db migrate
```

2.  Then, run the airflow server:

```bash
airflow api-server -p 8080 -H localhost
```

3.  From there, click the URL and login using the details found in the system messages.

> [!NOTE]
> For windows, we will need to install WSL (Windows Subsystem for Linux).
> This can be easily done by doing `wsl --install`.

### Docker 🐳

Alternatively, an easier way of using Airflow is via Docker.

The guide to do so can be found at https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html.

> [!NOTE]
> Before this, you must ensure that Docker is installed and is running in the background.

1. The first step is to initialise the database:

- `docker compose up airflow-init` OR
- `just airflow-setup`

2. Build the Airflow docker image:

- `docker compose build` OR
- `just airflow-build`

3. Run the following to start up Airflow:

- `docker compose up` OR
- `just airflow-up`

4. To interact with the service, there are a few ways (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#accessing-the-environment).

- One way would be to access the web UI interface at http://localhost:8080.
- The default account username is `airflow` with password `airflow`.

5. To tear down the Airflow Docker instance, you can do:

- `docker compose down -v --rmi all` OR
- `just airflow-down`

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
