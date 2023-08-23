from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher import FSMContext

from tgbot.filters import Menu_states
from tgbot.data_base import Task_Menu
from tgbot.keyboards import Keyboard_Start, Keyboard_Menu1, Keyboard_Menu2, Keyboard_Fin, Keyboard_read_more, Keyboard_restart

from random import choice

task_menu = Task_Menu()

async def menu_temp(message: Message, state: FSMContext):
    columns=task_menu.vol
    kb = Keyboard_Menu1(columns)
    
    task_drinks = task_menu.temp
    res_list = list(task_drinks.index)
    await state.update_data(res=res_list)
    await state.update_data(list_column=[])
    await state.update_data(next_columns = task_drinks.columns)
    
    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        columns = take_columns(task_menu.vol, data.get('res'))
        kb = Keyboard_Menu1(columns)
        await state.update_data(next_columns = columns)
        await message.answer('Выбери объем',  reply_markup=kb.kb)

async def menu_vol(message: Message, state: FSMContext):
    task_drinks = task_menu.vol
    
    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        columns = take_columns(task_menu.grade, data.get('res'))
        kb = Keyboard_Menu1(columns)
        await state.update_data(next_columns = columns)
        await message.answer('Выбери крепость',  reply_markup=kb.kb)

async def menu_grade(message: Message, state: FSMContext):
    task_drinks = task_menu.grade

    if await intermediate(state, message, task_drinks):

        data=await state.get_data()
        columns=take_columns(task_menu.taste, data.get('res'))
        kb = Keyboard_Menu2(columns)
        await state.update_data(next_columns = columns)
        await message.answer('Выбери вкус',  reply_markup=kb.kb)

async def menu_taste(message: Message, state: FSMContext):
    task_drinks = task_menu.taste
    
    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        columns = take_columns(task_menu.aroma1, data.get('res'))
        if len(columns)>1:
            kb = Keyboard_Menu2(columns)
            await state.update_data(next_columns = columns)
            await message.answer('Выбери аромат 1',  reply_markup=kb.kb)
        else:
            await menu_fin(message, state)
            #await message.answer('Генирирую результат', reply_markup=Keyboard_Fin.kb)

async def menu_aroma1(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma1

    if await intermediate(state, message, task_drinks):
        data=await state.get_data()
        columns = take_columns(task_menu.aroma2, data.get('res'))

        if len(columns)>1:
            kb = Keyboard_Menu2(columns)
            await state.update_data(next_columns = columns)
            await message.answer('Выбери аромат 2',  reply_markup=kb.kb)
        else:
           
            await menu_fin(message, state)
            #await message.answer('Генирирую результат', reply_markup=Keyboard_Fin.kb)
            

async def menu_aroma2(message: Message, state: FSMContext):
    task_drinks = task_menu.aroma2

    if await intermediate(state, message, task_drinks):
        #await message.answer('Генирирую результат', reply_markup=Keyboard_Fin.kb)
        await menu_fin(message, state)



async def intermediate(state, message, task_drinks):
    text = message.text
    data=await state.get_data()
    result=data.get('res')
    columns=data.get('next_columns')
    if text == 'Вернуться в меню':
        await menu_fin_all(message, state)
    elif text == 'Случайный выбор':
        random_column=choice(columns)
        new_res = take_drinks(task_drinks.loc[:, [random_column]], result)
        await message.answer('Выбран:' )
        await message.answer(random_column)
    elif text in columns:
        new_res = take_drinks(task_drinks.loc[:, [text]], result)
    else:
        await message.answer('Не понял вас, повторите выбор, либо можете вернуться в меню', reply_markup= Keyboard_restart.kb)
        
        return False    
    
    await state.update_data(res = new_res)
    if len(new_res)==0:
        await message.answer('Не нашлось таких напитков',reply_markup=Keyboard_Start.kb )
        await state.reset_state()
        return False
    else:
        await Menu_states.next()
        return True
    
    

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
    

    await message.answer('Напитки по выбранным критериям:', reply_markup=Keyboard_Fin.kb)
    res_dict = {}
    for i in res_3:
        res_str= take_res_str(i)
        res_dict[i] = res_str[1]
        photo = task_menu.photo[i]
        kb = Keyboard_read_more(i)
        if photo != 'nan':
            await message.answer_photo(photo, caption=res_str[0], reply_markup= kb.kb)
        else:
            await message.answer(res_str[0], reply_markup= kb.kb)
    await state.update_data(res_dict = res_dict)
    
    await state.set_state(Menu_states.Q7_Fin)
    #await state.reset_state()

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
    #res_str+= '\n'+'Бокал:    ' + take_col(task_menu.glass, i)

    res_str+= '\n'+'Цена:    ' + task_menu.price[i] + 'р'
    res_str+= '\n'+'Состав:    '+ task_menu.comp[i] 
    res_all_str='Подробнее о напитке '+ i+':    '
    #res_str+= '\n'+'Температура:    ' + take_col(task_menu.temp, i)
    #res_str+= '\n'+'Объем:    ' + take_col(task_menu.vol, i)
    res_all_str+= '\n'+'Крепость:    ' + take_col(task_menu.grade, i)
    res_all_str+= '\n'+'Вкусы:    ' + take_col(task_menu.taste, i)
    res_all_str+= '\n'+'Ароматы:    ' + take_col(task_menu.aroma1, i) + take_col(task_menu.aroma2, i)
    descr =  task_menu.descr[i] 
    if descr != 'nan':
        res_all_str+= '\n'+'Описание:    ' + descr
    
    return [res_str, res_all_str]
async def menu_fin_all(message: Message, state: FSMContext):

    if message.text == 'Вернуться в меню':
        await message.answer('Всегда рад помочь!', reply_markup=Keyboard_Start.kb)
        await state.reset_state()
        await Menu_states.Q0_Def.set() 
    else:
        await message.answer('Вы можете подробнее узнать о напитке, либо вернуться в меню')
    


async def callback_read_more(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    res_dict = data.get('res_dict')

    await call.message.answer(res_dict[call.data])
    
async def callback_restart(call: CallbackQuery,state: FSMContext):

    if call.data == 'menu':
        await call.message.answer('Всегда рад помочь!', reply_markup=Keyboard_Start.kb) 
        await state.reset_state()
        await Menu_states.Q0_Def.set() 

async def menu_random(message: Message, state: FSMContext):
    
    name =choice(task_menu.data.index)
    print(task_menu.data.index)
    print(name)
    res_str= take_res_str(name)
    res_dict ={ name: res_str[1]} 
    await state.update_data(res_dict = res_dict)
    photo = task_menu.photo[name]
    kb = Keyboard_read_more(name)
    await message.answer('Случайный напиток:',reply_markup=Keyboard_Fin.kb )
    if photo != 'nan':
        await message.answer_photo(photo, caption=res_str[0], reply_markup= kb.kb)
    else:
        await message.answer(res_str[0], reply_markup= kb.kb)
    await Menu_states.Q7_Fin.set() 

def register_menu_en(dp: Dispatcher):

    dp.register_message_handler(menu_temp, state=Menu_states.Q1_Temp)
    dp.register_message_handler(menu_vol, state=Menu_states.Q2_Vol)
    dp.register_message_handler(menu_grade, state=Menu_states.Q3_Grade)
    dp.register_message_handler(menu_taste, state=Menu_states.Q4_Taste)
    dp.register_message_handler(menu_aroma1, state=Menu_states.Q5_Aroma1)
    dp.register_message_handler(menu_aroma2, state=Menu_states.Q6_Aroma2)
    dp.register_message_handler(menu_fin_all, state=Menu_states.Q7_Fin)
    dp.register_callback_query_handler(callback_read_more, state=Menu_states.Q7_Fin)
    dp.register_message_handler(menu_random, text='Случайный напиток', state=Menu_states.Q0_Def)
    dp.register_callback_query_handler(callback_restart, state= Menu_states.all_states)

