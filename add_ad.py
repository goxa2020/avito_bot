# Это конечный автомат для добавления объявлений

# import logging
from loader import db, bot
from markups import *
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Add_ad(StatesGroup):
    waiting_for_name = State()
    waiting_for_product_name = State()
    waiting_for_product_amount = State()
    waiting_for_product_price = State()
    waiting_for_town = State()
    waiting_for_picture = State()
    waiting_for_description = State()
    waiting_for_confirm = State()


ad_dict = {}


class Ad:
    def __init__(self, name):
        self.name = name
        self.product_name = None
        self.product_amount = None
        self.product_price = None
        self.town = None
        self.picture_id = None
        self.description = None


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
    if message.text.isdigit():
        chat_id = message.from_user.id
        product_amount = message.text
        ad = ad_dict[chat_id]
        ad.product_amount = product_amount
        await message.answer("Введите цену в рублях:", reply_markup=cancel_kb())
        await Add_ad.next()
    else:
        await message.answer('Это должно быть число', reply_markup=cancel_kb())


async def product_price_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    if message.text.isdigit():
        chat_id = message.from_user.id
        product_price = message.text
        ad = ad_dict[chat_id]
        ad.product_price = product_price
        await message.answer("Введите свой город:", reply_markup=cancel_kb())
        await Add_ad.next()
    else:
        await message.answer('Это должно быть число', reply_markup=cancel_kb())


async def town_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    town = message.text
    ad = ad_dict[chat_id]
    ad.town = town
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Нет", "Отмена")
    await message.answer('Теперь ты отправь фотогравию товора, если её нет, нажми "Нет"', reply_markup=keyboard)
    await Add_ad.next()


async def picture_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    if message.content_type == 'photo':
        chat_id = message.from_user.id
        ad = ad_dict[chat_id]
        ad.picture_id = message.photo[0].file_id

        await message.answer(f'Отлично, теперь отправь описание товара', reply_markup=cancel_kb())

        await Add_ad.next()
    elif message.content_type == 'text':
        if message.text == "Нет":
            # chat_id = message.from_user.id
            # ad = ad_dict[chat_id]
            await message.answer(f'Окей, без фотки обойдёмся\n'
                                 f'Отправь описание товара', reply_markup=cancel_kb())
            await Add_ad.next()
        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add("Нет", "Отмена")
            await message.answer("Мне нужна фотогравия", reply_markup=keyboard)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Нет", "Отмена")
        await message.answer("Мне нужна фотогравия", reply_markup=keyboard)


async def description_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await cancel(message, state)
        return
    chat_id = message.from_user.id
    ad = ad_dict[chat_id]
    ad.description = message.text

    await message.answer(f'Подтвердите пожалуйста\n'
                         f'Имя: {ad.name}\n'
                         f'Название товара: {ad.product_name}\n'
                         f'Количество товара: {ad.product_amount}\n'
                         f'Цена: {ad.product_price}\n'
                         f'Город: {ad.town}\n'
                         f'Описание: {ad.description}', reply_markup=confirm_ad_kb())

    await Add_ad.next()


async def confirm_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await state.finish()
        chat_id = message.from_user.id
        ad = ad_dict[chat_id]
        db.add_ad(message.from_user.mention, ad.product_name, ad.product_amount,
                  ad.product_price, ad.town, ad.picture_id, message.from_user.id, ad.description)
        await bot.send_message(chat_id, f'Всё отлично', reply_markup=mainMenu(message.from_user.id))
    elif message.text == 'Отмена':
        await cancel(message, state)
    else:
        await message.answer('Пользуйся клавиатурой')
