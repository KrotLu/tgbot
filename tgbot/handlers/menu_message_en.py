from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.dispatcher import FSMContext

from tgbot.filters import Menu_states
from tgbot.data_base import Task_Menu
from tgbot.keyboards import Keyboard_Start, Keyboard_Menu1, Keyboard_Menu2, Keyboard_Fin

from random import choice

task_menu = Task_Menu()

async def menu_temp(message: Message, state: FSMContext):
    kb = Keyboard_Menu1(task_menu.vol)

    task_drinks = task_menu.temp
    res_list = list(task_drinks.index)
    await state.update_data(res=res_list)
    await state.update_data(list_column=[])
    
    if await intermediate(state, message, task_drinks):
        await message.answer('Выбери объем',  reply_markup=kb.kb)

async def menu_vol(message: Message, state: FSMContext):
    task_drinks = task_menu.vol
    kb = Keyboard_Menu1(task_menu.grade)
    if await intermediate(state, message, task_drinks):
        await message.answer('Выбери крепость',  reply_markup=kb.kb)

async def menu_grade(message: Message, state: FSMContext):
    task_drinks = task_menu.grade
    
    if await intermediate(state, message, task_drinks):

        data=await state.get_data()
        kb = Keyboard_Menu2(take_columns(task_menu.taste, data.get('res')))
        
        await message.answer('Выбери вкус',  reply_markup=kb.kb)

async def menu_taste(message: Message, state: FSMContext):
    task_drinks = task_menu.taste
    
    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        columns = take_columns(task_menu.aroma1, data.get('res'))
        kb = Keyboard_Menu2(columns)
        await message.answer('Выбери аромат',  reply_markup=kb.kb)

async def menu_aroma1(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma1

    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        kb = Keyboard_Menu2(take_columns(task_menu.aroma2, data.get('res')))
        await message.answer('Выбери аромат',  reply_markup=kb.kb)

async def menu_aroma2(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma2

    if await intermediate(state, message, task_drinks):
        await message.answer('Генирирую результат', reply_markup=Keyboard_Fin.kb)

async def intermediate(state, message, task_drinks):
    text = message.text
    data=await state.get_data()
    result=data.get('res')

    if text in task_drinks.columns:
        new_res = take_drinks(task_drinks.loc[:, [text]], result)
        await state.update_data(res = new_res)
        if len(new_res)==0:
            await message.answer('Не нашлось таких напитков',reply_markup=Keyboard_Start.kb )
            await state.reset_state()
            return False
        else:
            await Menu_states.next()
            return True
    else:
        await message.answer('Не понял, повторите выбор')
        return False

def take_drinks(drinks, result:list):
    new_result = []
    for i in result:
        if (drinks.loc[i] == '+').any():
            new_result.append(i)
    print(new_result)  
    return new_result

def take_columns(drinks, res):
    new_columns = []
    for c in drinks.columns:
        count = 0
        for i in res:
            if (drinks.loc[i,c] == '+'):
                count+=1
                print(count, 'это нашлись плюсы в', i, c)  
        if count>=1:
            new_columns.append(c)
    return new_columns

 
    
def register_menu_en(dp: Dispatcher):

    dp.register_message_handler(menu_temp, state=Menu_states.Q1_Temp)
    dp.register_message_handler(menu_vol, state=Menu_states.Q2_Vol)
    dp.register_message_handler(menu_grade, state=Menu_states.Q3_Grade)
    dp.register_message_handler(menu_taste, state=Menu_states.Q4_Taste)
    dp.register_message_handler(menu_aroma1, state=Menu_states.Q5_Aroma1)
    dp.register_message_handler(menu_aroma2, state=Menu_states.Q6_Aroma2)
