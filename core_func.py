from typing import List, Union, Dict

import pytz
from datetime import datetime

from openpyxl.workbook import Workbook

from config import hidden_vars
from core_vars import sqlite_connection, y

samsung_xlsx_list = list()
xiaomi_xlsx_list = list()
apple_txt_list = list()


def date_out(date):
    m_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z")
    tz = pytz.timezone("Etc/GMT-3")
    m_date_utc3 = tz.normalize(m_date.astimezone(tz))
    out_date = m_date_utc3.strftime("%Y-%m-%dT%H:%M")
    return out_date


def ya_time_converter(time):
    a = time
    tz = pytz.timezone("Etc/GMT-3")
    date = tz.normalize(a.astimezone(tz))
    return date.date().strftime("%d %m %Y")


days = ({0: "Понедельник"},
        {1: "Вторник"},
        {2: "Среда"},
        {3: "Четверг"},
        {4: "Пятница"},
        {5: "Суббота"},
        {6: "Воскресенье"})

month = ({1: "Января"},
         {2: "Февраля"},
         {3: "Марта"},
         {4: "Апреля"},
         {5: "Мая"},
         {6: "Июня"},
         {7: "Июля"},
         {8: "Августа"},
         {9: "Сентября"},
         {10: "Октября"},
         {11: "Ноября"},
         {12: "Декабря"})


def title_formatting(price, name):
    del_list = list()
    if price == 'optmobex_xiaomi':
        del_list = ['EU ', 'Xiaomi ', 'CN', ' RU/СТБ', ' RU']
    if price == 'optmobex_samsung':
        del_list = ['Samsung Galaxy', 'AE', 'AH', 'KZ', 'EU', 'CN',
                    'IN', ',', 'Simfree', 'RU', 'ZA', '   ', 'TH', '/']
    for i in del_list:
        name = name.replace(i, '')
    return name


def _profit(entry_price):
    price_range = [(0, 2000),  #500
                   (2000, 7000),  # 1400
                   (7000, 10000),  # 1900
                   (10000, 15000),  # 2400
                   (15000, 20000),  # 2900
                   (20000, 30000),  # 3400
                   (30000, 50000),  # 3900
                   (50000, 100000),  # 5900
                   (100000, 3000000)]  # 8900
    profit = [500, 1400, 1900, 2400, 2900, 3400, 3900, 5900, 8900]
    for i in range(len(profit)):
        if entry_price in range(*price_range[i]):
            return entry_price + profit[i]


def pars_price_from_mes(price: str, separator: str, table: str, date: datetime) -> None:
    convert_date = date_out(date)
    interval_result_list_ = list()
    interval_result_list = list()
    if separator == 'separator_dash':
        for line in price.split('\n'):
            if '-' in line and 'дней' not in line:
                interval_result_list_.append(line.split('-'))
    if separator == 'separator_space':
        for line in price.split('\n'):
            interval_result_list_.append(line.split(' '))
    for i in interval_result_list_:
        interval_result_list.append([' '.join(i[:-1]), i[-1]])
    wb = Workbook()
    ws = wb.active
    ws.title = "Лист1"
    ws.append(['Наименование', 'Цена', 'Заказ'])
    for item in interval_result_list:
        ws.append([item[0].strip(), int(item[1])])
    filename = table + '_' + convert_date[:10] + '.xlsx'
    wb.save(f'shippers/{hidden_vars.mail_connect.mail_path}/{filename}')
    y.upload(f'shippers/{hidden_vars.mail_connect.mail_path}/{filename}', f'/shippers/Mobex/{filename}',
             overwrite=True)
    sqlite_cur = sqlite_connection.cursor()
    for item in interval_result_list:
        sqlite_cur.execute(f"INSERT INTO {table} VALUES "
                           f"('{convert_date}', "
                           f"'{item[0]}', "
                           f"'{item[1]}', "
                           f"'{_profit(int(item[1]))}')")
    sqlite_connection.commit()
    print('Запись:', table, convert_date[:10], 'завершена')