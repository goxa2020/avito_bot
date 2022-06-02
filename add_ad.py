import logging
from loader import dp, db, bot
from markups import *
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


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


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=mainMenu(message.from_user.id))


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
        await bot.send_message(chat_id, f'Всё отлично', reply_markup=mainMenu(message.from_user.id))
    elif message.text == 'Отмена':
        await cancel(message, state)
    else:
        await message.answer('Пользуйся клавиатурой')