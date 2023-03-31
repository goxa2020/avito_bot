from aiogram import types
from loader import bot


async def show_ad_to_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
