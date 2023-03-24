from aiogram.utils import executor
from message_handlers.register_handlers import register_handlers
from loader import db, dp
import callback_handlers


async def start_on(_):
    """
    Функция вызывается при старте бота
    """
    register_handlers(dp)  # Регистрируем message handler`ы


async def on_shutdown(_):
    """
    Функция вызывается при закрытии бота
    """
    db.close()  # Выключаем базу данных


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_on, on_shutdown=on_shutdown)  # Запускаем бота
