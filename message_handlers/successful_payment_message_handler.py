from aiogram import types

from config import chanel_name
from datatypes import Ad
from loader import session, bot


async def process_pay(message: types.Message):
    if 'month_sub' in message.successful_payment.invoice_payload:
        ad_id = message.successful_payment.invoice_payload.split('_')[2]
        ad: Ad = session.query(Ad).filter(Ad.ad_id == ad_id).first()
        await message.answer('Объявление успешно закреплено))\n'
                             'Спасоби за покупку')
        await bot.pin_chat_message(chanel_name, ad.post_id, True)

        ad.is_pinned = True
        session.commit()


