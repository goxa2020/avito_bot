import logging

from aiogram.dispatcher import Dispatcher
from callback_query_handlers.admin_menu_callback_queries.delete_admin import delete_admin, confirm_delete_admin, cancel_delete_admin
from callback_query_handlers.admin_menu_callback_queries.publish_ad import publish_ad, confirm_publish_ad, cancel_publish_ad
from callback_query_handlers.admin_menu_callback_queries.detele_ad import delete_ad, confirm_delete_ad, cancel_delete_ad
from callback_query_handlers.admin_menu_callback_queries.show_ad import show_ad
from callback_query_handlers.user_callback_queries.show_ad_to_user_handler import show_ad_to_user


def register_callback_query_handler(dispatcher: Dispatcher):

    dispatcher.register_callback_query_handler(delete_admin, text_contains=["callDelAdm_"])
    dispatcher.register_callback_query_handler(confirm_delete_admin, text_contains=["confirmCallDelAdm_"])
    dispatcher.register_callback_query_handler(cancel_delete_admin, text_contains=["cancelCallDelAdm_"])

    dispatcher.register_callback_query_handler(publish_ad, text_contains=["publishAd_"])
    dispatcher.register_callback_query_handler(confirm_publish_ad, text_contains=["confirmPublishAd_"])
    dispatcher.register_callback_query_handler(cancel_publish_ad, text_contains=["cancelPublishAd"])

    dispatcher.register_callback_query_handler(delete_ad, text_contains=["deleteAd_"])
    dispatcher.register_callback_query_handler(confirm_delete_ad, text_contains=["confirmDelAd_"])
    dispatcher.register_callback_query_handler(cancel_delete_ad, text_contains=["cancelDelAd"])

    dispatcher.register_callback_query_handler(show_ad, text_contains="showAd_")

    dispatcher.register_callback_query_handler(show_ad_to_user, text_contains="show_ad_to_user")

    logging.info('Callback query handlers registered.')
