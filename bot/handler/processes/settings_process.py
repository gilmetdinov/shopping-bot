from api import ApiClient
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import bot.states as states
from bot.handler.processes.common import AbstractProcess
from bot import keyboards
from bot.handler.handlers import SettingsHandler
from bot.filters import SettingsFilter


class SettingsProcess(AbstractProcess):

    def __init__(self, api: ApiClient, router: Router):
        super().__init__(api, router)
        self.service = SettingsHandler(api=self.api)

    def set(self):
        @self.router.message(
            states.Common.onMainPage,
            F.text.in_(keyboards.List.settings.value)
        )
        async def settings_menu(message: Message, state: FSMContext) -> None:
            await self.service.settings_menu(message=message, state=state)

        @self.router.message(
            states.Settings.menu,
            SettingsFilter(list(keyboards.List.settingsMenu.value.values()))
        )
        async def switch_notif(message: Message, state: FSMContext) -> None:
            setting_type = list(keyboards.List.settingsMenu.value.keys())[
                list(keyboards.List.settingsMenu.value.values()).index(f"{message.text.split(':')[0]}: ")]
            await self.service.switch_notif(message=message, state=state, _type=setting_type)
