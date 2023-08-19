from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove




b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Отправь_номер', request_contact=True)
b5 = KeyboardButton('/Где я?', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)   # one_time_keyboard=True - прячет клавиатуру

#kb_client.add(b1).add(b2).insert(b3)   (add - добавляет с новой строки, insert - в ту же строку, row - все в одну строку сразу)
kb_client.row(b1, b3).row(b2, b4).add(b5)


# Кнопки клавиатуры админа!
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)


