import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from admin import *
from markups import *
from loader import bot, db, dp
from callback_handlers import *
from message_handlers import *
from add_ad import *


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(name_entered, state=Add_ad.waiting_for_name)
    dp.register_message_handler(product_name_chosen, state=Add_ad.waiting_for_product_name)
    dp.register_message_handler(product_amount_chosen, state=Add_ad.waiting_for_product_amount)
    dp.register_message_handler(product_price_chosen, state=Add_ad.waiting_for_product_price)
    dp.register_message_handler(town_chosen, state=Add_ad.waiting_for_town)
    dp.register_message_handler(picture_chosen, state=Add_ad.waiting_for_picture, content_types=['text', 'photo'])
    dp.register_message_handler(accept_chosen, state=Add_ad.waiting_for_accept)


async def start_on(_):
    register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_on)
