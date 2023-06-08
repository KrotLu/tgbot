from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from tgbot.data_base import Task_Menu
task_menu = Task_Menu()

class Keyboard_Start:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button_hi = KeyboardButton('Привет! 👋')
    kb.add(button_hi)

    button1 = KeyboardButton('Выбрать напиток')
    #button2 = KeyboardButton('/test')
    kb.add(button1)
    #kb.insert(button2)

class Keyboard_Menu1:
    def __init__(self,kb_text= task_menu.descr) -> None:
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        self.kb_dict={}
        for text in kb_text:
            self.kb_dict[text]=KeyboardButton(text)
            self.kb.insert(self.kb_dict[text])



class Keyboard_Menu2:
    def __init__(self,kb_text= task_menu.descr) -> None:
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        self.kb_dict={}
        for text in kb_text:
            self.kb_dict[text]=KeyboardButton(text)
            self.kb.insert(self.kb_dict[text])
        #self.kb.add(KeyboardButton('Выбрано'))
    
    def change(self, text):
        self.kb_dict[text]= KeyboardButton(text + ' +')

class Keyboard_Fin:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_hi = KeyboardButton('Получить напиток')
    kb.add(button_hi)

    
    





   