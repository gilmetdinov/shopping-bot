from aiogram import Bot
from aiogram.types import BotCommandScopeDefault
from aiogram.exceptions import TelegramBadRequest
import message as _message
import bot.commands


class BotClient:

    def __init__(self, token, webhook_url):
        self.__token = token
        self.instance = Bot(token=self.__token)
        self.__webhookUrl = webhook_url
        self.__message_builder = _message.Builder()

    async def set_webhook(self):
        return await self.instance.set_webhook(self.__webhookUrl)

    async def delete_webhook(self):
        return await self.instance.delete_webhook()

    async def set_commands(self):
        commands = bot.commands.get_commands_array()
        return await self.instance.set_my_commands(commands, BotCommandScopeDefault())

    async def delete_commands(self):
        return await self.instance.delete_my_commands(BotCommandScopeDefault())

    async def close_session(self):
        return await self.instance.session.close()

    async def send_message(self, chat_id=386636492, message='test', parse_mode=None):
        try:
            await self.instance.send_message(chat_id, message, parse_mode=parse_mode)
            return True
        except TelegramBadRequest:
            return False

    async def send_message_mass(self, chat_ids: list, message, parse_mode=None):
        success_chat_ids = []
        fail_chat_ids = []
        for chat_id in chat_ids:
            if await self.send_message(chat_id, message, parse_mode=parse_mode):
                success_chat_ids.append(chat_id)
            else:
                fail_chat_ids.append(chat_id)
        return {'success': success_chat_ids, 'fail': fail_chat_ids}

    async def send_notification(self, chat_id: int, notif_type, contents):
        message = self.__message_builder.notification(notif_type=notif_type, contents=contents)
        if message:
            return await self.send_message(chat_id=chat_id, message=message, parse_mode='MarkdownV2')
        return False

    async def send_notification_mass(self, chat_ids: list, notif_type, contents):
        message = self.__message_builder.notification(notif_type=notif_type, contents=contents)
        if message:
            return await self.send_message_mass(chat_ids=chat_ids, message=message, parse_mode='MarkdownV2')
        return False
