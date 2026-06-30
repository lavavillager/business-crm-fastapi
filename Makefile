.PHONY: help install run test migrate seed up down lint

help:
	@echo "install  - установить зависимости"
	@echo "run      - запустить dev-сервер (uvicorn)"
	@echo "test     - запустить тесты"
	@echo "migrate  - применить миграции Alembic"
	@echo "seed     - загрузить демо-данные"
	@echo "up       - поднять стек в Docker"
	@echo "down     - остановить стек"

install:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -q

migrate:
	alembic upgrade head

seed:
	python -m app.db.seed

up:
	docker compose up --build

down:
	docker compose down
