from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from config import Bot_name, no_photo
from loader import db, bot
from markups import mainMenu


async def admin_ref(message: types.Message):
    await message.answer(f'Твоя ссылка для назначения админа⬇\n'
                         f'https://t.me/{Bot_name}?start=adm{str(message.from_user.id)[::-1]}\n'
                         f'Человек должен перейти по ней и нажать "Старт", чтобы стать админом\n'
                         f'Будь осторожен, не передовай эту ссылку неизвестным людям')


def adminMenuProfile() -> ReplyKeyboardMarkup():
    admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Добавить админа')
    btn2 = KeyboardButton('Мои админы')
    btn3 = KeyboardButton('Назад')
    admin_menu.add(btn1).add(btn2).add(btn3)
    return admin_menu


def my_admins_text(user_id: int) -> str:
    admins = db.get_admins()
    my_admins = [admin[0] for admin in admins if int(admin[1]) == user_id]
    my_admins_names = [admin[2] for admin in admins if admin[0] in my_admins]
    if len(my_admins) > 0:
        text = 'Админы, добавленные вами:\n'
        for i in range(len(my_admins)):
            text += f'{i + 1}: {my_admins_names[i]}, ID: {my_admins[i]}\n'
    else:
        text = 'У вас нет ниодного добавленного админа'
    return text


def my_admins_kb(user_id) -> InlineKeyboardMarkup():
    admins = db.get_admins()
    my_admins = [admin[0] for admin in admins if int(admin[1]) == user_id]
    my_admins_names = [admin[2] for admin in admins if admin[0] in my_admins]
    inline_kb = InlineKeyboardMarkup()
    for name in my_admins_names:
        inline_btn = InlineKeyboardButton(f'Лишить админки {name}',
                                          callback_data=f'callDelAdm_{my_admins[my_admins_names.index(name)]}')
        inline_kb.add(inline_btn)
    return inline_kb


def confirm_del_admin_kb(admin_id) -> InlineKeyboardMarkup():
    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'confirmCallDelAdm_{admin_id}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelCallDelAdm_{admin_id}')
    inline_kb.add(inline_btn1).add(inline_btn2)
    return inline_kb


async def show_ad(user_id, ad_index=None):
    ad_index = ad_index or 0

    ads = db.get_not_posted_ads()
    print(ads)

    if not len(ads):
        return await bot.send_message(user_id, 'Нет объявлений на рассмотрении', reply_markup=mainMenu(user_id))

    ad_index = int(ad_index % len(ads))

    ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {len(ads)}\n" \
           f"Имя: {ad[1]}\n" \
           f"Название товара: {ad[2]}\n" \
           f"Количество: {ad[3]}\n" \
           f"Цена: {ad[4]}\n" \
           f"Город: {ad[5]}\n" \
           f"Описание: {ad[7]}\n"

    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'showAd_{ad_index - 1}')
    inline_btn2 = InlineKeyboardButton('Следующее объявление', callback_data=f'showAd_{ad_index + 1}')
    inline_btn3 = InlineKeyboardButton('Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn4 = InlineKeyboardButton('Опубликовать', callback_data=f'publishAd_{ad_index}')

    if len(ads) > 1:
        inline_kb.row(inline_btn1, inline_btn2)
    inline_kb.row(inline_btn3, inline_btn4)

    if ad[8]:
        return await bot.send_photo(chat_id=user_id, photo=ad[8], caption=text, reply_markup=inline_kb)

    return await bot.send_photo(chat_id=user_id, photo=no_photo, caption=text, reply_markup=inline_kb)
