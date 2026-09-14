"""Dev-запуск бота в режиме long polling (для локального прогона против mock API).

Продакшн работает через webhook (`app.py` + aiohttp web server); polling нужен
только для локальной разработки/демо, когда нет публичного URL для webhook.

Запуск:
    python run_polling.py
"""
from __future__ import annotations

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

from api import ApiClient
from bot.router import Router
from bot.commands import get_commands_array

load_dotenv()


async def main() -> None:
    # Прокси из окружения (нужен для доступа к api.telegram.org за VPN/файрволом).
    proxy = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    session = AiohttpSession(proxy=proxy) if proxy else None

    bot = Bot(token=os.getenv("TOKEN"), session=session)
    api = ApiClient(base_url=os.getenv("API_BASE_URL"))
    router = Router(api=api)

    dp = Dispatcher()
    dp.include_router(router.instance)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(get_commands_array())
    print(f"Polling started; mock API at {os.getenv('API_BASE_URL')}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
