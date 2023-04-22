import re

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.sqlite_work import choose_table

admin_basic_ = [
    [KeyboardButton(text='Загрузить прайс Apple')],
    [KeyboardButton(text='Продажи сегодня')],
    [KeyboardButton(text='Продажи вчера')],
    [KeyboardButton(text='Продажи другой день')],
]

admin_basic_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=admin_basic_)


choose_price_ibk = InlineKeyboardBuilder()
required_tables = []
for row in choose_table():
    for column in row:
        required_tables.append(column)
for line in required_tables:
    if re.findall('apple', line):
        choose_price_ibk.row(InlineKeyboardButton(
            text=line, callback_data=line))


separator_ibk = InlineKeyboardBuilder()
separator_ibk.row(InlineKeyboardButton(
    text='⋞ - ⋟', callback_data='separator_dash'))
separator_ibk.row(InlineKeyboardButton(
    text='⋞ пробел ⋟', callback_data='separator_space'))