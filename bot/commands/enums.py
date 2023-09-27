from enum import Enum
from aiogram.types import BotCommand


class CommandsEnum(Enum):
    start = BotCommand(
        command='start',
        description='Начало работы')
    help = BotCommand(
        command='help',
        description='Помощь')
    bind = None
    unbind = BotCommand(
        command='unbind',
        description='Отвязка профиля')
    search_order = BotCommand(
        command='search_order',
        description='Поиск заказа (по id/кошельку)'
    )
