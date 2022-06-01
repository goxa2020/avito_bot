import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from admin import *
from markups import *
from loader import bot, db, dp
from callback_handlers import *


class Add_ad(StatesGroup):
    waiting_for_name = State()
    waiting_for_product_name = State()
    waiting_for_product_amount = State()
    waiting_for_product_price = State()
    waiting_for_town = State()
    waiting_for_picture = State()
    waiting_for_accept = State()


ad_dict = {}


class Ad:
    def __init__(self, name):
        self.name = name
        self.product_name = None
        self.product_amount = None
        self.product_price = None
        self.town = None
        self.picture_id = None


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(name_entered, state=Add_ad.waiting_for_name)
    dp.register_message_handler(product_name_chosen, state=Add_ad.waiting_for_product_name)
    dp.register_message_handler(product_amount_chosen, state=Add_ad.waiting_for_product_amount)
    dp.register_message_handler(product_price_chosen, state=Add_ad.waiting_for_product_price)
    dp.register_message_handler(town_chosen, state=Add_ad.waiting_for_town)
    dp.register_message_handler(picture_chosen, state=Add_ad.waiting_for_picture, content_types=['text', 'photo'])
    dp.register_message_handler(accept_chosen, state=Add_ad.waiting_for_accept)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    is_admin = db.user_is_admin(message.from_user.id)
    await message.answer("Действие отменено", reply_markup=mainMenu(is_admin))


async def start_on(_):
    register_handlers(dp)


async def ad_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(f'{message.from_user.first_name}')
    btn2 = KeyboardButton('Отмена')
    keyboard.add(btn1).add(btn2)
    await message.answer("Введите своё имя:", reply_markup=keyboard)
    await Add_ad.first()


async def name_entered(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    name = message.text
    ad = Ad(name)
    ad_dict[chat_id] = ad
    await message.answer("Введите название товара:", reply_markup=cancel_kb())
    await Add_ad.next()


async def product_name_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    product_name = message.text
    ad = ad_dict[chat_id]
    ad.product_name = product_name
    await message.answer("Введите количество:", reply_markup=cancel_kb())
    await Add_ad.next()


async def product_amount_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    product_amount = message.text
    ad = ad_dict[chat_id]
    ad.product_amount = product_amount
    await message.answer("Введите цену:", reply_markup=cancel_kb())
    await Add_ad.next()


async def product_price_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    product_price = message.text
    ad = ad_dict[chat_id]
    ad.product_price = product_price
    await state.update_data(product_price=message.text)
    await message.answer("Введите свой город:", reply_markup=cancel_kb())
    await Add_ad.next()


async def town_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    town = message.text
    ad = ad_dict[chat_id]
    ad.town = town
    await state.update_data(town=message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Нет", "Отмена")
    await message.answer('Теперь ты отправь фотогравию товора, если её нет, нажми "Нет"', reply_markup=keyboard)
    await Add_ad.next()


async def picture_chosen(message: types.Message):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    if message.content_type == 'photo':
        chat_id = message.from_user.id
        picture = message.photo[0].file_id
        ad = ad_dict[chat_id]
        ad.picture_id = picture
        await bot.send_photo(chat_id=message.from_user.id, photo=picture)
        await bot.send_message(chat_id, "Подтверди плиз", reply_markup=accept_ad_kb())
        await Add_ad.next()
    elif message.content_type == 'text':
        if message.text == "Нет":
            await message.answer("Окей, без фотки обойдёмся\nПодтверди плиз", reply_markup=accept_ad_kb())
            await Add_ad.next()
        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add("Нет", "Отмена")
            await message.answer("Мне нужна фотогравия", reply_markup=keyboard)


async def accept_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await state.finish()
        chat_id = message.from_user.id
        ad = ad_dict[chat_id]
        print(ad)
        is_admin = db.user_is_admin(message.from_user.id)
        await bot.send_message(chat_id, f'Всё отлично', reply_markup=mainMenu(is_admin))
    elif message.text == 'Отмена':
        await cancel(message, state)
    else:
        await message.answer('Пользуйся клавиатурой')


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        admin_invite = bool(len(message.text[:6:-1]))
        is_admin = db.user_is_admin(message.from_user.id)
        if admin_invite:
            if is_admin:
                await message.answer('Вы и так уже админ', reply_markup=mainMenu(is_admin))
            else:
                await message.answer('Поздравляю, теперь вы админ', reply_markup=mainMenu(True))
                await bot.send_message(message.text[:6:-1], f'Через вашу ссылку человек '
                                                            f'({message.from_user.first_name}) получил права админа')
                db.add_admin(message.from_user.id, message.text[:6:-1], message.from_user.first_name)
        elif db.user_exists(message.from_user.id):
            await message.answer('Давно не виделись', reply_markup=mainMenu(is_admin))
        else:
            await message.answer('Привет, приятно познакомиться\n'
                                 'Я бот для добавления объявлений на канал',
                                 reply_markup=mainMenu(is_admin))
            db.add_user(message.from_user.id)


@dp.message_handler(content_types=['text'])
async def all_messages(message: types.Message):
    if message.chat.type == 'private':
        is_admin = db.user_is_admin(message.from_user.id)
        if message.text == 'Добавить админа':
            if db.user_is_admin(message.from_user.id):
                await admin_ref(message)
            else:
                await message.answer('Вы не имеете доступа к этой команде')
        elif message.text == 'Мои админы':
            if is_admin:
                await bot.send_message(message.from_user.id, my_admins_text(message.from_user.id),
                                       reply_markup=my_admins_kb(message.from_user.id))
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(is_admin))
        elif message.text == 'Управление админами':
            if is_admin:
                await message.answer('Управление:', reply_markup=adminMenuProfile())
            else:
                await message.answer('У вас нет доступа к этой команде', mainMenu(is_admin))
        elif message.text == "Назад" or message.text == "Отмена":
            await message.answer('Вы вернулись назад', reply_markup=mainMenu(is_admin))
        elif message.text == "Добавить объявление":
            await ad_start(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_on)
