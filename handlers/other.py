from aiogram import types, Dispatcher
from create_bot import dp
import json

#@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower() for i in message.text.split()}.intersection(set(json.load(open('mat.json')))) !=set():
# генератор множеств, split, чтоб вывести каждое слово, приводим в нижний регистр, intersection(совпадения),
# load open чтение нашего json файла с матами, если НЕ равно пустому set(), значит было матное слово! set работает быстрее!
        await message.reply('Маты запрещены, по губам получишь!')
        await message.delete()
    elif message.text == 'привет':
        return await message.answer('И тебе привет! )')
    await message.reply(message.text + '!')



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
