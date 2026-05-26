#!/usr/bin/env bash
set -euo pipefail

BOT_TOKEN="${1:-}"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

if [ -n "$BOT_TOKEN" ]; then
  sed -i.bak "s|^BOT_TOKEN=.*$|BOT_TOKEN=${BOT_TOKEN}|" .env && rm -f .env.bak
  echo "BOT_TOKEN updated in .env"
fi

echo "Starting services..."
docker compose up -d --build
echo "Done. API docs: http://localhost:8000/docs"
echo "Follow bot logs: docker compose logs -f bot"
