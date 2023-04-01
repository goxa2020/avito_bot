from aiogram import types
from loader import dp


async def help_message(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Эта функция на стадии разработки')
