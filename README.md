# Viloyatga Boramiz — MVP

MVP starter: FastAPI + SQLAlchemy 2 + PostgreSQL, Aiogram 3 bot, Next.js + TypeScript + Tailwind.
This is a development starter, not a production-certified deployment. Payment provider, SMS/phone auth,
map tiles/geocoding, legal review, and live Telegram credentials must be configured before production.

## Requirements
- Docker + Docker Compose
- Telegram bot token (optional for web-only development)

## Run
1. Copy `.env.example` to `.env` and set secrets.
2. Run `docker compose up --build`.
3. API docs: http://localhost:8000/docs
4. Frontend: http://localhost:3000

The first MVP includes trip publishing/search, driver trial-period calculation, trip ownership checks,
and a basic responsive Uzbek interface. Expand authentication and production hardening before launch.
