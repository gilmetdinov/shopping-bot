from enum import Enum


class Prompts(Enum):
    refill = f"о пополнении баланса"
    order = f"об исполнении заказов"
    serviceList = f"услуг"
    productList = f"товаров"
    product_bList = f"товаров B"
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
        3: 'Ваши текстовые данные',
        1: 'Данные A',
        2: 'Данные с условиями',
        4: 'Данные B'
    }
