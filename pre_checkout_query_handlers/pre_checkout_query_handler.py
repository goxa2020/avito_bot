from aiogram import types

from loader import bot


async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, True)
