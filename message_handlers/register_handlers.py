from add_ad import *


def register_handlers(dispatcher):
    """
    Это аналоги @dp.message_handler(), только собранные в одном месте
    """
    dispatcher.register_message_handler(name_entered, state=Add_ad.waiting_for_name)
    dispatcher.register_message_handler(product_name_chosen, state=Add_ad.waiting_for_product_name)
    dispatcher.register_message_handler(product_amount_chosen, state=Add_ad.waiting_for_product_amount)
    dispatcher.register_message_handler(product_price_chosen, state=Add_ad.waiting_for_product_price)
    dispatcher.register_message_handler(town_chosen, state=Add_ad.waiting_for_town)
    dispatcher.register_message_handler(picture_chosen, state=Add_ad.waiting_for_picture,
                                        content_types=['text', 'photo'])
    dispatcher.register_message_handler(description_chosen, state=Add_ad.waiting_for_description)
    dispatcher.register_message_handler(confirm_chosen, state=Add_ad.waiting_for_confirm)