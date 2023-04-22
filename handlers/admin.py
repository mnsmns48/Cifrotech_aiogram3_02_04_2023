from datetime import date, timedelta

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F

from core_func import date_out
from db.fdb_work import sales_one_day
from filters import AdminFilter
from keyboards.admin import admin_basic_kb, choose_price

admin_ = Router()


class GiveMeData(StatesGroup):
    date = State()
    apple_price = State()


date_today = date.today()
date_yesterday = date_today - timedelta(days=1)
date_today = str(date_today)
date_yesterday = str(date_yesterday)


async def choose_date(m: Message, state: FSMContext) -> None:
    if m.text == 'Продажи сегодня':
        line = sales_one_day(date=date_today)
        await m.answer(line)
    if m.text == 'Продажи вчера':
        line = sales_one_day(date=date_yesterday)
        await m.answer(line)
    if m.text == "Продажи другой день":
        await m.answer('Введите дату в формате: ХХХХ\nХХ - ДЕНЬ ХХ - МЕСЯЦ\nнапример: 0303\n'
                       'Будет показан отчет\nза 3 марта текущего года\n\n'
                       'Еcли ввести дату в формате: ХХХХХХ\n'
                       'ХХ - ДЕНЬ ХХ - МЕСЯЦ ХХ - ГОД\n'
                       'напрмер: 030320\n'
                       'Будет показан отчет\nза 3 марта 2020 года')
        await state.set_state(GiveMeData.date)


async def answer_date_another_day(m: Message, state: FSMContext):
    date_r = str()
    if m.text.isdigit():
        if len(m.text) == 4:
            date_r = '2023' + '-' + str(m.text[2:]) + '-' + m.text[:2]
        if len(m.text) == 6:
            date_r = '20' + str(m.text[4:]) + '-' + str(m.text[2:4]) + '-' + str(m.text[0:2])
        line = sales_one_day(date=date_r)
        await m.answer(line)
        await state.clear()
    else:
        await m.answer('Введите дату в нужном формате!\n\n'
                       'Читай инструкцию сверху')
        await state.clear()


async def price_download(m: Message, state: FSMContext):
    await m.answer('Добавляем')
    await state.set_state(GiveMeData.apple_price)


async def price_download_receiving(m: Message, state: FSMContext):
    await state.update_data(apple_price=m.text)
    await m.answer('Выбери куда сохранять', reply_markup=choose_price.as_markup())


async def choose_table(call: CallbackQuery, state: FSMContext):
    text = await state.get_data()
    print(text.get('apple_price'))
    await call.message.answer('вывел в консоль')

    await state.clear()


async def download_photo(m: Message):
    await m.answer('Адрес на сервере Telegram:')
    await m.answer(m.photo[-1].file_id)


async def start(m: Message):
    await m.answer('Admin Mode', reply_markup=admin_basic_kb)


def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(download_photo, F.photo)
    admin_.message.register(start, CommandStart())
    admin_.message.register(choose_date, F.text.contains('Продажи '))
    admin_.message.register(answer_date_another_day, GiveMeData.date)
    admin_.message.register(price_download, F.text == 'Загрузить прайс Apple')
    admin_.message.register(price_download_receiving, GiveMeData.apple_price)
    admin_.callback_query.register(choose_table)
