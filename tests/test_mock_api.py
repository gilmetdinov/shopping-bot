"""Smoke-тесты mock-сервера: полный флоу заказа без реального магазина."""
from __future__ import annotations

from fastapi.testclient import TestClient

from mock_api.app import app

client = TestClient(app)


def _post(path, **body):
    return client.post(path, json=body)


def test_bind_check_unbind():
    chat_id = 101
    assert _post("/api/telegram/check-user", chat_id=chat_id).json()["is_bound"] is False

    assert _post("/api/telegram/bind", chat_id=chat_id, key="k", username="u").json()["status"] == "success"
    assert _post("/api/telegram/check-user", chat_id=chat_id).json()["is_bound"] is True

    assert _post("/api/telegram/unbind", chat_id=chat_id).json()["is_bound"] is False


def test_service_list_and_balance():
    chat_id = 102
    _post("/api/telegram/bind", chat_id=chat_id, key="k")

    for _type in ("service", "product", "product_b", "product_c"):
        lst = _post("/api/telegram/get-service-list", type=_type, chat_id=chat_id).json()["list"]
        assert len(lst) > 0
        assert {"short", "label", "price"} <= set(lst[0].keys())

    assert _post("/api/telegram/get-balance", chat_id=chat_id).json()["balance"] == 1000.0


def test_make_order_and_list():
    chat_id = 103
    _post("/api/telegram/bind", chat_id=chat_id, key="k")

    resp = _post(
        "/api/telegram/make-order",
        chat_id=chat_id,
        order_data={"type": "product", "service_label": "Товар A1", "price": 150.0},
    ).json()
    assert resp["status"] == "success"
    assert resp["order_id"] > 0

    orders = _post("/api/telegram/get-order-list", chat_id=chat_id, type="product").json()["orders"]
    assert len(orders) == 1
    first = list(orders.values())[0]
    assert first["service_label"] == "Товар A1"
    assert first["status"] in ("waiting", "done", "canceled", "error")


def test_order_info_and_additional():
    chat_id = 104
    _post("/api/telegram/bind", chat_id=chat_id, key="k")
    order = _post(
        "/api/telegram/make-order",
        chat_id=chat_id,
        order_data={"type": "product", "service_label": "Товар A1", "price": 150.0},
    ).json()

    info = _post("/api/telegram/get-order-info", chat_id=chat_id, order_id=order["order_id"]).json()
    assert info["order_info"]["id"] == order["order_id"]

    extra = _post("/api/telegram/get-order-additional-info", chat_id=chat_id, order_id=order["order_id"]).json()
    assert extra["status"] == "success"
    assert extra["info"]["order_id"] == order["order_id"]
