from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import no_photo_id, Bot_name
from datatypes import User, Ad
from loader import bot, session
from markups import mainMenu


async def send_to_admins(text: str):
    admins = session.query(User).filter(User.is_admin).all()
    for admin in admins:
        await bot.send_message(admin.user_id, text=text)


async def not_access(user_id):
    return await bot.send_message(user_id, 'У вас нет доступа к этой команде', reply_markup=mainMenu(user_id))


def add_admin_text(user_id):
    return f'Твоя ссылка для назначения админа⬇\n' \
           f'https://t.me/{Bot_name}?start=adm{str(user_id)[::-1]}\n' \
           f'Человек должен перейти по ней и нажать "Старт", чтобы стать админом\n' \
           f'Будь осторожен, не передовай эту ссылку неизвестным людям'


def admin_menu_profile() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='Добавить админа')
    btn2 = KeyboardButton(text='Мои админы')
    btn3 = KeyboardButton(text='Назад')
    admin_menu = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3]], resize_keyboard=True)
    return admin_menu


def my_admins_text(user_id: int) -> str:
    admins: list[User] = session.query(User).filter(User.is_admin)
    my_admins = [admin for admin in admins if int(admin.admin_inviter_id) == user_id]
    if len(my_admins) > 0:
        text = 'Админы, добавленные вами:\n'
        for i in range(len(my_admins)):
            text += f'{i + 1}: {my_admins[i].user_first_name}, ID: {my_admins[i].user_id}\n'
    else:
        text = 'У вас нет ниодного добавленного админа'
    return text


def my_admins_kb(user_id) -> InlineKeyboardMarkup:
    admins = session.query(User).filter(User.is_admin)
    my_admins = [admin for admin in admins if int(admin.admin_inviter_id) == user_id]
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])
    for admin in my_admins:
        inline_btn = InlineKeyboardButton(text=f'Лишить админки {admin.user_first_name}',
                                          callback_data=f'callDelAdm_{admin.user_id}')
        inline_kb.inline_keyboard.append([inline_btn])
    return inline_kb


async def show_ad(user_id, ad_index=None):
    ad_index = ad_index or 0

    non_posted_ads = session.query(Ad).filter(Ad.posted == False)
    if not non_posted_ads.count():
        return await bot.send_message(user_id, 'Нет объявлений на рассмотрении', reply_markup=mainMenu(user_id))

    ad_index = int(ad_index % non_posted_ads.count())

    ad = non_posted_ads[ad_index]

    text = f"Объявление {ad_index + 1} из {non_posted_ads.count()}\n" \
           f"Имя: {ad.owner.user_first_name}\n" \
           f"Название товара: {ad.product_name}\n" \
           f"Количество: {ad.amount}\n" \
           f"Цена: {ad.price}\n" \
           f"Город: {ad.town}\n" \
           f"Описание: {ad.description}\n"

    inline_btn3 = InlineKeyboardButton(text='Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn4 = InlineKeyboardButton(text='Опубликовать', callback_data=f'publishAd_{ad_index}')

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    if non_posted_ads.count() > 1:
        inline_btn1 = InlineKeyboardButton(text='Предыдущее объявление', callback_data=f'showAd_{ad_index - 1}')
        inline_btn2 = InlineKeyboardButton(text='Следующее объявление', callback_data=f'showAd_{ad_index + 1}')
        inline_kb.inline_keyboard.append([inline_btn1, inline_btn2])

    inline_kb.inline_keyboard.append([inline_btn3, inline_btn4])

    if ad.picture_id:
        return await bot.send_photo(chat_id=user_id, photo=ad.picture_id, caption=text, reply_markup=inline_kb)

    return await bot.send_photo(chat_id=user_id, photo=no_photo_id, caption=text, reply_markup=inline_kb)
