from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class KeyboardBuilder:

    def __init__(self, items: list[str] = None, resize_keyboard: bool = True, is_custom=False):
        self.items = items
        self.resize_keyboard = resize_keyboard
        if is_custom:
            self.__keyboard_builder = ReplyKeyboardBuilder()

    def add_row(self, items, row_width=None):
        big_row = [KeyboardButton(text=item) for item in items]
        self.__keyboard_builder.row(*big_row, width=row_width)

    def get_custom_keyboard(self) -> ReplyKeyboardMarkup:
        return self.__keyboard_builder.as_markup(resize_keyboard=self.resize_keyboard)

    def make_row_keyboard(self) -> ReplyKeyboardMarkup:
        row = [KeyboardButton(text=item) for item in self.items]
        return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=self.resize_keyboard)

    def make_rows_keyboard(self, row_width: int) -> ReplyKeyboardMarkup:
        rows = []
        row_height = len(self.items) // row_width + len(self.items) % 2
        for i in range(row_height):
            row = []
            for j in range(row_width):
                if len(self.items) - j - (i * row_width) > 0:
                    row.append(KeyboardButton(text=self.items[j + (i * row_width)]))
            if row:
                rows.append(row)
        return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=self.resize_keyboard)


class InlineBuilder:

    def __init__(self, items=None, is_custom=False):
        self.items = items
        if is_custom:
            self.__keyboard_builder = InlineKeyboardBuilder()

    def add_row(self, items: dict, row_width=None):
        big_row = [InlineKeyboardButton(text=value, callback_data=key) for key, value in items.items()]
        self.__keyboard_builder.row(*big_row, width=row_width)

    def get_custom_keyboard(self) -> InlineKeyboardMarkup:
        return self.__keyboard_builder.as_markup()

    def make_row_keyboard(self) -> InlineKeyboardMarkup:
        row = [InlineKeyboardButton(text=value, callback_data=key) for key, value in self.items.items()]
        return InlineKeyboardMarkup(inline_keyboard=[row])
