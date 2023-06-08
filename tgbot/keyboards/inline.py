from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# создаем кнопки с определенными значениями
button1 = InlineKeyboardButton("Кнопка 1", callback_data="button1")
button2 = InlineKeyboardButton("Кнопка 2", callback_data="button2")
button3 = InlineKeyboardButton("Кнопка 3", callback_data="button3")

# создаем объект InlineKeyboardMarkup и добавляем кнопки
keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(button1, button2, button3)
