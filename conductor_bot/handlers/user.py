import emoji
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from time import sleep

from conductor_bot.config import User
from conductor_bot.keyboards.inline import main_menu, found_menu
from conductor_bot.misc.db import check_user_system, get_user_description
from conductor_bot.misc.states import UserState
from conductor_bot.models.users import bd_users


async def start_handler(message: Message):
    user_in_db = await check_user_system(message.chat.username)
    if user_in_db:
        await message.answer(
            text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'),
            reply_markup=main_menu)
        await UserState.user_in_system.set()
    else:
        await message.answer(emoji.emojize(":red_exclamation_mark: Вас нету в системе :locked_with_key:\nПредлагаем вам посетить наш сайт https://divarteam.ru"))



async def user_base_handler(message: Message):
    user_in_db = await check_user_system(message.chat.username)
    if user_in_db:
        await message.answer(
            text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'),
            reply_markup=main_menu)
        await UserState.user_in_system.set()
    else:
        await message.answer(emoji.emojize(":red_exclamation_mark: Вас нету в системе :locked_with_key:\nПредлагаем вам посетить наш сайт https://divarteam.ru"))

async def play_find_animation(call: CallbackQuery, tile = 0.2):
        await call.bot.edit_message_text(
            text=emoji.emojize("Идет поиск."),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id
            )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=found_menu
        )
        sleep(tile)
        await call.bot.edit_message_text(
            text=emoji.emojize("Идет поиск.."),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id
            )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=found_menu
        )
        sleep(tile)
        await call.bot.edit_message_text(
            text=emoji.emojize("Идет поиск..."),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id
            )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=found_menu
        )
        sleep(tile)
        await call.bot.edit_message_text(
            text=emoji.emojize("Режим ожидания включен :check_mark_button:"),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id
            )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=found_menu
        )

async def find_handler(call: CallbackQuery):
    # await call.bot.edit_message_text("Hello wordl", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=main_menu)
    curr_username = call.from_user.username
    curr_chat_id = call.from_user.id
    await bd_users.add_user(curr_username, curr_chat_id, curr_chat_id)
    await play_find_animation(call)
    
    if await bd_users.check_users(curr_username):
        friend: User = await bd_users.get_friend(curr_username)
        await call.bot.send_message(chat_id=curr_chat_id, text=get_user_description(friend.username))
        await bd_users.delete_user(call.from_user.username)
        await call.bot.send_message(chat_id=friend.chat_id, text=get_user_description(curr_username))
        await call.bot.edit_message_text(
            text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id)
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=main_menu
        )
    else:
        await call.answer("Пользователи не найдены!")
        await call.bot.edit_message_text(
            text=emoji.emojize("Режим ожидания включен :speaker_high_volume:"),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id
            )
        await call.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=found_menu
        )


async def cancel_handler(call: CallbackQuery):
    # await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await bd_users.delete_user(call.from_user.username)
    await call.bot.edit_message_text(
            text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'),
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            reply_markup=main_menu)


def register_user_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(find_handler, state=UserState.user_in_system, text="btnFind")
    dp.register_callback_query_handler(cancel_handler, state=UserState.user_in_system, text="btnCancel")
    dp.register_message_handler(start_handler, commands=["/start"], state="*")
    dp.register_message_handler(user_base_handler, state="*")