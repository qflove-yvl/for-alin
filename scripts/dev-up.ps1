Param(
    [string]$BotToken = ""
)

$ErrorActionPreference = "Stop"

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}

if ($BotToken -ne "") {
    (Get-Content ".env") -replace '^BOT_TOKEN=.*$', "BOT_TOKEN=$BotToken" | Set-Content ".env"
    Write-Host "BOT_TOKEN updated in .env"
}

Write-Host "Starting services..."
docker compose up -d --build
Write-Host "Done. API docs: http://localhost:8000/docs"
Write-Host "Follow bot logs: docker compose logs -f bot"
