from aiogram import Router

from pre_checkout_query_handlers.pre_checkout_query_handler import process_pre_checkout_query


def register_pre_checkout_query_handlers(router: Router):
    router.pre_checkout_query.register(process_pre_checkout_query)
