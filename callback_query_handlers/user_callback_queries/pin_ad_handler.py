from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot


async def pin_ad_handler(callback_query: CallbackQuery):
    await callback_query.answer('Функция не готова')

    text = 'Поместить ваше объявление в "Закреплённые" стоит 100 руб. \n' \
           'Если вы удалите объявление, деньги не будут возвращены \n' \
           'Вы согласны?'

    inline_kb = InlineKeyboardMarkup()

    inline_btn1 = InlineKeyboardButton('Подтвердить', callback_data='')
    inline_btn2 = InlineKeyboardButton('Отмена', callback_data='')

    inline_kb.row(inline_btn1, inline_btn2)
    await bot.send_message(callback_query.from_user.id, text)
# TODO: Доделать
