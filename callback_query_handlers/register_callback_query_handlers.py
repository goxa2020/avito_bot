import logging

from aiogram import Router, F
from callback_query_handlers.admin_menu_callback_queries.delete_admin_handler import delete_admin, confirm_delete_admin, cancel_delete_admin
from callback_query_handlers.admin_menu_callback_queries.publish_ad_handler import publish_ad, confirm_publish_ad, cancel_publish_ad
from callback_query_handlers.admin_menu_callback_queries.detele_ad_handler import delete_ad, confirm_delete_ad, cancel_delete_ad
from callback_query_handlers.admin_menu_callback_queries.show_ad_to_admin_handler import show_ad_to_admin
from callback_query_handlers.user_callback_queries.delete_my_ad_handler import delete_users_ad, confirm_delete_users_ad
from callback_query_handlers.user_callback_queries.show_ad_to_user_handler import show_ad_to_user_handler
from callback_query_handlers.user_callback_queries.pin_ad_handler import pin_ad_handler, confirm_pin_ad, cancel_pin_ad


def register_callback_query_handlers(router: Router):

    router.callback_query.register(delete_admin, F.data.contains("callDelAdm"))
    router.callback_query.register(confirm_delete_admin, F.data.contains("confirmCallDelAdm"))
    router.callback_query.register(cancel_delete_admin, F.data.contains("cancelCallDelAdm"))

    router.callback_query.register(publish_ad, F.data.contains("publishAd"))
    router.callback_query.register(confirm_publish_ad, F.data.contains("confirmPublishAd"))
    router.callback_query.register(cancel_publish_ad, F.data.contains("cancelPublishAd"))

    router.callback_query.register(delete_ad, F.data.contains("deleteAd"))
    router.callback_query.register(confirm_delete_ad, F.data.contains("confirmDelAd"))
    router.callback_query.register(cancel_delete_ad, F.data.contains("cancelDelAd"))

    router.callback_query.register(show_ad_to_admin, F.data.contains("showAd"))

    router.callback_query.register(show_ad_to_user_handler, F.data.contains("showUsersAd"))

    router.callback_query.register(delete_users_ad, F.data.contains("deleteUsersAd"))
    router.callback_query.register(confirm_delete_users_ad, F.data.contains("confirmDeleteUsersAd"))

    router.callback_query.register(pin_ad_handler, F.data.contains("pinAd"))
    router.callback_query.register(confirm_pin_ad, F.data.contains("confirmPinAd"))
    router.callback_query.register(cancel_pin_ad, F.data.contains("cancelPinAd"))

    logging.info('Callback query handlers registered.')
