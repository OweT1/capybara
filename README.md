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
