from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from admin import *
from markups import mainMenu
from loader import bot, db, dp


class Add_ad(StatesGroup):
    waiting_for_name = State()
    waiting_for_product_name = State()
    waiting_for_product_amount = State()
    waiting_for_product_price = State()
    waiting_for_town = State()
    waiting_for_picture = State()


async def start_on(_):
    pass


@dp.callback_query_handler(text_contains="callDelAdm_")
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    del_id = callback_query.data.split("_")[1]
    admin_name = db.get_admin_name(del_id)
    await bot.edit_message_text(f'Точно удалить {admin_name}', callback_query.from_user.id,
                                callback_query.message.message_id, reply_markup=accept_del_kb(admin_name, del_id))


@dp.callback_query_handler(text_contains="acceptCallDelAdm_")
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    del_id = callback_query.data.split("_")[1]
    try:
        if db.user_is_admin(del_id):
            db.del_admin(del_id)
    except Exception:
        await bot.edit_message_text('Что-то не получилось', callback_query.from_user.id,
                                    callback_query.message.message_id)
        await bot.send_message(user_id, my_admins_text(user_id), reply_markup=my_admins_kb(user_id))
    else:
        await bot.edit_message_text(f'Человек успешно лишён админки \n{my_admins_text(user_id)}',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=my_admins_kb(user_id))
        await bot.send_message(del_id, 'Вас лишили прав администратора')


@dp.callback_query_handler(text_contains="cancelCallDelAdm_")
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    await bot.edit_message_text(f'Действие отменено \n{my_admins_text(user_id)}',
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=my_admins_kb(user_id))


async def ad_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(f'{message.from_user.first_name}')
    keyboard.add(btn)
    await message.answer("Введите своё имя:", reply_markup=keyboard)
    await Add_ad.waiting_for_name.set()


async def name_entered(message: types.Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await OrderFood.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


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
        elif message.text == "Назад":
            await message.answer('Вы вернулись назад', reply_markup=mainMenu(is_admin))
        elif message.text == "Добавить объявление":
            await ad_start(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_on)
