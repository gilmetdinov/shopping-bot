from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import bot.states as states
from bot.keyboards import List
from bot.handler.processes.common import AbstractProcess
from bot.handler.services.order import BundleService


class BundleProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = BundleService(api=self.api)

    def set(self):
        for bundleType in List.bundleType.value.values():
            @self.router.message(
                states.Order.choosingBundle,
                F.text.contains(bundleType)
            )
            async def set_bundle_type(message: Message, state: FSMContext) -> None:
                await self.service.set_service(message=message, state=state)
