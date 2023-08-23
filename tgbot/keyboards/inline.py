from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# создаем кнопки с определенными значениями
button1 = InlineKeyboardButton("Кнопка 1", callback_data="button1")
button2 = InlineKeyboardButton("Кнопка 2", callback_data="button2")
button3 = InlineKeyboardButton("Кнопка 3", callback_data="button3")

# создаем объект InlineKeyboardMarkup и добавляем кнопки
keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(button1, button2, button3)

class Keyboard_read_more:
    def __init__(self,name) -> None:
        self.kb = InlineKeyboardMarkup(resize_keyboard=True)

        self.buttom = InlineKeyboardButton(text='Подробнее', callback_data=name)
        self.kb.add(self.buttom)
class Keyboard_restart:
    
    kb = InlineKeyboardMarkup(resize_keyboard=True)

    buttom = InlineKeyboardButton(text='Вернуться в меню', callback_data='menu') 
    kb.add(buttom)
