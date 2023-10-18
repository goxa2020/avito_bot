import asyncio
import logging

from aiogram import Router

from admin import send_to_admins
from message_handlers.register_message_handlers import register_handlers
from callback_query_handlers.register_callback_query_handlers import register_callback_query_handlers
from pre_checkout_query_handlers.register_pre_checkout_query_handlers import register_pre_checkout_query_handlers
from loader import dp, session, bot


async def on_start(router: Router):
    """
    Функция вызывается при старте бота
    """
    register_handlers(router)  # Регистрируем message handler`ы
    register_callback_query_handlers(router)  # Регистрируем callback handler`ы
    register_pre_checkout_query_handlers(router)


async def on_shutdown():
    """
    Функция вызывается при закрытии бота
    """
    session.close()  # Выключаем базу данных
    logging.info('Database connection closed successfully')


async def main():
    logging.info('Starting the bot')

    await on_start(dp)
    await send_to_admins("Бот запущен")
    await dp.start_polling(bot)  # Запускаем бота
    await on_shutdown()

    logging.info('Bot is turned off')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(e)
