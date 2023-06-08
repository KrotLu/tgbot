from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from tgbot.config import Config


class StartFilter(BoundFilter):

    async def check(self, message: types.Message):
        return message.text=="/start"
       
