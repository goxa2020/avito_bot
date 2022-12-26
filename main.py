# import logging
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loader import db, dp
from admin import *
from markups import *
from callback_handlers import *
from message_handlers import start_message_handler, help_message_handler, text_message_handler
from add_ad import *


# Это аналоги @dp.message_handler(), только собранные в одном месте
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(name_entered, state=Add_ad.waiting_for_name)
    dp.register_message_handler(product_name_chosen, state=Add_ad.waiting_for_product_name)
    dp.register_message_handler(product_amount_chosen, state=Add_ad.waiting_for_product_amount)
    dp.register_message_handler(product_price_chosen, state=Add_ad.waiting_for_product_price)
    dp.register_message_handler(town_chosen, state=Add_ad.waiting_for_town)
    dp.register_message_handler(picture_chosen, state=Add_ad.waiting_for_picture, content_types=['text', 'photo'])
    dp.register_message_handler(description_chosen, state=Add_ad.waiting_for_description)
    dp.register_message_handler(accept_chosen, state=Add_ad.waiting_for_accept)


# Функция вызывается при старте бота
async def start_on(_):
    register_handlers(dp)  # Регестрируем message handler`ы


# Функция вызывается при закрытии бота
async def on_shutdown(_):
    db.close()  # Выключаем базу данных


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_on, on_shutdown=on_shutdown)  # Запускаем бота
