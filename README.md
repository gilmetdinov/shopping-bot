# shopping-bot

A customer-facing **Telegram bot for an online store**, built on aiogram 3. It
binds a Telegram account to a store profile, sends order/balance notifications,
and lets customers browse and manage their purchases directly from chat.

## Features

- **Profile binding** — link a Telegram account to a store profile (via the store
  site), with bound/unbound flows handled separately.
- **Notifications** — balance refills and order fulfilment pushed to Telegram
  (single and mass send, MarkdownV2).
- **Order management** — four abstract order types (`service`, `product`,
  `product_b`, `product_c`) with per-status rendering (canceled / waiting / done
  / error).
- **Replenishment flow** — guided top-up process from chat.
- **Web app + API client** — a FastAPI web part and a store REST API client
  (request builder/sender) with request signing.
- **Anti-phishing hygiene** — support/channel links are emitted only through the
  store-configured URLs, never hardcoded.

## Architecture

A layered design, 120+ modules:

```
api/         store REST API client (request builder + sender)
bot/         Telegram layer
  client/      aiogram Bot wrapper (webhook, commands, mass send)
  handler/     dto / processes / handlers / factories — business logic
  keyboards/   inline/reply keyboards
  router/      route registration
  states/      FSM states
message/      message builder (env-driven links, markdown escaping)
utils/        markdown, date, enums, sign, factories
mock_api/     local mock of the store backend (FastAPI)
web/          web app entry points
config/       routing config
```

Business logic is split into DTOs (data bundles), **processes** (step flows) and
**handlers** (actions), assembled through factories — keeping the FSM layer thin
and the logic testable.

## Stack

- Python 3.11+, aiogram 3, aiohttp, python-dotenv, pytz
- FastAPI (web part + mock API), Docker

## Configuration

All store-specific values come from environment variables (see `.env.example`):

```
TOKEN, WEBHOOK_URL           bot + webhook
API_BASE_URL, HOOK_KEY       store API
TG_CHANNEL_1, TG_CHANNEL_2   notification channels
SUPPORT_TG, PROJECT_NAME     support link / project name
SITE_URL, SETTINGS_URL       store site / profile settings
REFILL_HISTORY_URL, ORDERS_URL
```

```bash
cp .env.example .env   # fill in
docker compose up --build
```

## Mock server

A local FastAPI mock emulates the store backend (see `docs/mock-server-plan.md`),
so the full order flow works without a real store:

```bash
python -m mock_api            # serves on http://localhost:8844
```

Point the bot at it via `API_BASE_URL=http://localhost:8844`.

## Tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install aiogram aiohttp python-dotenv pytz fastapi uvicorn httpx pytest pytest-asyncio
python -m pytest tests/
```

Covers the mock API endpoints (`test_mock_api.py`) and the bot's `ApiClient`
against a live mock server (`test_api_flow.py`).

## History

Originally built in **2022** as a production Telegram bot for a specific store.
On **14.09.2026** it was scrubbed of store specifics and personal identifiers,
upgraded from aiogram 3.0.0b7 to aiogram 3.x, and finalized for the portfolio:
abstract order types (`service` / `product` / `product_b` / `product_c`), a mock
store API, and tests.
