import os
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from bot.keyboards import List
from bot.handler.services.order.common import AbstractOrderService
import bot.states as states
import bot.handler.utils as utils
from bot.handler.dto import IdentDto


class IdentService(AbstractOrderService):

    def __init__(self, api):
        super().__init__(api, _type='ident')

    def __get_docs_shortname(self, order: str) -> str:
        """Getting shortname from reply markup selected button"""
        value = order.split('(')[0].rstrip()
        service_list = self.keyboardHelper.key_value_reverse(List.docsType.value)
        return service_list[value]

    async def __get_docs_keyboard(self, chat_id):
        """Getting reply markup with docs types for ident"""
        docs_list_resp = await self.api.get_service_list(_type='docs', chat_id=chat_id)
        docs_list = []
        if self._check_response(response=docs_list_resp):
            docs_list = docs_list_resp['list']
        return utils.docs_type_keyboard(docs_list)

    async def __update_ident_form(self, form: CallbackQuery, dto: IdentDto, state: FSMContext):
        """Updating ident order cache after changing ident form"""
        update_order_resp = await self.api.update_verif_order_cache(chat_id=form.message.chat.id,
                                                                    order_data=dto.order_data())
        if self._check_response(response=update_order_resp):
            await self._update_form(form=form, dto=dto)
        else:
            answer = self._handle_response_error(response=update_order_resp)
            await form.message.answer(answer, parse_mode='MarkdownV2', reply_markup=None)
            await form.message.delete()
            await state.clear()  # очищаем state, потому как системная ошибка

    async def step_two(self, message, state):
        """Getting order cache from server and proceeding to order form with it"""
        user_data = await state.get_data()
        choose_order_msg: Message = user_data['choose_order_msg']

        get_order_cache_resp = await self.api.get_verif_order_cache(chat_id=message.chat.id)
        inline_markup = None

        if self._check_response(response=get_order_cache_resp):
            order_cache = get_order_cache_resp['order_cache']
            dto = IdentDto(order_cache=order_cache)
            await state.update_data(order_dto=dto)
            await state.set_state(self._form_state())
            answer, inline_markup = self._get_form(dto=dto, username=message.chat.username)
        else:
            answer = self._handle_response_error(response=get_order_cache_resp)
            await state.clear()  # очищаем state, потому что системная ошибка

        await message.answer(answer, parse_mode='MarkdownV2', reply_markup=inline_markup)
        await message.delete()
        await choose_order_msg.delete()

    async def input_wallet_number(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(order_form=callback)
        await state.set_state(states.Order.inputWalletNumber)
        answer = self.messageBuilder.input_wallet_number()
        await callback.answer(answer, show_alert=True)

    async def set_wallet_number(self, message: Message, state: FSMContext):
        wallet_number = message.text.strip()
        user_data = await state.get_data()

        dto: IdentDto = user_data['order_dto']
        dto.set_wallet(wallet_number=wallet_number)
        await state.update_data(order_dto=dto)
        await state.set_state(states.Order.identForm)

        form: CallbackQuery = user_data['order_form']
        await self.__update_ident_form(form=form, dto=dto, state=state)
        await message.delete()

    async def choose_service(self, callback: CallbackQuery, state: FSMContext):
        """Displaying reply markup of available services for ident: service_name (price р.)"""
        await state.update_data(order_form=callback)
        service_list = await self._get_service_list(message=callback.message, state=state, force_update=True)
        answer = self.messageBuilder.choose_service()
        reply_markup = utils.service_reply_keyboard(_type=self.type, service_list=service_list)
        await state.set_state(states.Order.setService)
        answer_msg = await callback.message.answer(answer, reply_markup=reply_markup, parse_mode=self.MD)
        await state.update_data(service_msg=answer_msg)

    async def set_service(self, message: Message, state: FSMContext):
        """Setting service with splitting chosen reply markup button on service shortname and price"""
        user_data = await state.get_data()
        service_list: list = await self._get_service_list(message=message, state=state, user_data=user_data)

        message_text = message.text.strip()
        chosen_service: dict or None = next(
            (service for service in service_list if service['full_label'] == message_text),
            None
        )
        if chosen_service is None:
            answer = self.messageBuilder.incorrect_service()
            reply_markup = utils.service_reply_keyboard(_type=self.type, service_list=service_list)
            await message.answer(answer, reply_markup=reply_markup, parse_mode=self.MD)
            return

        service_short, service_label, service_price = (chosen_service['short'],
                                                       chosen_service['label'],
                                                       float(chosen_service['price']))
        dto: IdentDto = user_data['order_dto']
        dto.set_service(service=service_short, service_label=service_label, price=service_price)
        await state.update_data(order_dto=dto)
        await state.set_state(self._form_state())

        form: CallbackQuery = user_data['order_form']
        service_msg: Message = user_data['service_msg']
        await self.__update_ident_form(form=form, dto=dto, state=state)
        await service_msg.delete()
        await message.delete()

    async def service_go_back(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        service_msg: Message = user_data['service_msg']
        await state.set_state(self._form_state())
        await service_msg.delete()
        await message.delete()

    async def switch_premium(self, callback: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        dto: IdentDto = user_data['order_dto']
        dto.switch_premium(price=dto.premium_price)
        await state.update_data(order_dto=dto)
        await state.update_data(order_form=callback)
        answer = self.messageBuilder.premium_switched(status=dto.premium)
        await callback.answer(answer, show_alert=True)
        await self.__update_ident_form(form=callback, dto=dto, state=state)

    async def choose_docs(self, callback: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        dto: IdentDto = user_data['order_dto']
        await state.update_data(order_form=callback)
        answer = self.messageBuilder.choose_docs(service=dto.service)
        reply_markup = await self.__get_docs_keyboard(chat_id=callback.message.chat.id)
        await state.set_state(states.Order.setDocs)
        answer_msg = await callback.message.answer(answer, reply_markup=reply_markup)
        await state.update_data(docs_msg=answer_msg)

    async def set_docs(self, message: Message, state: FSMContext):
        order = message.text.strip()
        docs_type = self.__get_docs_shortname(order=order)
        price = self._get_price(order=order) if docs_type in (1, 4) else 0
        user_data = await state.get_data()
        dto: IdentDto = user_data['order_dto']
        dto.set_docs_type(docs_type=docs_type, price=price)
        await state.update_data(order_dto=dto)
        await state.set_state(self._form_state())
        form: CallbackQuery = user_data['order_form']
        docs_msg: Message = user_data['docs_msg']
        await self.__update_ident_form(form=form, dto=dto, state=state)
        await message.delete()
        await docs_msg.delete()

    async def docs_go_back(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        docs_msg: Message = user_data['docs_msg']
        await state.set_state(self._form_state())
        await message.delete()
        await docs_msg.delete()

    async def __images_deleted(self, order_cache_id, chat_id, dto: IdentDto):
        resp = await self.api.delete_images(order_cache_id=order_cache_id, chat_id=chat_id)
        return self._check_response(response=resp) and dto.delete_images()

    async def upload_docs(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(order_form=callback)
        user_data = await state.get_data()
        dto: IdentDto = user_data['order_dto']
        reply_markup = None
        if dto.docs_type == 0 and await self.__images_deleted(order_cache_id=dto.order_cache_id,
                                                              chat_id=callback.message.chat.id,
                                                              dto=dto):
            answer = self.messageBuilder.upload_image_docs()
            reply_markup = utils.done_keyboard()
            await state.set_state(states.Order.uploadImageDocs)
            await state.update_data(images_count=0)
            await state.update_data(uploaded_images=[])
            await state.update_data(order_dto=dto)
        elif dto.docs_type == 3:
            answer = self.messageBuilder.upload_string_docs()
            await state.set_state(states.Order.uploadStringDocs)
        else:
            answer = self._handle_error(code=self.errorCodes.InlineError.value)
            await state.clear()

        upload_rules_msg = await callback.message.answer(answer, reply_markup=reply_markup)
        await state.update_data(upload_rules_msg=upload_rules_msg)

    async def upload_string_docs(self, message: Message, state: FSMContext):
        data = message.text.strip()
        user_data = await state.get_data()

        dto: IdentDto = user_data['order_dto']
        dto.set_docs_string(data=data)
        await state.update_data(order_dto=dto)
        await state.set_state(self._form_state())

        form: CallbackQuery = user_data['order_form']
        await self.__update_ident_form(form=form, dto=dto, state=state)
        upload_rules_msg: Message = user_data['upload_rules_msg']
        await upload_rules_msg.delete()
        await message.delete()

    async def __after_image_upload(self, form: CallbackQuery, dto: IdentDto, state: FSMContext):
        user_data = await state.get_data()
        uploaded_images: list[Message] = user_data['uploaded_images']
        for image in uploaded_images:
            await image.delete()
        upload_rules_msg: Message = user_data['upload_rules_msg']
        await upload_rules_msg.delete()
        await self._update_form(form=form, dto=dto)

    async def upload_image(self, message: Message, bot: Bot, state: FSMContext):
        user_data = await state.get_data()
        images_count = user_data['images_count']
        dto: IdentDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']
        uploaded_images: list = user_data['uploaded_images']
        uploaded_images.append(message)
        await state.update_data(uploaded_images=uploaded_images)

        if images_count < 3:
            alias = list(dto.docs_images.keys())[images_count]
            filename = f"{dto.order_cache_id}-{alias}.jpg"
            _dir = self._get_dir(chat_id=str(message.chat.id))
            path = f"{_dir}/{filename}"
            image = message.photo.pop()
            await bot.download(image, destination=path)
            # await message.answer(f"saved image to {path}")  # debug
            resp = await self.api.upload_image(chat_id=str(message.chat.id),
                                               order_cache_id=str(dto.order_cache_id),
                                               img_path=path)
            if self._check_response(response=resp):
                dto.load_images(resp['data'])
                images_count += 1
                await state.update_data(images_count=images_count)
                await state.update_data(order_dto=dto)
            else:
                answer = self._handle_error(code=self._get_error_code(response=resp))
                await message.answer(answer)
                await form.message.delete()
                await state.set_state(self._form_state())
            os.unlink(path=path)

        if images_count >= 3:
            await state.set_state(self._form_state())
            await self.__after_image_upload(form=form, dto=dto, state=state)

    async def stop_image_uploading(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        await state.set_state(self._form_state())
        dto: IdentDto = user_data['order_dto']
        form: CallbackQuery = user_data['order_form']
        await self.__after_image_upload(form=form, dto=dto, state=state)
        await message.delete()

    async def view_docs(self, callback: CallbackQuery, state: FSMContext, bot: Bot):
        user_data = await state.get_data()
        dto: IdentDto = user_data['order_dto']
        docs = dto.docs_data()
        docs_messages = None
        reply_markup = utils.done_keyboard()
        if docs and 'string' in docs.keys():
            answer = self.messageBuilder.view_string_docs(data=docs['string'])
            docs_messages = [await callback.message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)]
        elif docs and len(docs) >= 1:
            answer = self.messageBuilder.view_image_docs()
            docs_messages = [await callback.message.answer(answer, parse_mode='MarkdownV2', reply_markup=reply_markup)]
            media: list[InputMediaPhoto] = []
            for photo in docs.values():
                media.append(InputMediaPhoto(media=photo))
            docs_messages += await bot.send_media_group(chat_id=callback.message.chat.id, media=media)

        if docs_messages:
            await state.update_data(docs_messages=docs_messages)
            await state.set_state(states.Order.viewingDocs)

    async def stop_viewing_docs(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        docs_messages: list[Message] = user_data['docs_messages']
        for doc in docs_messages:
            await doc.delete()
        await message.delete()
        await state.set_state(self._form_state())
