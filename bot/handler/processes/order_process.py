from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
import bot.states as states
from bot.keyboards import List, Callbacks
from bot.handler.processes.common import AbstractProcess
from bot.handler.services import OrderService
from bot.handler.factories import OrderProcessFactory


class OrderProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api=api, router=router)
        self.service = OrderService(api=api)

    def set(self):
        @self.router.message(
            states.Common.onMainPage,
            F.text.in_(List.order.value[0])
        )
        async def step_one(message: Message, state: FSMContext) -> None:
            await self.service.step_one(message=message, state=state)

        for _state in self.stateHelper.choosing_order_states():
            @self.router.message(
                _state,
                F.text.contains(List.goBack.value[0])
            )
            async def go_back_to_order_type_from_reply(message: Message, state: FSMContext) -> None:
                await self.service.step_one(message=message, state=state)

        for _state in self.stateHelper.paginated_step_two_lists():
            @self.router.callback_query(
                _state,
                Text(Callbacks.GoBack.value)
            )
            async def go_back_to_order_type_from_paginated(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.step_one(message=callback.message, state=state)
                await callback.message.delete()

        for order_type in List.orderType.value.values():
            @self.router.message(
                states.Order.choosingType,
                F.text.in_(order_type)
            )
            async def step_two(message: Message, state: FSMContext) -> None:
                await self.service.step_two(message=message, state=state)

        for _state in self.stateHelper.choosing_order_states(_true=True):
            @self.router.callback_query(
                _state,
                Text(Callbacks.FlipForward.value)
            )
            async def next_page(callback: CallbackQuery, state: FSMContext) -> None:
                """Turning pages on paginated service lists where they appear"""
                await self.service.turn_page(callback=callback, state=state)

        for _state in self.stateHelper.choosing_order_states(_true=True):
            @self.router.callback_query(
                _state,
                Text(Callbacks.FlipBack.value)
            )
            async def prev_page(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.turn_page(callback=callback, state=state, backward=True)

        for _state in self.stateHelper.order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.ConfirmOrder.value)
            )
            async def confirm_order(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.send_order(callback=callback, state=state)

        for _state in self.stateHelper.order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.GoBack.value)
            )
            async def go_back_from_form(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.step_one(message=callback.message, state=state)
                await callback.message.delete()

        self.__set_base_form_parts()

    def __set_base_form_parts(self):
        """Change/set amount, address, name, phone number, telegram username"""
        for _state in self.stateHelper.discrete_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.ChangeAmount.value)
            )
            async def change_amount(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.change_amount(callback=callback, state=state)

        @self.router.message(
            states.Order.inputAmount
        )
        async def set_amount(message: Message, state: FSMContext) -> None:
            await self.service.set_amount(message=message, state=state)

        for _state in self.stateHelper.delivery_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.InputAddress.value)
            )
            async def input_address(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.input_address(callback=callback, state=state)

        @self.router.message(
            states.Order.inputAddress
        )
        async def set_address(message: Message, state: FSMContext) -> None:
            await self.service.set_address(message=message, state=state)

        for _state in self.stateHelper.delivery_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.InputFullName.value)
            )
            async def input_full_name(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.input_full_name(callback=callback, state=state)

        @self.router.message(
            states.Order.inputFullName
        )
        async def set_full_name(message: Message, state: FSMContext) -> None:
            await self.service.set_full_name(message=message, state=state)

        for _state in self.stateHelper.delivery_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.InputPhoneNumber.value)
            )
            async def input_phone_number(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.input_phone_number(callback=callback, state=state)

        @self.router.message(
            states.Order.inputPhoneNumber
        )
        async def set_phone_number(message: Message, state: FSMContext) -> None:
            await self.service.set_phone_number(message=message, state=state)

        for _state in self.stateHelper.delivery_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.InputTelegram.value)
            )
            async def input_telegram(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.input_telegram(callback=callback, state=state)

        @self.router.message(
            states.Order.inputTelegram
        )
        async def set_telegram(message: Message, state: FSMContext) -> None:
            await self.service.set_telegram(message=message, state=state)

        for _state in self.stateHelper.delivery_order_form_states():
            @self.router.callback_query(
                _state,
                Text(Callbacks.ChooseDeliveryType.value)
            )
            async def choose_delivery_type(callback: CallbackQuery, state: FSMContext) -> None:
                await self.service.choose_delivery_type(callback=callback, state=state)

        for deliveryType in List.deliveryType.value.values():
            @self.router.message(
                states.Order.choosingDeliveryType,
                F.text.in_(deliveryType)
            )
            async def set_delivery_type(message: Message, state: FSMContext) -> None:
                await self.service.set_delivery_type(message=message, state=state)

    @classmethod
    def get_subprocesses(cls) -> list:
        order_types = List.orderType.value.keys()
        subprocesses = []
        for order_type in order_types:
            process = OrderProcessFactory().get_order_process(order_type)
            if process:
                subprocesses.append(process)
        return subprocesses
