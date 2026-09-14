import bot.keyboards as keyboards
from bot.handler.dto import *
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


def main_keyboard(balance='') -> ReplyKeyboardMarkup:
    replenishment_button = [keyboards.List.replenish.value[0] + f"({balance} р.)"]

    keyboard_builder = keyboards.Builder(is_custom=True)

    keyboard_builder.add_row(keyboards.List.order.value)
    keyboard_builder.add_row(replenishment_button)
    keyboard_builder.add_row(keyboards.List.settings.value)
    return keyboard_builder.get_custom_keyboard()


def replenishment_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)

    keyboard_builder.add_row(keyboards.List.replenishmentMethod.value, row_width=3)
    keyboard_builder.add_row(keyboards.List.goBack.value)
    return keyboard_builder.get_custom_keyboard()


def confirmation_keyboard() -> ReplyKeyboardMarkup:
    return keyboards.Builder(items=keyboards.List.confirmation.value).make_row_keyboard()


def settings_keyboard(refill_notif=0, order_notif=0) -> ReplyKeyboardMarkup:
    settings_menu_buttons = [keyboards.List.settingsMenu.value['refill'] + ('Вкл.' if refill_notif else 'Выкл.'),
                             keyboards.List.settingsMenu.value['order'] + ('Вкл.' if order_notif else 'Выкл.')]

    keyboard_builder = keyboards.Builder(is_custom=True)

    keyboard_builder.add_row(settings_menu_buttons, row_width=1)
    keyboard_builder.add_row(keyboards.List.toMain.value)
    return keyboard_builder.get_custom_keyboard()


def done_keyboard() -> ReplyKeyboardMarkup:
    return keyboards.Builder(items=keyboards.List.done.value).make_row_keyboard()


def order_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)
    order_type_list = list(keyboards.List.orderType.value.values())

    keyboard_builder.add_row(order_type_list[:2])
    keyboard_builder.add_row(order_type_list[2:], row_width=1)
    keyboard_builder.add_row(keyboards.List.toMain.value)
    return keyboard_builder.get_custom_keyboard()


def product_category_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)

    keyboard_builder.add_row([keyboards.List.productCategory.value[0]])
    keyboard_builder.add_row(keyboards.List.productCategory.value[1:])
    keyboard_builder.add_row(keyboards.List.goBack.value)
    return keyboard_builder.get_custom_keyboard()


def service_reply_keyboard(_type, service_list) -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)

    if service_list:
        buttons = [service['full_label'] for service in service_list]
        keyboard_builder.add_row(buttons, row_width=2)
    keyboard_builder.add_row(keyboards.List.goBack.value)
    return keyboard_builder.get_custom_keyboard()


def service_pagination_keyboard(service_list, page: int = 1) -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)

    buttons = {}
    for i in range(len(service_list[10 * (page - 1):10 * page])):
        buttons[service_list[i + 10 * (page - 1)]['short']] = f"{i + 1}"

    keyboard_builder.add_row(buttons, row_width=5)

    pagination_row = keyboards.List.pagination.value
    pagination_row['page'] = f"({page})"
    keyboard_builder.add_row(pagination_row)

    keyboard_builder.add_row(keyboards.List.goBackDict.value)

    return keyboard_builder.get_custom_keyboard()


def docs_type_keyboard(docs_list) -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)

    buttons = []
    for docs_type in keyboards.List.docsType.value.keys():
        if docs_type in (0, 3):
            buttons.append(f"{keyboards.List.docsType.value[docs_type]}")
        elif docs_type in (1, 4):
            buttons.append(f"{keyboards.List.docsType.value[docs_type]} ({docs_list[str(docs_type)]} р.)")

    keyboard_builder.add_row(buttons, row_width=2)
    keyboard_builder.add_row(keyboards.List.goBack.value)
    return keyboard_builder.get_custom_keyboard()


def service_form_keyboard(dto: ServiceDto) -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)

    primary_buttons = {
        keyboards.Callbacks.InputProduct.value: '✅ Номер введен' if dto.product else 'Ввести номер',
        keyboards.Callbacks.ChooseHandler.value: 'Сменить сервис'
    }
    secondary_buttons = {
        keyboards.Callbacks.ChooseDocs.value: 'Сменить тип данных',
        keyboards.Callbacks.PrioritySwitch.value: 'Приоритет: ' + ('вкл' if dto.priority else 'выкл'),
    }
    confirm_order = {
        keyboards.Callbacks.ConfirmOrder.value: 'Сделать заказ'
    }
    upload_docs = {
        keyboards.Callbacks.UploadDocs.value: '✅ Документы загружены' if dto.validate_docs() else 'Загрузить документы'
    }
    view_docs = {
        keyboards.Callbacks.ViewDocs.value: 'Посмотреть загруженные данные'
    }
    go_back = keyboards.List.goBackDict.value

    keyboard_builder.add_row(primary_buttons, row_width=1)
    keyboard_builder.add_row(secondary_buttons, row_width=2)
    if dto.docs_type in (0, 3):
        keyboard_builder.add_row(upload_docs)
        if dto.validate_docs():
            keyboard_builder.add_row(view_docs)
    if dto.validate():
        keyboard_builder.add_row(confirm_order)
    keyboard_builder.add_row(go_back)

    return keyboard_builder.get_custom_keyboard()


def product_form_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)
    primary_buttons = {
        keyboards.Callbacks.ChangeAmount.value: '🔢 Изменить количество',
        keyboards.Callbacks.ConfirmOrder.value: '✅ Сделать заказ'
    }
    go_back = keyboards.List.goBackDict.value
    keyboard_builder.add_row(primary_buttons, row_width=2)
    keyboard_builder.add_row(go_back)

    return keyboard_builder.get_custom_keyboard()


def delivery_form_keyboard(dto: DeliveryDto) -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)

    primary_buttons = {
        keyboards.Callbacks.InputAddress.value:
            '✅ Адрес доставки введен' if dto.address else 'Ввести адрес доставки',
        keyboards.Callbacks.InputFullName.value:
            '✅ ФИО введено' if dto.full_name else 'Ввести ФИО',
        keyboards.Callbacks.InputPhoneNumber.value:
            '✅ Номер телефона введен' if dto.phone_number else 'Ввести номер телефон',
    }
    secondary_buttons = {
        keyboards.Callbacks.ChangeAmount.value: '🔢 Изменить количество',
        keyboards.Callbacks.ChooseDeliveryType.value: f"📦 {keyboards.List.deliveryType.value[dto.delivery_type]}",
    }
    telegram_button = {
        keyboards.Callbacks.InputTelegram.value:
            '✅ Телеграм для связи введен' if dto.telegram else 'Ввести телеграм для связи'
    }
    confirm_order = {
        keyboards.Callbacks.ConfirmOrder.value: 'Сделать заказ'
    }
    go_back = keyboards.List.goBackDict.value

    keyboard_builder.add_row(primary_buttons, row_width=1)
    keyboard_builder.add_row(secondary_buttons, row_width=2)
    keyboard_builder.add_row(telegram_button)
    if dto.validate():
        keyboard_builder.add_row(confirm_order)
    keyboard_builder.add_row(go_back)

    return keyboard_builder.get_custom_keyboard()


def delivery_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(items=keyboards.List.deliveryType.value.values())
    return keyboard_builder.make_row_keyboard()


def order_list_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = keyboards.Builder(is_custom=True)
    order_type_list = list(keyboards.List.orderListType.value.values())

    keyboard_builder.add_row(order_type_list[:2])
    keyboard_builder.add_row(order_type_list[2:], row_width=1)
    keyboard_builder.add_row(keyboards.List.toMain.value)
    return keyboard_builder.get_custom_keyboard()


def order_list_keyboard(order_list: dict, page: int) -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)

    buttons = {}
    for order_id in order_list:
        index = list(order_list.keys()).index(order_id)
        buttons[order_id] = f"{index + 1}"

    keyboard_builder.add_row(buttons, row_width=5)

    pagination_row = keyboards.List.pagination.value
    pagination_row['page'] = f"({page})"
    keyboard_builder.add_row(pagination_row)

    keyboard_builder.add_row(keyboards.List.goBackDict.value)

    return keyboard_builder.get_custom_keyboard()


def order_info_keyboard(has_additional_data: bool) -> InlineKeyboardMarkup:
    keyboard_builder = keyboards.InlineBuilder(is_custom=True)

    if has_additional_data:
        view_data = {keyboards.Callbacks.ViewData.value: keyboards.List.viewData.value[0]}
        keyboard_builder.add_row(view_data)

    done = {keyboards.Callbacks.Done.value: keyboards.List.done.value[0]}
    keyboard_builder.add_row(done)

    return keyboard_builder.get_custom_keyboard()
