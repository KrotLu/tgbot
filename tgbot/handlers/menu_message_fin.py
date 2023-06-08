from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.dispatcher import FSMContext

from tgbot.filters import Menu_states
from tgbot.data_base import Task_Menu
from tgbot.keyboards import Keyboard_Start

from random import choice

task_menu = Task_Menu()

async def menu_fin(message: Message, state: FSMContext):
    data = await state.get_data()
    result = data.get('res')
    
    res_3 = []
    if len(result)>2:
        while len(res_3)<3:
            r = choice(result)
            
            res_3.append(r)
            result.remove(r)
    else:
        res_3=result
    

    await message.answer('вот что получилось', reply_markup=Keyboard_Start.kb)
    for i in res_3:
        res_str= take_res_str(i)
        
        photo = task_menu.photo[i]
        if photo != 'nan':
            await message.answer_photo(photo, caption=i)
        else:
            await message.answer(res_str)

    await state.reset_state()

def take_col(task, i):
    res_str=''
    for c in task.columns:
            val = task.loc[i,c]
            if val=='+':
                res_str +=c+'    '
            elif val !='nan':
                res_str +=val+'    '
    return res_str

def take_res_str(i:str):
    res_str='Напиток:    '+ i

    res_str+= '\n'+'Температура:    ' + take_col(task_menu.temp, i)
    res_str+= '\n'+'Объем:    ' + take_col(task_menu.vol, i)
    res_str+= '\n'+'Крепость:    ' + take_col(task_menu.grade, i)
    res_str+= '\n'+'Вкусы:    ' + take_col(task_menu.taste, i)
    res_str+= '\n'+'Ароматы:    ' + take_col(task_menu.aroma1, i) + take_col(task_menu.aroma2, i)
    res_str+= '\n'+'Бокал:    ' + take_col(task_menu.glass, i)

    res_str+= '\n'+'Цена:    ' + task_menu.price[i] + 'р'
    res_str+= '\n'+'Состав:    '+ task_menu.comp[i] 
    res_str+= '\n'+'Описание:    ' + task_menu.descr[i] 

    return res_str
    
def register_menu_fin(dp: Dispatcher):
    dp.register_message_handler(menu_fin, state=Menu_states.Q7_Fin)