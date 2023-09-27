from enum import Enum


class Prompts(Enum):
    refill = f"о пополнении баланса"
    order = f"об исполнении заказов"
    identList = f"идентификаций"
    walletList = f"готовых кошельков"
    bundleList = f"комплектов"
    statuses = {
        'canceled': "🚫",
        'waiting': "⏳",
        'done': "✅",
        'error': "❗️"
    }
    statusesFull = {
        'canceled': "🚫 Отменен",
        'waiting': "⏳ В процессе",
        'done': "✅ Исполнен",
        'error': "❗️ Ошибка"
    }
    docsInfo = {
        0: 'Ваши данные',
        3: 'Ваши текст. данные',
        1: 'Наши данные',
        2: 'Данные с критериями',
        4: 'Наши текст. данные'
    }
