from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import client_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    discriptions = State()
    price = State()

#@dp.message_handler(commands=['модератор', 'moderator'], is_chat_admin=True)   # проверка админа
async def check_admin(message: types.message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, text='Тебе чего хозяин?', reply_markup=client_kb.button_case_admin)
    await message.delete()


#@dp.message_handler(commands=['Загрузить'], state=None)        # старт на загрузку, запуск цикла
async def cmd_download(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.answer('Загрузите фото')

#@dp.message_handler(state='*', commands='отмена')                  # отмена цикла, должна быть именно здесь!
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')        # ignore_case - игнорировать регистр букв !
async def cancel_cmd(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Вы прервали загрузку данных')


#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)     # фото
async def cmd_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Напиши имя пиццы')

#@dp.message_handler(state=FSMadmin.name)                        # имя
async def cmd_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text.upper()
        await FSMadmin.next()
        await message.reply('Напиши ингредиенты')

#@dp.message_handler(state=FSMadmin.discriptions)                    # описание
async def cmd_discriptions(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['discriptions'] = message.text
        await FSMadmin.next()
        await message.reply('Напиши цену')

#@dp.message_handler(state=FSMadmin.price)                           # цена и завершаем цикл!
async def cmd_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['price'] = message.text
        await sqlite_db.sql_add_command(state)          # вызов из sql! ЗАПИСЬ
        await state.finish()
        await message.reply('Информация сохранена!')
        await message.answer(f"Фото: {data['photo']}\nИмя: {data['name']} Описание: {data['discriptions']}\nЦена: {data['price']} ")

#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


#@dp.message_handler(commands=['Удалить'])
async def delete_item(message: types.Message):
    if message.from_user.id ==ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')) )


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_download, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_cmd, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_cmd, Text(equals=['отмена'], ignore_case=True), state='*')   # ignore_case - игнорировать регистр букв !
    dp.register_message_handler(cmd_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(cmd_name, state=FSMadmin.name)
    dp.register_message_handler(cmd_discriptions, state=FSMadmin.discriptions)
    dp.register_message_handler(cmd_price, state=FSMadmin.price)
    dp.register_message_handler(check_admin, commands=['модератор', 'moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands=['Удалить'])