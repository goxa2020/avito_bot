# import logging

from aiogram.utils import executor
from message_handlers.register_message_handlers import register_handlers
from callback_query_handlers.register_callback_query_handlers import register_callback_query_handlers
from pre_checkout_query_handlers.register_pre_checkout_query_handlers import register_pre_checkout_query_handlers
from loader import dp, session


async def on_start(_):
    """
    Функция вызывается при старте бота
    """
    register_handlers(dp)  # Регистрируем message handler`ы
    register_callback_query_handlers(dp)  # Регистрируем callback handler`ы
    register_pre_checkout_query_handlers(dp)


async def on_shutdown(_):
    """
    Функция вызывается при закрытии бота
    """
    session.close()  # Выключаем базу данных


if __name__ == '__main__':
    # try:
    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown)  # Запускаем бота
    # except Exception as e:
    #
    #     logging.error(e)
