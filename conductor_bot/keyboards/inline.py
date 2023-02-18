from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import emoji

main_menu = InlineKeyboardMarkup(row_width=1)
found_menu = InlineKeyboardMarkup(row_width=1)
check_menu = InlineKeyboardMarkup(row_width=1)

btnFind = InlineKeyboardButton(text=emoji.emojize("Искать собеседник :light_bulb:"), callback_data="btnFind")
btnCancel = InlineKeyboardButton(text=emoji.emojize("Остановить поиск :bell_with_slash:"), callback_data="btnCancel")
btnCheck = InlineKeyboardButton(text="Проверить", callback_data="btnCheck")

main_menu.insert(btnFind)
found_menu.insert(btnCancel)
check_menu.insert(btnCheck)