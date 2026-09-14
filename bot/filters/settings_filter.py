from aiogram.filters import BaseFilter
from aiogram.types import Message


class SettingsFilter(BaseFilter):

    def __init__(self, setting_types: list):
        self.setting_types = setting_types

    async def __call__(self, message: Message) -> bool:
        text = message.text.split(':')[0]
        return f"{text}: " in self.setting_types
