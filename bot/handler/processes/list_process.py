from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import bot.states as states
from bot import commands
from bot.keyboards import List, Callbacks
from bot.handler.processes.common import AbstractProcess
from bot.handler.handlers import ListHandler


class ListProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api=api, router=router)
        self.service = ListHandler(api=api)

    def set(self):
        @self.router.message(
            states.Common.onMainPage,
            F.text.in_(List.order.value[1])
        )
        async def list_choose_order_type(message: Message, state: FSMContext):
            await self.service.choose_order_type(message=message, state=state)

        for order_type in List.orderListType.value.values():
            @self.router.message(
                states.List.choosingType,
                F.text.in_(order_type)
            )
            async def display_order_list(message: Message, state: FSMContext) -> None:
                await self.service.display_order_list(message=message, state=state)

        @self.router.callback_query(
            states.List.viewing,
            F.data == Callbacks.GoBack.value
        )
        async def go_back_from_viewing(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.choose_order_type(message=callback.message, state=state)
            await callback.message.delete()

        @self.router.callback_query(
            states.List.viewing,
            F.data == Callbacks.FlipForward.value
        )
        async def list_next_page(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.turn_page(callback=callback, state=state)

        @self.router.callback_query(
            states.List.viewing,
            F.data == Callbacks.FlipBack.value
        )
        async def list_prev_page(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.turn_page(callback=callback, state=state, backward=True)

        @self.router.callback_query(
            states.List.viewing,
            F.data == Callbacks.Page.value
        )
        async def page_number_click(callback: CallbackQuery, state: FSMContext) -> None:
            user_data = await state.get_data()
            page = user_data['page']
            await callback.answer(self.messageBuilder.page_info(page))

        @self.router.callback_query(
            states.List.viewing
        )
        async def display_order_info(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.display_order_info(callback=callback, state=state)

        @self.router.callback_query(
            states.List.viewingOrder,
            F.data == Callbacks.ViewData.value
        )
        async def view_additional_info(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
            await self.service.view_additional_info(callback=callback, state=state, bot=bot)

        @self.router.message(
            states.List.viewingAdditionalInfo,
            F.text.in_(List.done.value)
        )
        async def stop_viewing_additional_info(message: Message, state: FSMContext) -> None:
            await self.service.return_to_order_info(message=message, state=state)

        @self.router.callback_query(
            states.List.viewingOrder,
            F.data == Callbacks.Done.value
        )
        async def stop_viewing_order(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.return_from_order_info(callback=callback, state=state)

        @self.router.message(Command(commands=[commands.List.search_order.name]))
        async def search_order(message: Message, state: FSMContext) -> None:
            await self.service.search_order(message=message, state=state)

