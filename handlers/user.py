import json
import string
import time

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot import dp, bot
from db.fdb_work import goods_list
from db.sqlite_work import write_user_enter, take_caption_sqlite, read_product, get_date_from_db, show_distributor_offer
from core_func import date_out, title_formatting
from keyboards.user import user_first_kb, \
    catalog_full_kb, \
    redmi_inline_kb, \
    catalog_brand_phones_kb, \
    realme_inline_kb, \
    samsung_inline_kb, \
    tecno_inline_kb, \
    tcl_inline_kb, \
    media_pad_kb, \
    key_old_phones_kb, \
    watches_kb, \
    catalog_order_kb, powerbanks_kb, services_kb, smartphone_repair_kb, battery_kb, display_kb, honor_inline_kb

from config import hidden_vars


async def smart_goods(m: Message):
    txt = list()
    result = goods_list(80, 84)
    for row in result:
        txt.append(f'{row[1]}\nЦена: {int(row[3])} руб\n\n')
    line = ''.join(txt)
    txt.clear()
    await m.answer(text=line)


async def show_product(callback: CallbackQuery):
    code_product = callback.data
    chat_id = callback.from_user.id
    caption = take_caption_sqlite(code_product)
    pic = read_product(name='PHOTO', code='CODE', product_code=code_product)
    if pic is None or pic[0] is None:
        pic = FSInputFile(path=hidden_vars.misc_path.photo_path + str(code_product) + '.jpg',
                          chunk_size=100)
        await bot.send_photo(chat_id=chat_id, photo=pic, caption=caption)

    else:
        await bot.send_photo(chat_id=chat_id,
                             photo=read_product(name='PHOTO', code='CODE', product_code=code_product)[0],
                             caption=caption)


async def start(m: Message):
    write_user_enter(
        date_out(m.date),
        m.from_user.id,
        m.from_user.first_name,
        m.from_user.last_name,
        m.from_user.username,
        m.message_id,
        m.text
    )
    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption=f'Привет, {m.from_user.full_name}, этот БОТ показывает наличие и цены '
                                 f'в салоне мобильной связи ЦИФРОТЕХ\n\n'
                                 f'А также актуальные цены на продукцию под заказ',
                         reply_markup=user_first_kb)


async def begin(m: Message):
    await m.answer('Выбери категорию', reply_markup=user_first_kb)


async def catalog_all(m: Message):
    await m.answer(text='Выбери группу товаров', reply_markup=catalog_full_kb)


async def catalog_phones(m: Message):
    await m.answer(text='Выбери производителя или в конце списка есть перечень всех моделей',
                   reply_markup=catalog_brand_phones_kb)


async def redmi_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=redmi_inline_kb.as_markup())


async def realme_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=realme_inline_kb.as_markup())


async def honor_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=honor_inline_kb.as_markup())


async def samsung_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=samsung_inline_kb.as_markup())


async def tecno_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tecno_inline_kb.as_markup())


async def tcl_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tcl_inline_kb.as_markup())


async def catalog_media_pad(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=media_pad_kb.as_markup())


async def catalog_old_key_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=key_old_phones_kb.as_markup())


async def smart_watches(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=watches_kb.as_markup())


async def powerbanks(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=powerbanks_kb.as_markup())


async def items_order(m: Message):
    await m.answer(text='Товары под заказ доставляются\nот 1-го до 7-ми дней', reply_markup=catalog_order_kb)


async def services(m: Message):
    await m.answer('Услуги', reply_markup=services_kb)


async def smartphone_repair(m: Message):
    await m.answer('Можем быстро и недорого оказать помощь по ремонту', reply_markup=smartphone_repair_kb)


async def battery(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=battery_kb.as_markup())
    await m.answer('Заменим аккумулятор на вашем смартфоне.\n'
                   'Ассортимент тех, что в наличии представлен выше\n'
                   'Для заказа любого другого аккумулятора пишите:\n@tser88 или @cifrotech_mobile')


async def display(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=display_kb.as_markup())
    await m.answer('Заменим разбитый дислпей!\n'
                   'Ассортимент тех, что в наличии представлен выше\n'
                   'Стоимость указана за дисплей вместе с услугой по установке\n'
                   'Для заказа любого другого пишите:\n@tser88 или @cifrotech_mobile')


async def xerox(m: Message):
    await m.answer_photo(photo='AgACAgIAAxkBAAIUBGQ7_ZXQPPvs1o8pNmt9ncZIKTd2AAKlxzEb73ThScaSExX72hsBAQADAgADeQADLwQ',
                         caption='ПН-СБ: С 8-00 до 17-00\n'
                                 '   ВС: С 9-00 до 17-00\n\n'
                                 'Всегда рады помочь🙂')


async def chat_bot(m: Message):
    await m.answer('Любые консультации по проектированию, созданию и размещению на сервере чат-ботов любой сложности\n'
                   '@tser88\n\n')


async def display_order_list(m: Message):
    spreadsheet = str()
    if m.text == 'Xiaomi под заказ':
        spreadsheet = 'optmobex_xiaomi'
    elif m.text == 'Samsung под заказ':
        spreadsheet = 'optmobex_samsung'
    elif m.text == 'Apple под заказ':
        spreadsheet = 'optmobex_apple'
    update_text = f'Цены обновлены {get_date_from_db(spreadsheet)}\nи будут актуальны 1-3 дня'
    result = show_distributor_offer(spreadsheet)
    mess = update_text + '\n\n↓ ↓ ↓ ↓ \n' + \
           title_formatting(spreadsheet, ''.join(item[0] + ' ' + str(item[1]) + '\n' for item in result))
    if len(mess) > 4096:
        for i in range(0, len(mess), 4096):
            part_mess = mess[i: i + 4096]
            await m.answer(part_mess)
            time.sleep(1)
    else:
        await m.answer(mess)
    await m.answer('ВНИМАНИЕ, смотрите на дату обновления цен в начале сообщения\n'
                   'По любым вопросам обращайтесь\n@tser88 или @cifrotech_mobile')


async def echo(m: Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in m.text.split(' ')} \
            .intersection(set(json.load(open('mat.json')))):
        await m.reply('Некрасиво выражаешься')
        await m.delete()
    else:
        await m.answer('Всё ясно! Пользуйся всплывающей клавиатурой')


async def hello(m: Message):
    await m.answer('И тебе привет! Внизу есть клавиатура, выбирай нужный пункт меню')


async def download_photo(m: Message):
    await m.answer(m.photo[-1].file_id)


def register_user_handlers():
    dp.message.register(start, CommandStart())
    dp.callback_query.register(show_product)
    dp.message.register(begin, F.text == 'Перейти в начало')
    dp.message.register(catalog_all, F.text == 'В наличии')
    dp.message.register(catalog_phones, F.text == 'Смартфоны')
    dp.message.register(redmi_phones, F.text == 'Xiaomi / Redmi / Poco')
    dp.message.register(realme_phones, F.text == "Realme / Oppo / OnePlus")
    dp.message.register(honor_phones, F.text == "Huawei / Honor")
    dp.message.register(samsung_phones, F.text == "Samsung")
    dp.message.register(tecno_phones, F.text == "Tecno / Infinix")
    dp.message.register(tcl_phones, F.text == "TCL")
    dp.message.register(catalog_media_pad, F.text == "Планшеты")
    dp.message.register(catalog_old_key_phones, F.text == "Кнопочные телефоны")
    dp.message.register(smart_watches, F.text == "Умные часы")
    dp.message.register(powerbanks, F.text == "Power Banks")
    dp.message.register(smart_goods, F.text == "Полный список смартфонов")
    dp.message.register(items_order, F.text == "Под заказ")
    dp.message.register(hello, F.text == "Привет")
    dp.message.register(display_order_list, F.text.contains(' под заказ'))
    dp.message.register(services, F.text == 'Услуги')
    dp.message.register(smartphone_repair, F.text == 'Ремонт смартфонов')
    dp.message.register(battery, F.text == 'Замена батареи')
    dp.message.register(display, F.text == 'Замена дисплея')
    dp.message.register(xerox, F.text == 'Ксерокопия, печать, сканирование')
    dp.message.register(chat_bot, F.text == 'Проектирование чат-ботов')
    dp.message.register(echo, F.text)
    # dp.message.register(download_photo, F.photo)
