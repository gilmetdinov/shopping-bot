from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
import bot.states as states
from bot.handler.processes.common import AbstractProcess
from bot.handler.services.order import IdentService
from bot.keyboards import List, Callbacks


class IdentProcess(AbstractProcess):

    def __init__(self, api, router):
        super().__init__(api, router)
        self.service = IdentService(api=self.api)

    def set(self):
        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.InputWallet.value)
        )
        async def input_wallet_number(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.input_wallet_number(callback=callback, state=state)

        @self.router.message(
            states.Order.inputWalletNumber
        )
        async def set_wallet_number(message: Message, state: FSMContext) -> None:
            await self.service.set_wallet_number(message=message, state=state)

        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.ChooseService.value)
        )
        async def choose_service(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.choose_service(callback=callback, state=state)

        for identType in List.identType.value.values():
            @self.router.message(
                states.Order.setService,
                F.text.contains(identType)
            )
            async def set_service(message: Message, state: FSMContext) -> None:
                await self.service.set_service(message=message, state=state)

        @self.router.message(
            states.Order.setService,
            F.text.in_(List.goBack.value)
        )
        async def service_go_back(message: Message, state: FSMContext) -> None:
            await self.service.service_go_back(message=message, state=state)

        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.ChooseDocs.value)
        )
        async def choose_docs(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.choose_docs(callback=callback, state=state)

        for docsType in List.docsType.value.values():
            @self.router.message(
                states.Order.setDocs,
                F.text.contains(docsType)
            )
            async def set_docs(message: Message, state: FSMContext) -> None:
                await self.service.set_docs(message=message, state=state)

        @self.router.message(
            states.Order.setDocs,
            F.text.in_(List.goBack.value)
        )
        async def docs_go_back(message: Message, state: FSMContext) -> None:
            await self.service.docs_go_back(message=message, state=state)

        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.PremiumSwitch.value)
        )
        async def switch_premium(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.switch_premium(callback=callback, state=state)

        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.UploadDocs.value)
        )
        async def upload_docs(callback: CallbackQuery, state: FSMContext) -> None:
            await self.service.upload_docs(callback=callback, state=state)

        @self.router.message(
            states.Order.uploadStringDocs
        )
        async def upload_string_docs(message: Message, state: FSMContext) -> None:
            await self.service.upload_string_docs(message=message, state=state)

        @self.router.message(
            states.Order.uploadImageDocs,
            F.text.in_(List.done.value)
        )
        async def stop_image_uploading(message: Message, state: FSMContext) -> None:
            await self.service.stop_image_uploading(message=message, state=state)

        @self.router.message(
            states.Order.uploadImageDocs,
            F.photo
        )
        async def upload_image_docs(message: Message, bot: Bot, state: FSMContext) -> None:
            await self.service.upload_image(message=message, bot=bot, state=state)

        @self.router.callback_query(
            states.Order.identForm,
            Text(Callbacks.ViewDocs.value)
        )
        async def view_docs(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
            await self.service.view_docs(callback=callback, state=state, bot=bot)

        @self.router.message(
            states.Order.viewingDocs,
            F.text.in_(List.done.value[0])
        )
        async def stop_viewing_docs(message: Message, state: FSMContext) -> None:
            await self.service.stop_viewing_docs(message=message, state=state)

