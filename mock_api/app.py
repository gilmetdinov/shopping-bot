"""Mock store API — FastAPI app emulating the store backend.

Endpoints mirror `config/routes/api.py`. The bot talks to this mock the same way
it talks to the real store: POST with a JSON body containing `chat_id` (and an
optional `sign` field the mock ignores).

Run:
    python -m mock_api            # or: uvicorn mock_api.app:app --port 8844
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI, Request

from mock_api.store import Store

store = Store()
app = FastAPI(title="Mock Store API")


def _ok(**kwargs) -> dict:
    return {"status": "success", **kwargs}


def _err(code: int = -1) -> dict:
    return {"status": "error", "code": code}


def _chat_id(body: Optional[dict]) -> Optional[int]:
    if not body:
        return None
    chat_id = body.get("chat_id")
    try:
        return int(chat_id) if chat_id is not None else None
    except (TypeError, ValueError):
        return None


async def _body(request: Request) -> dict:
    try:
        return await request.json() or {}
    except Exception:
        return {}


@app.get("/api/telegram/")
async def ping():
    return _ok(message="pong")


@app.post("/api/telegram/test")
async def test(request: Request):
    return _ok(message="test ok")


@app.post("/api/telegram/bind")
async def bind(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return store.bind(chat_id, key=body.get("key", ""), username=body.get("username", ""))


@app.post("/api/telegram/check-user")
async def check_user(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return _ok(is_bound=store.is_bound(chat_id))


@app.post("/api/telegram/get-unbind-code")
async def get_unbind_code(request: Request):
    return _ok(code="123456")


@app.post("/api/telegram/unbind")
async def unbind(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return store.unbind(chat_id)


@app.post("/api/telegram/get-payment-address")
async def get_payment_address(request: Request):
    body = await _body(request)
    return _ok(payment_address="mock-address-0001",
               currency=body.get("currency", "BTC"),
               course=100.0)


@app.post("/api/telegram/get-balance")
async def get_balance(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return _ok(balance=store.balance(chat_id))


@app.post("/api/telegram/get-notif-settings")
async def get_notif_settings(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    settings = store.notif_settings.setdefault(chat_id, {"refill": True, "order": True})
    return _ok(refill_notif=settings.get("refill", True), order_notif=settings.get("order", True))


@app.post("/api/telegram/switch-notif")
async def switch_notif(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    settings = store.notif_settings.setdefault(chat_id, {"refill": True, "order": True})
    _type = body.get("type")
    if _type in settings:
        settings[_type] = not settings[_type]
    return _ok(new_setting=settings.get(_type, False))


@app.post("/api/telegram/get-service-list")
async def get_service_list(request: Request):
    body = await _body(request)
    return _ok(list=store.service_list(body.get("type", "product")))


@app.post("/api/telegram/get-order-cache")
async def get_order_cache(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return _ok(order_cache=store.get_order_cache(chat_id))


@app.post("/api/telegram/update-order-cache")
async def update_order_cache(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return store.update_order_cache(chat_id, body.get("order_data", {}))


@app.post("/api/telegram/delete-images")
async def delete_images(request: Request):
    return _ok(deleted=True)


@app.post("/api/telegram/upload-image")
async def upload_image(request: Request):
    return _ok(uploaded=True, data={"img_one": {"url": "", "path": "", "name": ""}})


@app.post("/api/telegram/make-order")
async def make_order(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return store.make_order(chat_id, body.get("order_data", {}))


@app.post("/api/telegram/get-order-list")
async def get_order_list(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    return _ok(orders=store.order_list(chat_id, body.get("type")))


@app.post("/api/telegram/get-order-info")
async def get_order_info(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    info = store.order_info(chat_id, int(body.get("order_id", 0))) if chat_id is not None else None
    print(f"[mock] get-order-info chat_id={chat_id} order_id={body.get('order_id')} -> {info}")
    if info is None:
        return _err(-1)
    return _ok(order_info=info)


@app.post("/api/telegram/get-order-additional-info")
async def get_order_additional_info(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    info = store.order_add_info(chat_id, int(body.get("order_id", 0))) if chat_id is not None else None
    if info is None:
        return _err(-1)
    return _ok(info=info)


@app.post("/api/telegram/search-order")
async def search_order(request: Request):
    body = await _body(request)
    chat_id = _chat_id(body)
    if chat_id is None:
        return _err(-1)
    try:
        order_id = int(body.get("params", ""))
    except (TypeError, ValueError):
        return _err(-1)
    info = store.order_info(chat_id, order_id)
    if info is None:
        return _ok(order_type="", order_info=None)
    return _ok(order_type=info["type"], order_info=info)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8844)
