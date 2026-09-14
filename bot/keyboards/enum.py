from enum import Enum
from utils.enums import DeliveryType


class KeyboardEnum(Enum):
    order = ['🛒 Оформить заказ', '📚 Мои заказы']
    orderType = {
        'service': '🧩 Услуга',
        'product': '📦 Товар A',
        'product_b': '🎁 Товар B',
        'product_c': '🧾 Товар C'
    }
    orderListType = {
        'service': '🧩 Услуги',
        'product': '📦 Товары A',
        'product_b': '🎁 Товары B'
    }
    productCategory = ['Все', '🔹 Категория A', '🔸 Категория B']
    replenish = ['➕ Пополнить баланс ']
    replenishmentMethod = ['Способ A', 'Способ B', 'Способ C', 'Способ D', 'Способ E']
    settings = ['⚙️ Настройки']
    settingsMenu = {
        'refill': 'Уведомления о пополнении баланса: ',
        'order': 'Уведомления о выполненных заказах: '
    }
    toMain = ['🏠 На главную']
    goBack = ['↩️ Назад']
    goBackDict = {'go-back': '↩️ Назад'}
    done = ['🆗 Готово']
    viewData = ['ℹ️ Посмотреть данные']
    confirmation = ['✅ Да', '❌ Нет']
    pagination = {'flip-back': '⬅️', 'page': '', 'flip-forward': '➡️'}
    deliveryType = {
        DeliveryType.PickUpPoint.value: 'Пункт выдачи',
        DeliveryType.DirectDelivery.value: 'Доставка'
    }
    docsType = {
        1: 'Тип данных A',
        4: 'Тип данных B',
        0: 'Ваши данные',
        3: 'Ваши текстовые данные'
    }
