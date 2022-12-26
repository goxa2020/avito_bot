from aiogram import types
from loader import dp


@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Эта функция на стадии разработки')