from aiogram.types import CallbackQuery

from callback_query_handlers.user_callback_queries.show_ad_to_user import show_ad_to_user


async def show_ad_to_user_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    ad_index, send_message = map(int, callback_query.data.split("_")[1::])

    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    await show_ad_to_user(user_id, ad_index, send_message, message_id)
