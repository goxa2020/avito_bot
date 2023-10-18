# Это конечный автомат для добавления объявлений
__all__ = ('Add_ad', 'enter_product_name', 'product_name_chosen', 'product_amount_chosen', 'product_price_chosen',
           'town_chosen', 'picture_chosen', 'description_chosen', 'confirm_chosen', 'cancel')
# import logging
from datatypes import Ad, User
from loader import session, bot
from markups import mainMenu, cancel_kb, no_or_cancel_kb
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Add_ad(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_product_amount = State()
    waiting_for_product_price = State()
    waiting_for_town = State()
    waiting_for_picture = State()
    waiting_for_description = State()
    waiting_for_confirm = State()


ad_dict = {}


async def cancel(message: types.Message, state: FSMContext):
    await state.set_state(state=None)
    await message.answer("Действие отменено", reply_markup=mainMenu(message.from_user.id))


async def enter_product_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = session.query(User).filter(User.user_id == user_id).first()
    ad = Ad(owner=user, user_id=user.id)
    ad_dict[user_id] = ad
    await message.answer("Введите название товара:", reply_markup=cancel_kb())
    await state.set_state(Add_ad.waiting_for_product_name)


async def product_name_chosen(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    product_name = message.text
    ad = ad_dict[chat_id]
    ad.product_name = product_name
    await message.answer("Введите количество:", reply_markup=cancel_kb())
    await state.set_state(Add_ad.waiting_for_product_amount)


async def product_amount_chosen(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        chat_id = message.from_user.id
        product_amount = message.text
        ad = ad_dict[chat_id]
        ad.amount = product_amount
        await message.answer("Введите цену в рублях:", reply_markup=cancel_kb())
        await state.set_state(Add_ad.waiting_for_product_price)
    else:
        await message.answer('Это должно быть число', reply_markup=cancel_kb())


async def product_price_chosen(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        chat_id = message.from_user.id
        product_price = message.text
        ad = ad_dict[chat_id]
        ad.price = product_price
        await message.answer("Введите свой город:", reply_markup=cancel_kb())
        await state.set_state(Add_ad.waiting_for_town)
    else:
        await message.answer('Это должно быть число', reply_markup=cancel_kb())


async def town_chosen(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    town = message.text
    ad = ad_dict[chat_id]
    ad.town = town
    await message.answer('Теперь ты отправь фотогравию товора, если её нет, нажми "Нет"', reply_markup=no_or_cancel_kb())
    await state.set_state(Add_ad.waiting_for_picture)


async def picture_chosen(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    ad = ad_dict[chat_id]
    if message.content_type == 'photo':
        ad.picture_id = message.photo[0].file_id

        await message.answer(f'Отлично, теперь отправь описание товара', reply_markup=cancel_kb())

        await state.set_state(Add_ad.waiting_for_description)
    elif message.content_type == 'text':
        if message.text == "Нет":
            await message.answer(f'Окей, без фотки обойдёмся\n'
                                 f'Отправь описание товара', reply_markup=cancel_kb())
            await state.set_state(Add_ad.waiting_for_description)
        else:
            await message.answer("Мне нужна фотогравия", reply_markup=no_or_cancel_kb())
    else:
        await message.answer("Мне нужна фотогравия", reply_markup=no_or_cancel_kb())


async def description_chosen(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    ad = ad_dict[chat_id]
    ad.description = message.text

    btn1 = KeyboardButton(text='Подтвердить')
    btn2 = KeyboardButton(text='Отмена')
    keyboard = ReplyKeyboardMarkup(keyboard=[[btn1, btn2]], resize_keyboard=True, one_time_keyboard=True)

    await message.answer(f'Подтвердите пожалуйста\n'
                         f'Название товара: {ad.product_name}\n'
                         f'Количество товара: {ad.amount}\n'
                         f'Цена: {ad.price}\n'
                         f'Город: {ad.town}\n'
                         f'Описание: {ad.description}', reply_markup=keyboard)

    await state.set_state(Add_ad.waiting_for_confirm)


async def confirm_chosen(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await state.set_state(state=None)
        chat_id = message.from_user.id
        ad = ad_dict[chat_id]
        session.add(ad)
        session.commit()
        return await bot.send_message(chat_id, f'Всё отлично', reply_markup=mainMenu(message.from_user.id))
    await message.answer('Пользуйся клавиатурой')
