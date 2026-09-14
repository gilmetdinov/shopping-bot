from api import ApiClient
from aiogram.fsm.context import FSMContext


async def get_balance(api: ApiClient, chat_id):
    resp = await api.get_balance(chat_id=chat_id)
    if resp['status'] == 'success':
        return resp['balance']
    else:
        return None


async def update_balance(api: ApiClient, chat_id, state: FSMContext):
    actual_balance = await get_balance(api=api, chat_id=chat_id)
    local_data = await state.get_data()
    if actual_balance:
        await state.update_data(balance=actual_balance)
    elif 'balance' not in local_data.keys():
        await state.update_data(balance='0')
    else:
        return local_data['balance']

    new_local_data = await state.get_data()
    return new_local_data['balance']
