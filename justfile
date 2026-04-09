set positional-arguments

config_path := "services/intake_service/config/application.yaml"
local_config_path := "services/intake_service/config/local.yaml"
app_module := "intake_service.main:app"

default:
    @just --list

setup:
    uv venv --python 3.11.8 .venv
    uv sync --extra dev

run:
    uv run uvicorn {{app_module}} --app-dir services/intake_service/src --host 0.0.0.0 --port 8000 --reload

run-config path="{{config_path}}":
    INTAKE_CONFIG_PATH={{path}} uv run uvicorn {{app_module}} --app-dir services/intake_service/src --host 0.0.0.0 --port 8000 --reload

migrate:
    cd services/intake_service && uv run alembic upgrade head

migrate-config path="{{config_path}}":
    cd services/intake_service && INTAKE_CONFIG_PATH=../../{{path}} uv run alembic upgrade head

migrate-local:
    cd services/intake_service && INTAKE_CONFIG_PATH=../../{{local_config_path}} uv run alembic upgrade head

test:
    uv run pytest services/intake_service/tests

docs:
    @echo "Swagger UI: http://127.0.0.1:8000/docs"
    @echo "ReDoc: http://127.0.0.1:8000/redoc"
    @echo "OpenAPI JSON: http://127.0.0.1:8000/openapi.json"
