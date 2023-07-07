import logging

from aiogram.utils import executor
from message_handlers.register_message_handlers import register_handlers
from callback_query_handlers.register_callback_query_handlers import register_callback_query_handler
from loader import dp, session


async def on_start(_):
    """
    Функция вызывается при старте бота
    """
    register_handlers(dp)  # Регистрируем message handler`ы
    register_callback_query_handler(dp)  # Регистрируем callback handler`ы


async def on_shutdown(_):
    """
    Функция вызывается при закрытии бота
    """
    session.close()  # Выключаем базу данных


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown)  # Запускаем бота
    except Exception as e:
        pass
        logging.error(e)
# TODO: полностью перейти на SQLAlchemy, во всех файлах переписать работу с БД
