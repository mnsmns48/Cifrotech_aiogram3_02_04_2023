from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.fdb_work import goods_list, cursor

samsung_phone_path = [80, 80]
realme_phone_path = [81, 81]
redmi_phone_path = [82, 82]
tecno_phone_path = [83, 83]
tcl_phone_path = [84, 84]
mediapad_phone_path = [29, 29]
key_old_phones = [28, 28]
smart_watches = [36, 36]


def show(*args):
    txt = list()
    result = goods_list(cursor, *args)
    for row in result:
        name = row[1].split(' ', 1)
        txt.append(f'{int(row[3])} {name[1]}_+_{row[0]}')
    # code = 0 name = 1 amount = 2 price = 3
    return txt


user_first_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=False,
                                    keyboard=[
                                        [KeyboardButton(text='В наличии')],
                                        [KeyboardButton(text='Под заказ')],
                                    ])

catalog_full_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                      one_time_keyboard=False,
                                      keyboard=[
                                          [KeyboardButton(text='Смартфоны')],
                                          [KeyboardButton(text='Планшеты')],
                                          [KeyboardButton(text='Умные часы')],
                                          [KeyboardButton(text='Кнопочные телефоны')],
                                          [KeyboardButton(text='Перейти в начало')]
                                      ])
catalog_brand_phones_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=False,
                                              keyboard=[
                                                  [KeyboardButton(text='Xiaomi / Redmi / Poco')],
                                                  [KeyboardButton(text='Realme / Oppo / OnePlus')],
                                                  [KeyboardButton(text='Samsung')],
                                                  [KeyboardButton(text='Tecno / Infinix')],
                                                  [KeyboardButton(text='TCL')],
                                                  [KeyboardButton(text='Полный список смартфонов')],
                                                  [KeyboardButton(text='Перейти в начало')]
                                              ])

redmi_inline_kb = InlineKeyboardBuilder()
for i in show(*redmi_phone_path):
    line = i.split('_+_')
    redmi_inline_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

realme_inline_kb = InlineKeyboardBuilder()
for i in show(*realme_phone_path):
    line = i.split('_+_')
    realme_inline_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

samsung_inline_kb = InlineKeyboardBuilder()
for i in show(*samsung_phone_path):
    line = i.split('_+_')
    samsung_inline_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

tecno_inline_kb = InlineKeyboardBuilder()
for i in show(*tecno_phone_path):
    line = i.split('_+_')
    tecno_inline_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

tcl_inline_kb = InlineKeyboardBuilder()
for i in show(*tcl_phone_path):
    line = i.split('_+_')
    tcl_inline_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

media_pad_kb = InlineKeyboardBuilder()
for i in show(*mediapad_phone_path):
    line = i.split('_+_')
    media_pad_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

key_old_phones_kb = InlineKeyboardBuilder()
for i in show(*key_old_phones):
    line = i.split('_+_')
    key_old_phones_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

watches_kb = InlineKeyboardBuilder()
for i in show(*smart_watches):
    line = i.split('_+_')
    watches_kb.row(InlineKeyboardButton(
        text=line[0], callback_data=line[1]))

catalog_order_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=False,
                                       keyboard=[
                                           [KeyboardButton(text='Apple под заказ')],
                                           [KeyboardButton(text='Xiaomi под заказ')],
                                           [KeyboardButton(text='Samsung под заказ')],
                                           [KeyboardButton(text='Перейти в начало')],
                                       ])