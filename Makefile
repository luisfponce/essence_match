.PHONY: help lint test build up down migrate

help:
	@printf '%s\n' 'Available targets: lint test build up down migrate'

lint:
	cd frontend && npm run lint

test:
	cd backend && pytest
	cd frontend && npm run test -- --run

build:
	cd frontend && npm run build

up:
	docker compose -f docker-compose.yml -f docker-compose.local.yml --env-file .env up --build

down:
	docker compose -f docker-compose.yml -f docker-compose.local.yml down

migrate:
	cd backend && alembic upgrade head
