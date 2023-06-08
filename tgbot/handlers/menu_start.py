from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards import Keyboard_Start

async def start_Bot(message: Message):
    await message.answer('Привет, я бот Григорий')
    await message.answer('Выбери действие',  reply_markup=Keyboard_Start.kb)  
    
def register_menu_start(dp: Dispatcher):
    
    dp.register_message_handler(start_Bot)