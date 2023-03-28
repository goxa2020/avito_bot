from aiogram import types
from loader import db


async def send_user_ads(message: types.Message):
    user_ads = db.get_user_ads(message.from_user.id)
    print(user_ads)
    text = 'Ваши объявления:'
    await message.answer(text)
    # TODO: ДОДЕЛАЙ БЛИН ФУНКЦИЮ
