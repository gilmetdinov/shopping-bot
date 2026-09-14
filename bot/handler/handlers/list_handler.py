import asyncio
import os
from enum import Enum
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from bot.handler.handlers.common import AbstractHandler
import bot.states as states
import bot.handler.utils as utils
from bot.handler.utils.order_info_factory import OrderInfoFactory
from bot.keyboards import List
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, URLInputFile, FSInputFile


class AdditionalInfoMethods(Enum):
    service = '_view_docs'  # sends media group of docs images or message with text docs
    product = '_view_product_info'  # sends txt file with product_c info and av codes
    product_b = None


class ListHandler(AbstractHandler):

    def __init__(self, api):
        super().__init__(api)
        self.orderInfoFactory = OrderInfoFactory(builder=self.messageBuilder)

    async def __throw_error_on_callback(self, callback: CallbackQuery, state: FSMContext, code: int):
        if code > 0:
            await callback.answer(self._handle_inline_error(code=code))
        else:
            await callback.message.answer(self._handle_error(code=code), parse_mode='MarkdownV2', reply_markup=None)
            await state.clear()
        return

    async def __get_order_list(self, _type: str, message: Message, state: FSMContext, page: int = 1,
                               throw_error: bool = True) -> dict | None:
        order_list_resp = await self.api.get_order_list(chat_id=message.chat.id, _type=_type, page=page)
        if not self._check_response(order_list_resp):
            if throw_error:
                code = self._get_error_code(response=order_list_resp)
                answer = self._handle_error(code=code)
                reply_markup = None if code < 0 else utils.order_list_type_keyboard()
                await message.answer(answer, reply_markup=reply_markup, parse_mode=self.MD)
                if code < 0:
                    await state.clear()
            return None
        return order_list_resp['orders'] or None

    def __form_paginated_list(self, _type, _list: dict, page: int = 1):
        answer = self.messageBuilder.get_order_list(_type=_type, _list=_list)
        inline_markup = utils.order_list_keyboard(order_list=_list, page=page)
        return answer, inline_markup

    def __get_additional_info_method(self, order_type):
        try:
            method_name = getattr(AdditionalInfoMethods, order_type).value
            method = getattr(self, method_name)
            return method
        except Exception:
            return None

    async def _view_docs(self, callback: CallbackQuery, state: FSMContext, bot: Bot, additional_info: dict):
        answer = self.messageBuilder.view_string_docs(additional_info['data']) if additional_info['type'] == 'string' \
            else self.messageBuilder.view_image_docs()
        reply_markup = utils.done_keyboard()
        additional_info_messages = [
            await callback.message.answer(answer, reply_markup=reply_markup, parse_mode=self.MD)
        ]
        if additional_info['type'] == 'image':
            media: list[InputMediaPhoto] = []
            for photo in additional_info['data']:
                media.append(InputMediaPhoto(media=photo))
            additional_info_messages += await bot.send_media_group(chat_id=callback.message.chat.id, media=media)
        await state.update_data(additional_info_messages=additional_info_messages)

    async def _view_product_info(self, callback: CallbackQuery, state: FSMContext, bot: Bot, additional_info: dict):
        data = additional_info['data']
        filename = f"product_order_{additional_info['order_id']}.txt"
        path = f"{self._get_dir(chat_id=str(callback.message.chat.id))}/{filename}"
        with open(file=path, mode='w', encoding='UTF-8') as f:
            print(data, file=f)
        file = FSInputFile(path=path, filename=filename)
        answer = self.messageBuilder.product_additional_info()
        reply_markup = utils.done_keyboard()
        additional_info_messages = [await bot.send_document(chat_id=callback.message.chat.id, document=file,
                                                            caption=answer, reply_markup=reply_markup)]
        await state.update_data(additional_info_messages=additional_info_messages)
        os.unlink(path)

    async def choose_order_type(self, message: Message, state: FSMContext):
        """Sending message to choose order list type  (service, product, product_b or product_c)"""
        await state.update_data(current_order_list_type=None)
        answer = self.messageBuilder.choose_order_type()
        reply_markup = utils.order_list_type_keyboard()
        await state.set_state(states.List.choosingType)
        choose_list_type_msg = await message.answer(answer, reply_markup=reply_markup)
        await state.update_data(choose_list_type_msg=choose_list_type_msg)

    async def display_order_list(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        choose_list_type_msg: Message = user_data['choose_list_type_msg']
        order_type_short = self.keyboardHelper.key_value_reverse(List.orderListType.value)[message.text]
        order_list = await self.__get_order_list(_type=order_type_short, message=message, state=state)
        if order_list is None:
            return

        answer, inline_markup = self.__form_paginated_list(_type=order_type_short, _list=order_list)
        await message.answer(answer, reply_markup=inline_markup, parse_mode=self.MD)
        await state.set_state(states.List.viewing)
        await state.update_data(current_order_list_type=order_type_short)
        await state.update_data(page=1)
        await choose_list_type_msg.delete()
        await message.delete()

    async def turn_page(self, callback: CallbackQuery, state: FSMContext, backward=False):
        """Turning page of paginated order lists to both sides"""
        user_data = await state.get_data()
        order_list_type = user_data['current_order_list_type']
        page = user_data['page']
        next_page = page - 1 if backward else page + 1
        new_order_list = await self.__get_order_list(_type=order_list_type, page=next_page,
                                                     message=callback.message, state=state, throw_error=False)
        if new_order_list is None:
            await callback.answer(self.messageBuilder.unavailable())
            return

        answer, inline_markup = self.__form_paginated_list(_type=order_list_type, _list=new_order_list, page=next_page)
        await state.update_data(page=next_page)
        try:
            await callback.message.edit_text(answer, reply_markup=inline_markup, parse_mode=self.MD)
        except TelegramBadRequest:
            pass

    async def display_order_info(self, callback: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        order_list_type = user_data['current_order_list_type']
        order_id = int(callback.data)
        order_info_resp = await self.api.get_order_info(chat_id=callback.message.chat.id, _type=order_list_type,
                                                        order_id=order_id)
        if not self._check_response(response=order_info_resp):
            code = self._get_error_code(response=order_info_resp)
            await self.__throw_error_on_callback(callback=callback, state=state, code=code)
            return

        order_info = order_info_resp['order_info']
        answer = self.orderInfoFactory.get_order_info_message(_type=order_list_type, order_info=order_info)
        inline_markup = utils.order_info_keyboard(order_info['has_additional_data'] or False)
        await callback.message.answer(answer, reply_markup=inline_markup, parse_mode=self.MD)
        await state.update_data(current_order_id=order_id)
        await state.update_data(preview_state=(await state.get_state()))
        await state.set_state(states.List.viewingOrder)

    async def view_additional_info(self, callback: CallbackQuery, state: FSMContext, bot: Bot):
        user_data = await state.get_data()
        order_list_type = user_data['current_order_list_type']
        order_id = user_data['current_order_id']
        method = self.__get_additional_info_method(order_type=order_list_type)
        if method is None:
            await callback.answer(self._handle_error(code=self.errorCodes.InlineError.value))
            return

        add_info_resp = await self.api.get_order_add_info(chat_id=callback.message.chat.id, _type=order_list_type,
                                                          order_id=order_id)
        if not self._check_response(response=add_info_resp):
            code = self._get_error_code(response=add_info_resp)
            await self.__throw_error_on_callback(callback=callback, state=state, code=code)
            return

        additional_info = add_info_resp['info']
        await method(callback=callback, state=state, bot=bot, additional_info=additional_info)
        await state.set_state(states.List.viewingAdditionalInfo)

    async def search_order(self, message: Message, state: FSMContext):
        exploded_message = message.text.strip().split()
        if len(exploded_message) != 2:
            incorrect_command_msg = await message.answer(self.messageBuilder.incorrect_command(is_bind=False),
                                                         parse_mode=self.MD)
            await asyncio.sleep(5)
            await incorrect_command_msg.delete()
            await message.delete()
            return

        params = exploded_message[1]
        search_order_resp = await self.api.search_order(chat_id=message.chat.id, params=params)
        if not self._check_response(response=search_order_resp):
            code = self._get_error_code(response=search_order_resp)
            if code > 0:
                await message.answer(self.messageBuilder.error_message(code=code, remove_entities=True),
                                     parse_mode=self.MD)
            else:
                await message.answer(self.messageBuilder.error_message(code=code, remove_entities=True),
                                     parse_mode=self.MD, reply_markup=None)
                await state.clear()
            return

        order_type = search_order_resp['order_type']
        order_info = search_order_resp['order_info']
        answer = self.orderInfoFactory.get_order_info_message(_type=order_type, order_info=order_info)
        inline_markup = utils.order_info_keyboard(order_info['has_additional_data'] or False)
        await message.answer(answer, reply_markup=inline_markup, parse_mode=self.MD)
        await state.update_data(current_order_id=order_info['id'])
        await state.update_data(current_order_list_type=order_type)
        await state.update_data(preview_state=(await state.get_state()))
        await state.update_data(command_msg=message)
        await state.set_state(states.List.viewingOrder)

    @classmethod
    async def return_to_order_info(cls, message: Message, state: FSMContext):
        user_data = await state.get_data()
        additional_info_messages = user_data['additional_info_messages']
        for _message in additional_info_messages:
            await _message.delete()
        await state.update_data(additional_info_messages=None)
        await state.set_state(states.List.viewingOrder)
        await message.delete()

    @classmethod
    async def return_from_order_info(cls, callback: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        preview_state = user_data['preview_state'] if 'preview_state' in user_data.keys() else states.List.viewing
        await state.update_data(current_order_id=None)
        await state.update_data(preview_state=None)
        await state.set_state(preview_state)
        await callback.message.delete()
        '''if 'command_msg' in user_data.keys() and user_data['command_msg'] is not None:
            await user_data['command_msg'].delete()
            await state.update_data(command_msg=None)'''
