from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin_basic_ = [
    [KeyboardButton(text='Загрузить прайс Apple')],
    [KeyboardButton(text='Продажи сегодня')],
    [KeyboardButton(text='Продажи вчера')],
    [KeyboardButton(text='Продажи другой день')],
]

admin_basic_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=admin_basic_)
