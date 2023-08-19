from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db

#@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    try:
        await bot.send_message(chat_id=message.from_user.id, text='Приятного аппетита!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('общение с ботом через ЛС, напишите ему: https://t.me/popo_pizza_bot ')

#@dp.message_handler(commands=['Режим_работы'])
async def open_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Вс-Чт: 9:00-18:00, Пт-Сб: 10:00-17:00')

#@dp.message_handler(commands=['Расположение'])
async def place_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='70 лет Октября, д. 22')

#@dp.message_handler(commands=["Меню"])
async def pizza_menu(message: types.Message):
    await sqlite_db.sql_read(message)           # Вызов из SQL  ЧТЕНИЕ!


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start', 'help'])
    dp.register_message_handler(open_cmd, commands=['Режим_работы'])
    dp.register_message_handler(place_cmd, commands=['Расположение'])
    dp.register_message_handler(pizza_menu, commands=["Меню"])