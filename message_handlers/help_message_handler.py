from aiogram import types


async def help_message(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Эта функция на стадии разработки')
