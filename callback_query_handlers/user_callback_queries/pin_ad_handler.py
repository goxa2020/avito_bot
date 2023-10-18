from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from callback_query_handlers.user_callback_queries.show_ad_to_user import show_ad_to_user
from config import yookassa_token
from datatypes import Ad
from loader import bot, session


async def pin_ad_handler(callback_query: CallbackQuery):
    await callback_query.answer('Функция не готова')

    ad_index = callback_query.data.split('_')[1]

    text = 'Поместить ваше объявление в "Закреплённые" стоит 100 руб. \n' \
           'Если вы удалите объявление, деньги не будут возвращены \n' \
           'Вы согласны?'

    inline_btn1 = InlineKeyboardButton(text='Подтвердить', callback_data=f'confirmPinAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(text='Назад', callback_data=f'cancelPinAd_{ad_index}')
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_btn1, inline_btn2]])

    # await bot.send_message(callback_query.from_user.id, text, reply_markup=inline_kb)
    await bot.edit_message_caption(callback_query.message.chat.id, callback_query.message.message_id, caption=text, reply_markup=inline_kb)


async def confirm_pin_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split('_')[1])
    ad = session.query(Ad).filter(Ad.posted)[ad_index]

    await bot.send_invoice(chat_id=callback_query.from_user.id,
                           title='Закреп сообщения',
                           description='Тестовое описание товара',
                           payload=f'month_sub_{ad.ad_id}',
                           provider_token=yookassa_token,
                           currency='RUB',
                           start_parameter='test_bot',
                           prices=[{'label': 'руб',
                                    'amount': 10000}])


async def cancel_pin_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split('_')[1])

    await show_ad_to_user(callback_query.from_user.id, ad_index, False, callback_query.message.message_id)
