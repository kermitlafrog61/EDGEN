run_dev:
	docker-compose -f docker-compose-dev.yml up -d

run_prod:
	docker-compose -f docker-compose-prod.yml up -d

superuser:
	docker exec edgen_api_1 python createsuperuser

down:
	docker compose -f docker-compose-dev.yml down
