from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import no_photo_id, Bot_name
from datatypes import User, Ad
from loader import bot, session
from markups import mainMenu


async def not_access(user_id):
    return await bot.send_message(user_id, 'У вас нет доступа к этой команде', reply_markup=mainMenu(user_id))


def add_admin_text(user_id):
    return f'Твоя ссылка для назначения админа⬇\n' \
           f'https://t.me/{Bot_name}?start=adm{str(user_id)[::-1]}\n' \
           f'Человек должен перейти по ней и нажать "Старт", чтобы стать админом\n' \
           f'Будь осторожен, не передовай эту ссылку неизвестным людям'


def admin_menu_profile() -> ReplyKeyboardMarkup():
    admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Добавить админа')
    btn2 = KeyboardButton('Мои админы')
    btn3 = KeyboardButton('Назад')
    admin_menu.add(btn1).add(btn2).add(btn3)
    return admin_menu


def my_admins_text(user_id: int) -> str:
    admins = session.query(User).filter(User.is_admin)
    my_admins = [admin for admin in admins if int(admin.admin_inviter_id) == user_id]
    my_admins_names = [admin.user_first_name for admin in my_admins]
    if len(my_admins) > 0:
        text = 'Админы, добавленные вами:\n'
        for i in range(len(my_admins)):
            text += f'{i + 1}: {my_admins_names[i]}, ID: {my_admins[i].user_id}\n'
    else:
        text = 'У вас нет ниодного добавленного админа'
    return text


def my_admins_kb(user_id) -> InlineKeyboardMarkup():
    admins = session.query(User).filter(User.is_admin)
    my_admins = [admin.user_id for admin in admins if int(admin.admin_inviter_id) == user_id]
    my_admins_names = [admin.user_first_name for admin in my_admins]
    inline_kb = InlineKeyboardMarkup()
    for name in my_admins_names:
        inline_btn = InlineKeyboardButton(f'Лишить админки {name}',
                                          callback_data=f'callDelAdm_{my_admins[my_admins_names.index(name)]}')
        inline_kb.add(inline_btn)
    return inline_kb


async def show_ad(user_id, ad_index=None):
    ad_index = ad_index or 0

    non_posted_ads = session.query(Ad).filter(Ad.posted == False)
    print(non_posted_ads.count())
    if not non_posted_ads.count():
        return await bot.send_message(user_id, 'Нет объявлений на рассмотрении', reply_markup=mainMenu(user_id))

    ad_index = int(ad_index % non_posted_ads.count())

    ad = non_posted_ads[ad_index]

    text = f"Объявление {ad_index + 1} из {non_posted_ads.count()}\n" \
           f"Имя: {ad.user_first_name}\n" \
           f"Название товара: {ad.product_name}\n" \
           f"Количество: {ad.amount}\n" \
           f"Цена: {ad.price}\n" \
           f"Город: {ad.town}\n" \
           f"Описание: {ad.description}\n"

    inline_kb = InlineKeyboardMarkup()

    inline_btn3 = InlineKeyboardButton('Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn4 = InlineKeyboardButton('Опубликовать', callback_data=f'publishAd_{ad_index}')

    if non_posted_ads.count() > 1:
        inline_btn1 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'showAd_{ad_index - 1}')
        inline_btn2 = InlineKeyboardButton('Следующее объявление', callback_data=f'showAd_{ad_index + 1}')
        inline_kb.row(inline_btn1, inline_btn2)

    inline_kb.row(inline_btn3, inline_btn4)

    if ad.picture_id:
        return await bot.send_photo(chat_id=user_id, photo=ad.picture_id, caption=text, reply_markup=inline_kb)

    return await bot.send_photo(chat_id=user_id, photo=no_photo_id, caption=text, reply_markup=inline_kb)
