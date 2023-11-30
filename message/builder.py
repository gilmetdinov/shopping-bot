import os
from dotenv import load_dotenv
from utils.markdown import *
from utils.date import DateHelper
from utils.enums import OrderStatus, ErrorCodes
from bot.keyboards import List
import message.errors as errors
from bot.handler.dto import *
from message.enum import Prompts

load_dotenv()


class MessageBuilder:

    def __init__(self):
        # ссылки на нас
        self.tgChannel1 = os.getenv('TG_CHANNEL_1')
        self.tgChannel2 = os.getenv('TG_CHANNEL_2')
        self.channelList = [
            self.tgChannel1,
            self.tgChannel2
        ]
        self.supportTg = os.getenv('SUPPORT_TG')
        self.projectName = os.getenv('PROJECT_NAME')
        self.siteUrl = os.getenv('SITE_URL')
        self.settingsUrl = os.getenv('SETTINGS_URL')
        self.refillHistoryUrl = os.getenv('REFILL_HISTORY_URL')
        self.ordersUrl = os.getenv('ORDERS_URL')

        self.remove_entities = remove_markdown_entities
        self.hide_link = hide_link
        self.errorHandler = errors.Builder(support_tg=self.supportTg, settings_url=self.settingsUrl)
        self.tsConverter = DateHelper
        self.orderStatus = OrderStatus

        # обработанные ссылки (тг + название проекта)
        self.redactedChannelList = self.__get_redacted_channel_list()
        self.redactedSupportTg = self.__get_redacted_support_tg()
        self.redactedProjectName = self.__get_redacted_project_name()

    def __get_redacted(self, text):
        return self.remove_entities(text)

    def __get_redacted_channel_list(self):
        redacted_channel_list = []
        for channel in self.channelList:
            redacted_channel_list.append(self.remove_entities(channel))
        return redacted_channel_list

    def __get_redacted_support_tg(self):
        return self.remove_entities(self.supportTg)

    def __get_redacted_project_name(self):
        return self.remove_entities(self.projectName)

    def __build(self, body, remove_entities=False):
        if remove_entities:
            return self.__get_redacted(text=body)
        return body

    def subscribe(self):
        channel_prompts = ""
        for channel in self.channelList:
            channel_prompts += f"\n✨ {channel}  ✨"
        body = f"Будем рады видеть Вас в наших телеграм каналах:{channel_prompts}"
        return self.__build(body=body, remove_entities=True)

    def start_bound(self):
        text_to_redact = f"Ваш профиль привязан к телеграм аккаунту.\n" \
                         f"Настройки уведомлений доступны в "
        redacted_text = self.__get_redacted(text=text_to_redact)
        hyperlink = f"[личном кабинете]({self.settingsUrl})\."
        body = redacted_text + hyperlink + "\n\n" + self.subscribe()
        return self.__build(body=body)

    def start_unbound(self):
        text_to_redact = f"Добро пожаловать!\n" \
                         f"Для привязки профиля к телеграм аккаунту, " \
                         f"пожалуйста, воспользуйтесь нашей "
        redacted_text = self.__get_redacted(text=text_to_redact)
        hyperlink = f"[инструкцией]({self.settingsUrl})\."
        support = f"Чат поддержки \(настоятельно рекомендуем переходить в чат поддержки только по ссылкам\):\n" \
                  f"{self.redactedSupportTg}\n"
        site_link = f"\nНаш сайт: {self.redactedProjectName}"
        body = redacted_text + hyperlink + "\n\n" + support + self.subscribe() + site_link
        return self.__build(body=body)

    def help_bound(self):
        body = f"Вас приветствует клиентский бот проекта [{self.redactedProjectName}]({self.siteUrl})\n" \
               f"Бот может отправлять уведомления:\n" \
               f"\- о пополнении баланса\n" \
               f"\- о выполнении заказов\n" \
               f"Настройки уведомлений доступны в Вашем [личном кабинете]({self.settingsUrl})\.\n\n" \
               f"Наши телеграм каналы:\n" \
               f"{self.redactedChannelList[0]}\n" \
               f"{self.redactedChannelList[1]}\n" \
               f"Чат поддержки \(настоятельно рекомендуем переходить в чат поддержки только по ссылкам\):\n" \
               f"{self.redactedSupportTg}" \
               f"\n\n" \
               f"*Заказы производятся исключительно через сайт или бота во избежание фишинга\!*"
        return self.__build(body=body)

    def help_unbound(self):
        body = f"Аккаунт не привязан."
        return self.__build(body=body, remove_entities=True)

    def bind_success(self):
        body = f"Вы успешно привязали ваш профиль!"
        return self.__build(body=body, remove_entities=True)

    def error_message(self, code, remove_entities: bool | None = None):
        body, _remove_entities = self.errorHandler.get_message_by_code(code=code)
        return self.__build(body=body,
                            remove_entities=remove_entities if remove_entities is not None else _remove_entities)

    def incorrect_command(self, is_bind=True, remove_entities: bool | None = None):
        body, _remove_entities = self.errorHandler.get_incorrect_command_message(is_bind=is_bind)
        return self.__build(body=body,
                            remove_entities=remove_entities if remove_entities is not None else _remove_entities)

    def incorrect_input(self, remove_entities: bool | None = None):
        body, _remove_entities = self.errorHandler.get_incorrect_input_message()
        return self.__build(body=body,
                            remove_entities=remove_entities if remove_entities is not None else _remove_entities)

    def incorrect_service(self, remove_entities: bool | None = None):
        body, _remove_entities = self.errorHandler.get_incorrect_service_message()
        return self.__build(body=body,
                            remove_entities=remove_entities if remove_entities is not None else _remove_entities)

    def __replenishment(self, amount, currency, time):
        """Replenishment notification message"""
        header = self.__get_redacted("[ПОПОЛНЕНИЕ✅]")
        hyperlink = f"[баланс]({self.refillHistoryUrl})"
        text_to_redact = f"успешно зачислено: {amount} ₽\n" \
                         f"Платеж был произведен через валюту {currency} " \
                         f"и обработан в {self.tsConverter(timestamp=time).get_date()}\n\n" \
                         f"Наш телеграм канал: {self.channelList[0]}\n" \
                         f"Поддержка: {self.supportTg}"
        redacted_text = self.__get_redacted(text=text_to_redact)
        body = f"{header}\nНа Ваш {hyperlink} {redacted_text}"
        return self.__build(body=body)

    def __order_update(self, order_id, status):
        """Order notification message (success/error)"""
        hyperlink = f"[К списку заказов]({self.ordersUrl})"
        if status == self.orderStatus.error.value:
            header = self.__get_redacted("[ЗАКАЗ⚠️]")
            text_to_redact = f"Во время выполнения заказа № {order_id} возникла ошибка!\n" \
                             f"Пожалуйста, свяжитесь с администрацией:\n" \
                             f"{self.supportTg}"
        elif status == self.orderStatus.complete.value:
            header = self.__get_redacted("[ЗАКАЗ✅]")
            text_to_redact = f"Заказ № {order_id} выполнен успешно!"
        else:
            return None

        redacted_text = self.__get_redacted(text=text_to_redact)
        body = f"{header}\n{redacted_text}\n\n{hyperlink}"
        return self.__build(body=body)

    def notification(self, notif_type, contents):

        if notif_type == 'replenishment':
            return self.__replenishment(
                amount=contents['amount'],
                currency=contents['currency'],
                time=int(contents['time'])
            )

        elif notif_type == 'order':
            return self.__order_update(
                order_id=contents['id'],
                status=int(contents['status'])
            )

        return None

    def unbind_confirmation(self):
        body = f"Вы уверены, что хотите отвязать Ваш профиль от данного телеграм аккаунта?"
        return self.__build(body=body, remove_entities=True)

    def unbind_cancel(self):
        hyperlink = f"[личном кабинете]({self.settingsUrl})\."
        text_to_redact = f"Отвязка профиля отменена.\n" \
                         f"Настройки уведомлений доступны в Вашем"
        redacted_text = self.__get_redacted(text=text_to_redact)
        body = f"{redacted_text} {hyperlink}"
        return self.__build(body=body)

    def unbind_instruction(self):
        hyperlink = f"[личном кабинете]({self.settingsUrl})\."
        text_to_redact = f"Для отвязки профиля, пожалуйста, введите код подтверждения.\n" \
                         f"Получить его Вы можете в Вашем"
        redacted_text = self.__get_redacted(text=text_to_redact)
        sup_text = f"В случае, если код не появился, пожалуйста, обратитесь в нашу поддержку:\n" \
                   f"{self.supportTg}"
        redacted_sup_text = self.__get_redacted(text=sup_text)
        body = f"{redacted_text} {hyperlink}\n\n{redacted_sup_text}"
        return self.__build(body=body)

    def unbind_success(self):
        hyperlink = f"[личном кабинете]({self.settingsUrl})\."
        text_to_redact = f"Вы успешно отвязали ваш профиль!\n" \
                         f"Вам доступна повторная привязка. Произвести ее Вы можете по инструкции, доступной в Вашем"
        redacted_text = self.__get_redacted(text=text_to_redact)
        body = f"{redacted_text} {hyperlink}\n\n{self.subscribe()}"
        return self.__build(body=body)

    def choose_replenishment_method(self):
        body = f"Пожалуйста, выберите способ оплаты."
        return self.__build(body=body)

    def replenishment_canceled(self):
        body = f"Пополнение баланса отменено."
        return self.__build(body=body)

    def replenish_message(self, wallet, currency, course):
        copiable_wallet = f"`{wallet}`"
        text_to_redact = f"Валюта: {currency}\n" \
                         f"Курс на текущий момент: 1 {currency} = {course} ₽\n\n" \
                         f"Если у Вас возникли вопросы, пожалуйста, обратитесь в нашу поддержку:\n" \
                         f"{self.supportTg}"
        redacted_text = self.__get_redacted(text=text_to_redact)
        body = f"Ваш кошелек для оплаты: {copiable_wallet}\n{redacted_text}"
        return self.__build(body=body)

    def settings_message(self):
        hyperlink = f"[личном кабинете]({self.settingsUrl})\."
        text_to_redact = f"Доступные настройки:\n" \
                         f"- уведомления о пополнении баланса;\n" \
                         f"- уведомления об исполнении заказов;\n\n" \
                         f"Полный список настроек доступен в Вашем "
        redacted_text = self.__get_redacted(text=text_to_redact)
        body = redacted_text + hyperlink
        return self.__build(body=body)

    def notif_set_message(self, _type, setting):
        try:
            type_text = getattr(Prompts, _type).value
        except Exception:
            return self.__build(body=f"Неизвестный тип уведомлений!", remove_entities=True)

        setting_text = f"включены" if setting else f"выключены"

        body = f"Уведомления {type_text} успешно {setting_text}!"
        return self.__build(body=body, remove_entities=True)

    def go_to_main_message(self):
        body = f"Возврат на главную страницу..."
        return self.__build(body=body)

    def unavailable(self):
        body = f"Недоступно"
        return self.__build(body=body)

    def not_enough_funds(self):
        body = f"Недостаточно средств для заказа!"
        return self.__build(body=body)

    def choose_order_type(self):
        body = f"Пожалуйста, выберете тип заказа."
        return self.__build(body=body)

    def choose_wallet_category(self):
        body = f"Пожалуйста, выберете тип кошелька."
        return self.__build(body=body, remove_entities=True)

    def choose_service(self, is_alert: bool = False):
        body = f"Пожалуйста, выберете сервис."
        return self.__build(body=body, remove_entities=not is_alert)

    def wallet_alert(self):
        bold_text = f"*\!\!\! ВНИМАНИЕ \!\!\!*"
        warning = f"С целью безопасности Ваших кошельков, настоятельно рекомендуем после покупки:\n" \
                  f"\- Сменить пароль на кошельке;\n" \
                  f"\- Привязать почту к вашему кошельку;"
        body = f"{bold_text}\n{warning}"
        return self.__build(body=body)

    def choose_bundle(self):
        requirements = f"Обратите внимание, что для совершения заказа Вам потребуется:\n" \
                       f"- Адрес доставки (ПВЗ СДЭК/курьером);\n" \
                       f"- ФИО получателя;\n" \
                       f"- Номер телефона получателя;\n" \
                       f"- Телеграм для связи;"
        text_to_redact = (f"Пожалуйста, выберете тип комплекта.\nДоставка комплекта доступна при покупке от 3 штук.\n"
                          + requirements)
        body = self.__get_redacted(text=text_to_redact)
        return self.__build(body=body)

    def service_pagination_list(self, _type, service_list, page=1):
        body = f""
        for i in range(len(service_list[10 * (page - 1):10 * page])):
            service_name = self.__get_redacted(service_list[i + 10 * (page - 1)]['label'])
            price = self.__get_redacted(service_list[i + 10 * (page - 1)]['price'])
            body += f"*{i + 1}*\. {service_name} \- {price} р\.\n"
        return self.__build(body=body)

    def get_ident_form(self, dto: IdentDto):
        service = f"*Сервис:* {self.__get_redacted(dto.service_label)}"
        wallet_number = f"*Номер кошелька:* {dto.wallet or ''}"
        docs_type = f"*Тип данных для идентификации:* {self.__get_redacted(List.docsType.value[dto.docs_type])}"
        total_price = f"*К оплате:* {self.__get_redacted(str(dto.price))} р\."
        body = f"Заказ идентификации:\n{service}\n{wallet_number}\n{docs_type}\n{total_price}"
        return self.__build(body=body)

    def get_wallet_form(self, dto: WalletDto):
        service = f"*Сервис:* {self.__get_redacted(dto.service_label)}"
        amount = f"*Количество:* {dto.amount}"
        total_price = f"*К оплате:* {self.__get_redacted(str(dto.total_price))} р\."
        body = f"Заказ готового кошелька:\n{service}\n{amount}\n{total_price}"
        return self.__build(body=body)

    def get_delivery_form(self, dto: DeliveryDto, username):
        service = f"*Сервис:* {self.__get_redacted(dto.service_label)}"
        amount = f"*Количество:* {dto.amount}"
        address = f"*Адрес доставки:* {self.__get_redacted(dto.address or '')}"
        full_name = f"*ФИО:* {self.__get_redacted(dto.full_name or '')}"
        phone_number = f"*Номер телефона:* {self.__get_redacted(dto.phone_number or '')}"
        telegram = f"\n*Юзернейм:* {self.__get_redacted(dto.telegram or '')}" \
            if dto.telegram and dto.telegram != f"@{username}" else ""
        total_price = f"*К оплате:* {self.__get_redacted(str(dto.total_price) or '')} р\."
        body = f"Заказ комплекта:\n{service}\n{address}\n{full_name}\n{phone_number}{telegram}\n{amount}\n{total_price}"
        return self.__build(body=body)

    def input_wallet_number(self):
        body = f"Пожалуйста, введите номер кошелька."
        return self.__build(body=body)

    def choose_docs(self, service: str):
        alert = f""
        if service == '1c':
            alert += f"\n\nОбратите внимание, что Цупис делается только на Ваши данные!\nЕсли заказ будет на наши, " \
                     f"то гарантий на данные не будет."
        text = f"Пожалуйста, выберете данные для идентификации."
        body = f"{text}{alert}"
        return self.__build(body=body)

    def premium_switched(self, status: bool):
        if status:
            return self.__premium_enabled()
        else:
            return self.__premium_disabled()

    def __premium_enabled(self):
        body = f"Заказ будет выполнен в приоритетном режиме"
        return self.__build(body=body)

    def __premium_disabled(self):
        body = f"Заказ будет выполнен в стандартном режиме"
        return self.__build(body=body)

    def upload_string_docs(self):
        body = f"Пожалуйста, отправьте текстовые данные для идентификации"
        return self.__build(body=body)

    def upload_image_docs(self):
        body = f"Пожалуйста, загрузите до 3 изображений в форматах: PNG/JPEG.\n" \
               f"Учтите, что при загрузке новых изображений старые удаляются."
        return self.__build(body=body)

    def view_string_docs(self, data: str):
        body = f"Ваши данные для идентификации:\n{self.__get_redacted(text=data) or ''}"
        return self.__build(body=body)

    def view_image_docs(self):
        body = f"Ваши данные для идентификации:"
        return self.__build(body=body)

    def order_success(self, response: dict):
        order_id = response['order_id'] or 0
        order_ids = response['order_ids'] or []
        order_price = response['order_price'] or ''
        if order_id > 0:
            return self.__single_order(order_id, order_price)
        elif len(order_ids) > 0:
            return self.__multi_order(order_ids, order_price)

        return self.__build(*self.errorHandler.get_message_by_code(ErrorCodes.Unexpected.value))

    def __single_order(self, order_id, order_price):
        text_to_redact = f"Заказ № {order_id} на сумму {order_price} ₽ успешно создан!"
        redacted_text = self.__get_redacted(text_to_redact)
        header = self.__get_redacted("[ЗАКАЗ✅]")
        hyperlink = f"[К списку заказов]({self.ordersUrl})"
        body = f"{header}\n{redacted_text}\n\n{hyperlink}"
        return self.__build(body=body)

    def __multi_order(self, order_ids, order_price):
        text_to_redact = f"Успешно создано {len(order_ids)} заказов на сумму {order_price} ₽!"
        redacted_text = self.__get_redacted(text_to_redact)
        header = self.__get_redacted("[ЗАКАЗ✅]")
        hyperlink = f"[К списку заказов]({self.ordersUrl})"
        body = f"{header}\n{redacted_text}\n\n{hyperlink}"
        return self.__build(body=body)

    def input_amount(self):
        body = f"Пожалуйста, введите желаемое количество."
        return self.__build(body=body)

    def input_address(self):
        body = f"Пожалуйста, укажите адрес доставки (Страна, город, улица, дом, квартира)."
        return self.__build(body=body)

    def input_full_name(self):
        body = f"Пожалуйста, введите ФИО получателя."
        return self.__build(body=body)

    def input_phone_number(self):
        body = f"Пожалуйста, введите номер телефона получателя."
        return self.__build(body=body)

    def input_telegram(self):
        body = f"Пожалуйста, введите дополнительный телеграм для связи."
        return self.__build(body=body)

    def choose_delivery_type(self):
        body = f"Пожалуйста, выберете способ доставки."
        return self.__build(body=body)

    def page_info(self, page: int):
        body = f"Страница {page}"
        return self.__build(body=body)

    def get_order_list(self, _type: str, _list: dict):
        _type_key = f"{_type}List"
        try:
            type_prompt = getattr(Prompts, _type_key).value
        except Exception:
            type_prompt = 'заказов'
        body = f"Список Ваших {type_prompt}:"
        for order_id in _list:
            index = list(_list.keys()).index(order_id) + 1
            service = _list[order_id]['service_label'] \
                if 'service_label' in _list[order_id] and _list[order_id]['service_label'] else 'Неизвестно'
            status = Prompts.statuses.value[_list[order_id]['status']]
            body += f"\n*{index}*\. {order_id} — {self.__get_redacted(service)} — {status}"
        return self.__build(body=body)

    def __base_order_info(self, _type, order_info: dict):
        order_id = order_info['id']
        service_name = self.__get_redacted(order_info['service_label']) \
            if 'service_label' in order_info and order_info['service_label'] else 'Неизвестно'
        price = self.__get_redacted(f"{order_info['price']} руб.")
        created_at = self.__get_redacted(order_info['created_at'])
        status = Prompts.statusesFull.value[order_info['status']]
        return order_id, service_name, price, created_at, status

    def ident_info(self, order_info: dict):
        order_id, service_name, price, created_at, status = self.__base_order_info(_type='ident',
                                                                                   order_info=order_info)
        wallet_number = self.__get_redacted(order_info['number'])
        docs_info = self.__get_redacted(Prompts.docsInfo.value[int(order_info['data_type'])])
        premium_status = List.confirmation.value[0] if order_info['premium'] else List.confirmation.value[1]
        body = f"Ваш заказ идентификации \#*`{order_id}`*:\n" \
               f"*Сервис*: {service_name}\n" \
               f"*Номер кошелька*: {wallet_number}\n" \
               f"*Данные для идентификации*: {docs_info}\n" \
               f"*Премиум*: {premium_status}\n" \
               f"*Стоимость*: {price}\n" \
               f"*Время заказа*: {created_at}\n" \
               f"*Статус*: {status}"
        return self.__build(body=body)

    def wallet_info(self, order_info: dict):
        order_id, service_name, price, created_at, status = self.__base_order_info(_type='wallet',
                                                                                   order_info=order_info)
        body = f"Ваш заказ готового кошелька \#*`{order_id}`*:\n" \
               f"*Сервис*: {service_name}\n" \
               f"*Стоимость*: {price}\n" \
               f"*Время заказа*: {created_at}\n" \
               f"*Статус*: {status}"
        if 'number' in order_info and 'password' in order_info and 'proxy' in order_info:
            body += f"\n\n" \
                    f"*Номер кошелька*: `{self.__get_redacted(order_info['number'])}`\n" \
                    f"*Пароль*: ||{self.__get_redacted(order_info['password'])}||\n" \
                    f"*Прокси*: {self.__get_redacted(order_info['proxy'])}"
        return self.__build(body=body)

    def bundle_info(self, order_info: dict):
        order_id, service_name, price, created_at, status = self.__base_order_info(_type='bundle',
                                                                                   order_info=order_info)
        address = self.__get_redacted(order_info['address'])
        full_name = self.__get_redacted(order_info['full_name'])
        delivery_number = self.__get_redacted(order_info['delivery_number'])
        tg_username = self.__get_redacted(order_info['tg_username'])
        delivery_method = self.__get_redacted(List.deliveryType.value[order_info['delivery_method']])
        body = f"Ваш заказ готового кошелька \#*`{order_id}`*:\n" \
               f"*Сервис*: {service_name}\n" \
               f"*Адрес доставки*: {address}\n" \
               f"*Способ доставки*: {delivery_method}\n" \
               f"*ФИО получателя*: {full_name}\n" \
               f"*Телефон получателя*: {delivery_number}\n" \
               f"*Контакты*: {tg_username}\n" \
               f"*Стоимость*: {price}\n" \
               f"*Время заказа*: {created_at}\n" \
               f"*Статус*: {status}"

        if status == Prompts.statusesFull.value['done']:
            body += f"\n\n" \
                    f"Трек\-код: `{self.__get_redacted(order_info['track_code'])}`"
            if order_info['wallet_number']:
                body += f"\nНомер кошелька: {self.__get_redacted(order_info['wallet_number'])}"

        return self.__build(body=body)

    def wallet_additional_info(self):
        return self.__build(body=f"Доп. данные кошелька:")
