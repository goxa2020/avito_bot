import logging

from aiogram.dispatcher import Dispatcher
from callback_query_handlers.admin_menu_callback_queries.delete_admin_handler import delete_admin, confirm_delete_admin, cancel_delete_admin
from callback_query_handlers.admin_menu_callback_queries.publish_ad_handler import publish_ad, confirm_publish_ad, cancel_publish_ad
from callback_query_handlers.admin_menu_callback_queries.detele_ad_handler import delete_ad, confirm_delete_ad, cancel_delete_ad
from callback_query_handlers.admin_menu_callback_queries.show_ad_to_admin_handler import show_ad_to_admin
from callback_query_handlers.user_callback_queries.delete_my_ad_handler import delete_users_ad, confirm_delete_users_ad
from callback_query_handlers.user_callback_queries.show_ad_to_user_handler import show_ad_to_user_handler
from callback_query_handlers.user_callback_queries.pin_ad_handler import pin_ad_handler


def register_callback_query_handler(dispatcher: Dispatcher):

    dispatcher.register_callback_query_handler(delete_admin, text_contains="callDelAdm")
    dispatcher.register_callback_query_handler(confirm_delete_admin, text_contains="confirmCallDelAdm")
    dispatcher.register_callback_query_handler(cancel_delete_admin, text_contains="cancelCallDelAdm")

    dispatcher.register_callback_query_handler(publish_ad, text_contains="publishAd")
    dispatcher.register_callback_query_handler(confirm_publish_ad, text_contains="confirmPublishAd")
    dispatcher.register_callback_query_handler(cancel_publish_ad, text_contains="cancelPublishAd")

    dispatcher.register_callback_query_handler(delete_ad, text_contains="deleteAd")
    dispatcher.register_callback_query_handler(confirm_delete_ad, text_contains="confirmDelAd")
    dispatcher.register_callback_query_handler(cancel_delete_ad, text_contains="cancelDelAd")

    dispatcher.register_callback_query_handler(show_ad_to_admin, text_contains="showAd")

    dispatcher.register_callback_query_handler(show_ad_to_user_handler, text_contains="showUsersAd")

    dispatcher.register_callback_query_handler(delete_users_ad, text_contains="deleteUsersAd")
    dispatcher.register_callback_query_handler(confirm_delete_users_ad, text_contains="confirmDeleteUsersAd")

    dispatcher.register_callback_query_handler(pin_ad_handler, text_contains="pinAd")

    logging.info('Callback query handlers registered.')
