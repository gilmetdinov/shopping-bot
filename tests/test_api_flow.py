"""Интеграционный тест: ApiClient бота против живого mock-сервера.

Проверяет, что клиентский слой бота (запросы + подпись) корректно ходит на mock —
то есть бот остаётся рабочим против эмулированного магазина.
"""
from __future__ import annotations

import threading
import time
import urllib.request

import pytest
import uvicorn

from api import ApiClient


class _FakeDto:
    def order_data(self):
        return {"type": "product", "service_label": "Товар A1", "price": 150.0}


@pytest.fixture(scope="module")
def mock_base_url():
    config = uvicorn.Config("mock_api.app:app", host="127.0.0.1", port=8845, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    base = "http://127.0.0.1:8845"
    for _ in range(100):
        try:
            urllib.request.urlopen(f"{base}/api/telegram/", timeout=1)
            break
        except Exception:
            time.sleep(0.1)
    yield base
    server.should_exit = True
    thread.join(timeout=5)


@pytest.mark.asyncio
async def test_api_client_flow_against_mock(mock_base_url):
    api = ApiClient(mock_base_url)
    chat_id = 4242

    ping = await api.ping()
    assert ping["status"] == "success"

    assert (await api.check_user(chat_id))["is_bound"] is False
    await api.bind(key="test-key", chat_id=chat_id, username="tester")
    assert (await api.check_user(chat_id))["is_bound"] is True

    for _type in ("service", "product", "product_b", "product_c"):
        lst = (await api.get_service_list(_type, chat_id))["list"]
        assert lst and "short" in lst[0]

    assert (await api.get_balance(chat_id))["balance"] == 1000.0

    order = await api.make_order(chat_id, "product", _FakeDto())
    assert order["status"] == "success"

    orders = (await api.get_order_list(chat_id, "product", 1))["orders"]
    assert len(orders) == 1
