.PHONY: up down logs bot-logs

up:
	./scripts/dev-up.sh

down:
	docker compose down

logs:
	docker compose logs -f

bot-logs:
	docker compose logs -f bot
