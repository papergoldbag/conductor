from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import emoji

from conductor_bot.models.users import bd_users
from conductor_bot.config import User
from conductor_bot.misc.states import UserState
from conductor_bot.keyboards.inline import main_menu, found_menu, check_menu
from conductor_bot.misc.db import check_user_system, get_user_description


async def start_handler(message: Message):
    user_in_db = await check_user_system(message.chat.username)
    if user_in_db:
        await message.answer(text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'), reply_markup=main_menu)
        await UserState.user_in_system.set()
    else:
        await message.answer(emoji.emojize(":red_exclamation_mark: Вас нету в системе :red_exclamation_mark:"))
        

async def user_base_handler(message: Message):
    user_in_db = await check_user_system(message.chat.username)
    if user_in_db:
        await message.answer(text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'), reply_markup=main_menu)
        await UserState.user_in_system.set()
    else:
        await message.answer(emoji.emojize(":red_exclamation_mark: Вас нету в системе :red_exclamation_mark:"))

        

async def find_handler(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    curr_username = call.from_user.username
    curr_chat_id = call.from_user.id
    await bd_users.add_user(curr_username, curr_chat_id, curr_chat_id)
    if await bd_users.check_users(curr_username):
        friend: list(User) = await bd_users.get_friend(curr_username)
        await call.bot.send_message(chat_id=curr_chat_id, text=get_user_description(friend.username))
        await bd_users.delete_user(call.from_user.username)
        await call.bot.send_message(chat_id=friend.chat_id, text=get_user_description(curr_username))
        await call.message.answer(text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'), reply_markup=main_menu)

    else:
        await call.answer("Пользователи не найдены!")
        await call.message.answer(emoji.emojize("Режим поиска включен :speaker_high_volume:"), reply_markup=found_menu)
    
    
async def cancel_handler(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await bd_users.delete_user(call.from_user.username)
    await call.message.answer(text=emoji.emojize(':magnifying_glass_tilted_right: Включить режим поиска :magnifying_glass_tilted_right:'), reply_markup=main_menu)

    
# async def ok(message: Message):
#     print(get_user_description(message.chat.username))
#     await message.answer("Ok")
       
def register_user(dp: Dispatcher):
    # dp.register_message_handler(ok, state=None)

    dp.register_callback_query_handler(find_handler, state=UserState.user_in_system, text="btnFind")
    dp.register_callback_query_handler(cancel_handler, state=UserState.user_in_system, text="btnCancel")
    dp.register_message_handler(start_handler, commands=["/start"], state="*")
    dp.register_message_handler(user_base_handler, state="*")
    
