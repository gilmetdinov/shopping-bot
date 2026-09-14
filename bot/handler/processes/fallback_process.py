from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.handler.processes.common import AbstractProcess


class FallbackProcess(AbstractProcess):
    """Глобальный catch-all: отвечает на нераспознанные сообщения, чтобы бот не молчал.

    Регистрируется ПОСЛЕДНИМ (без state-фильтров), поэтому срабатывает только когда
    ни один state-specific handler не сматчился.
    """

    def set(self):
        @self.router.message()
        async def fallback(message: Message, state: FSMContext) -> None:
            await message.answer(self.messageBuilder.incorrect_input(), parse_mode='MarkdownV2')
