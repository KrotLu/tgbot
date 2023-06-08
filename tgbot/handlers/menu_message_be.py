from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.dispatcher import FSMContext

from tgbot.filters import Menu_states
from tgbot.data_base import Task_Menu
from tgbot.keyboards import Keyboard_Start, Keyboard_Menu2, Keyboard_Fin

task_menu = Task_Menu()

async def menu_taste(message: Message, state: FSMContext):
    task_drinks = task_menu.taste
    
    if await be_intermediate(state, message, task_drinks):
        data=await state.get_data()
        kb = Keyboard_Menu2(take_columns(task_menu.aroma1, data.get('res')))
        await message.answer('Выбери аромат',  reply_markup=kb.kb)

async def menu_aroma1(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma1

    if await be_intermediate(state, message, task_drinks):
        data=await state.get_data()
        kb = Keyboard_Menu2(take_columns(task_menu.aroma2, data.get('res')))
        await message.answer('Выбери аромат',  reply_markup=kb.kb)

async def menu_aroma2(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma2

    if await be_intermediate(state, message, task_drinks):
        await message.answer('Генирирую результат', reply_markup=Keyboard_Fin.kb)

async def be_intermediate(state, message, task_drinks):
    text = message.text
    data=await state.get_data()
    result=data.get('res')
    if text in task_drinks.columns:
        list=data.get('list_column') 
        list.append(text)
        await state.update_data(list_column=list)

    elif text=='Выбрано':
        list_column=data.get('list_column') 
        if len(list_column)==0:
            await message.answer('Выберите один или несколько вариантов')
            return False
        task_drinks = task_drinks.loc[:, list_column]
        new_res = take_drinks(task_drinks, result)
        await state.update_data(res = new_res)
        await state.update_data(list_column=[])
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
        if count>=1:
            new_columns.append(c)
    
    return new_columns
    
def register_menu_be(dp: Dispatcher):
    pass
