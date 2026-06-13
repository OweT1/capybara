# capybara

## Set-up

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

### Development

For development, we have set up pre commit checks with ruff. To ensure that the pre commit checks are working, you must install them:

```shell
pre-commit install
```

Additionally, we will also use `just` commands to simplify some of our development works. For more information, you can refer to: https://github.com/casey/just.

To install it, you can do:

```shell
uv tool install rust-just
```
