from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
import bot.states as states
from bot.handler.processes.common import AbstractProcess
from bot.handler.services.order import WalletService
from bot.keyboards import List, Callbacks


class WalletProcess(AbstractProcess):
    type = 'wallet'

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = WalletService(api=self.api)

    def set(self):
        @self.router.message(
            states.Order.choosingWalletCategory,
            F.text.in_(List.walletCategory.value)
        )
        async def choose_wallet(message: Message, state: FSMContext) -> None:
            await self.service.display_service_list(message=message, state=state)

        @self.router.callback_query(
            states.Order.choosingWallet,
            Text(Callbacks.GoBack.value)
        )
        async def go_back_from_wallet(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.step_two(message=callback.message, state=state)

        @self.router.callback_query(
            states.Order.choosingWallet
        )
        async def wallet_chosen(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.set_service(callback=callback, state=state)
