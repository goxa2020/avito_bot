import logging

from aiogram import Router, F
from aiogram.filters import Command


from message_handlers.start_message_handler import start_message
from message_handlers.help_message_handler import help_message
from message_handlers.successful_payment_message_handler import process_pay
from message_handlers.text_message_handler import all_messages
from ad_utils.add_ad import *


def register_handlers(router: Router):
    """
    Это аналоги @dp.message(), только собранные в одном месте
    """
    router.message.register(cancel, F.text == "Отмена")

    router.message.register(process_pay, F.content_type == "successful_payment")

    router.message.register(product_name_chosen, Add_ad.waiting_for_product_name)
    router.message.register(product_amount_chosen, Add_ad.waiting_for_product_amount)
    router.message.register(product_price_chosen, Add_ad.waiting_for_product_price)
    router.message.register(town_chosen, Add_ad.waiting_for_town)
    router.message.register(picture_chosen, Add_ad.waiting_for_picture,
                            F.content_type.in_(['text', 'photo']))
    router.message.register(description_chosen, Add_ad.waiting_for_description)
    router.message.register(confirm_chosen, Add_ad.waiting_for_confirm)

    router.message.register(start_message, Command('start'))
    router.message.register(help_message, Command('help'))
    router.message.register(enter_product_name, F.text == "Добавить объявление")
    router.message.register(all_messages)

    logging.info('Message handlers registered.')
