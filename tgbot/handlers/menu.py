from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.filters import Menu_states
from tgbot.data_base import Task_Menu
from tgbot.keyboards import Keyboard_Menu1

task_menu = Task_Menu()

async def menu(message: Message):
    kb = Keyboard_Menu1(task_menu.temp)
    await message.answer('Выбери температуру',  reply_markup=kb.kb)  
    await Menu_states.Q1_Temp.set() 

def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, text='Выбрать напиток')
