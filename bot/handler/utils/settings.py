from api import ApiClient
from aiogram.fsm.context import FSMContext


async def get_settings(api: ApiClient, chat_id):
    resp = await api.get_notif_settings(chat_id=chat_id)
    if resp['status'] == 'success':
        return resp['refill_notif'], resp['order_notif']
    else:
        return -1, -1


async def update_settings(api: ApiClient, chat_id, state: FSMContext):
    actual_settings = await get_settings(api=api, chat_id=chat_id)
    local_data = await state.get_data()
    if actual_settings != (-1, -1):
        await state.update_data(refill_notif=actual_settings[0], order_notif=actual_settings[1])
    elif 'refill_notif' not in local_data.keys() or 'order_notif' not in local_data.keys():
        if 'refill_notif' not in local_data.keys():
            await state.update_data(refill_notif=0)
        elif 'order_notif' not in local_data.keys():
            await state.update_data(order_notif=0)
    else:
        return local_data['refill_notif'], local_data['order_notif']

    new_local_data = await state.get_data()
    return new_local_data['refill_notif'], new_local_data['order_notif']

