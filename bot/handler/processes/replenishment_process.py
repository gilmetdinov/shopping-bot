from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from api import ApiClient
import bot.states as states
from bot.keyboards import List
from bot.handler.processes.common import AbstractProcess
from bot.handler.services import ReplenishmentService


class ReplenishmentProcess(AbstractProcess):

    def __init__(self, api: ApiClient, router: Router):
        super().__init__(api, router)
        self.service = ReplenishmentService(api=api)

    def set(self):
        @self.router.message(
            states.Common.onMainPage,
            F.text.contains(List.replenish.value[0])
        )
        async def choose_replenishment_type(message: Message, state: FSMContext) -> None:
            await self.service.choose_replenishment_type(message=message, state=state)

        @self.router.message(
            states.Replenishment.choosingMethod,
            F.text.in_(List.goBack.value)
        )
        async def replenishment_cancel(message: Message, state: FSMContext) -> None:
            await self.service.replenishment_cancel(message=message, state=state)

        @self.router.message(
            states.Replenishment.choosingMethod,
            F.text.in_(List.replenishmentMethod.value)
        )
        async def replenishment_chosen(message: Message, state: FSMContext) -> None:
            await self.service.replenishment_chosen(message=message, state=state)
