from aiogram.types import CallbackQuery


def pin_ad_handler(callback_query: CallbackQuery):
    callback_query.answer('Функция не готова')
