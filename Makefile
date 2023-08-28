up_local:
	docker compose -f docker-compose-local.yaml up -d

down_local:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

up:
	docker-compose up

down:
	docker-compose down && docker network prune --force