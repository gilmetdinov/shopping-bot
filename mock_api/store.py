"""In-memory store for the mock store API.

Emulates the store backend the bot talks to via `api.ApiClient`. All state is
ephemeral: profiles, balances, service lists, order cache and orders.

Форматы ответов повторяют контракт реального бэкенда (см. `api.ApiClient` и
`bot/handler/handlers`), чтобы бот работал против mock без изменений.
"""
from __future__ import annotations

import itertools
import time
from typing import Any, Optional

# абстрактный каталог: 4 типа заказов (service / product / product_b / product_c)
SERVICE_LISTS: dict[str, list[dict]] = {
    "service": [
        {"short": "svc-basic", "label": "Базовая услуга", "price": 100.0},
        {"short": "svc-plus", "label": "Расширенная услуга", "price": 250.0},
        {"short": "svc-pro", "label": "Приоритетная услуга", "price": 500.0},
    ],
    "product": [
        {"short": "prod-a1", "label": "Товар A1", "price": 150.0},
        {"short": "prod-a2", "label": "Товар A2", "price": 300.0},
        {"short": "prod-a3", "label": "Товар A3", "price": 450.0},
    ],
    "product_b": [
        {"short": "prod-b1", "label": "Товар B1", "price": 600.0},
        {"short": "prod-b2", "label": "Товар B2", "price": 900.0},
    ],
    "product_c": [
        {"short": "prod-c1", "label": "Товар C1", "price": 750.0},
        {"short": "prod-c2", "label": "Товар C2", "price": 1200.0},
    ],
}


class Store:
    def __init__(self) -> None:
        self._ids = itertools.count(1)
        self.profiles: dict[int, dict[str, Any]] = {}
        self.balances: dict[int, float] = {}
        self.notif_settings: dict[int, dict[str, bool]] = {}
        self.order_caches: dict[int, dict[str, Any]] = {}
        self.orders: dict[int, list[dict[str, Any]]] = {}

    # --- profiles / binding ---
    def is_bound(self, chat_id: int) -> bool:
        return chat_id in self.profiles

    def bind(self, chat_id: int, key: str, username: str = "") -> dict:
        # Идемпотентно: повторный bind не падает, просто подтверждает привязку.
        self.profiles.setdefault(chat_id, {"chat_id": chat_id, "key": key, "username": username})
        self.balances.setdefault(chat_id, 1000.0)
        return {"status": "success", "is_bound": True}

    def unbind(self, chat_id: int) -> dict:
        self.profiles.pop(chat_id, None)
        return {"status": "success", "is_bound": False}

    # --- balance ---
    def balance(self, chat_id: int) -> float:
        return self.balances.setdefault(chat_id, 0.0)

    def debit(self, chat_id: int, amount: float) -> bool:
        if self.balance(chat_id) < amount:
            return False
        self.balances[chat_id] -= amount
        return True

    # --- service list ---
    def service_list(self, _type: str):
        if _type == "docs":
            # формат для docs_type_keyboard: {str(docs_type): цена}
            return {"1": 50.0, "4": 30.0}
        base = _type.split("_", 1)[0]
        return list(SERVICE_LISTS.get(base, SERVICE_LISTS["product"]))

    @staticmethod
    def _price_for(short: str, amount: float = 1) -> float:
        for lst in SERVICE_LISTS.values():
            for item in lst:
                if item["short"] == short:
                    return float(item["price"]) * amount
        return 100.0

    # --- order cache ---
    def _default_order_cache(self, chat_id: int) -> dict:
        return {
            "id": next(self._ids),
            "chat_id": chat_id,
            "service": "",
            "service_label": "",
            "service_price": 0,
            "product": None,
            "data_type": 1,
            "data_price": 0,
            "priority": 0,
            "priority_price": 100.0,
            "data": {},
        }

    def get_order_cache(self, chat_id: int) -> dict:
        if chat_id not in self.order_caches:
            self.order_caches[chat_id] = self._default_order_cache(chat_id)
        return self.order_caches[chat_id]

    def update_order_cache(self, chat_id: int, order_data: dict) -> dict:
        cache = self.get_order_cache(chat_id)
        cache.update(order_data)
        return {"status": "success", "order_cache_id": cache["id"]}

    # --- orders ---
    def _order_price(self, order_data: dict) -> float:
        _type = order_data.get("type")
        if _type == "service":
            return (float(order_data.get("service_price") or 0)
                    + float(order_data.get("docs_price") or 0)
                    + float(order_data.get("priority_price") or 0) * float(order_data.get("priority") or 0))
        amount = float(order_data.get("amount") or 1)
        return self._price_for(order_data.get("service", ""), amount)

    def make_order(self, chat_id: int, order_data: dict) -> dict:
        price = self._order_price(order_data)
        if not self.debit(chat_id, price):
            return {"status": "error", "code": -6}
        order = {
            "id": next(self._ids),
            "chat_id": chat_id,
            "type": order_data.get("type", "product"),
            "service_label": order_data.get("service_label", "Товар"),
            "status": "done",
            "price": price,
            "created_at": time.strftime("%d.%m.%Y %H:%M"),
            "data": order_data,
        }
        self.orders.setdefault(chat_id, []).append(order)
        return {"status": "success", "order_id": order["id"],
                "order_ids": [order["id"]], "order_price": price}

    def _find_order(self, chat_id: int, order_id: int) -> Optional[dict]:
        for o in self.orders.get(chat_id, []):
            if o["id"] == order_id:
                return o
        return None

    def order_list(self, chat_id: int, _type: str = None) -> dict:
        orders = [o for o in self.orders.get(chat_id, []) if not _type or o["type"] == _type]
        return {str(o["id"]): {"service_label": o["service_label"], "status": o["status"]} for o in orders}

    def order_info(self, chat_id: int, order_id: int) -> Optional[dict]:
        o = self._find_order(chat_id, order_id)
        if o is None:
            return None
        d = o["data"]
        info = {
            "id": o["id"],
            "type": o["type"],
            "service_label": o["service_label"],
            "status": o["status"],
            "price": o["price"],
            "created_at": o["created_at"],
            "has_additional_data": True,
        }
        if o["type"] == "service":
            info.update({
                "number": d.get("product"),
                "data_type": d.get("docs_type", 1),
                "priority": d.get("priority", 0),
            })
        elif o["type"] == "product":
            info.update({"number": "000000", "password": "secret", "proxy": "0.0.0.0:0000"})
        elif o["type"] in ("product_b", "product_c"):
            info.update({
                "address": d.get("address", ""),
                "full_name": d.get("full_name", ""),
                "delivery_number": d.get("phone_number", ""),
                "tg_username": d.get("telegram", ""),
                "delivery_method": d.get("delivery_type", 1),
                "track_code": "TRACK123",
                "number": d.get("product"),
            })
        return info

    def order_add_info(self, chat_id: int, order_id: int) -> Optional[dict]:
        o = self._find_order(chat_id, order_id)
        if o is None:
            return None
        if o["type"] == "service":
            return {"type": "string", "data": "Доп. данные услуги", "order_id": order_id}
        return {"type": "text", "data": "Доп. данные товара", "order_id": order_id}
