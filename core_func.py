import imaplib
import os
from datetime import datetime

import requests
import yadisk
from openpyxl.reader.excel import load_workbook
import pytz

from config import hidden_vars

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


def android_profit(entry_price):
    price_range = [(0, 7000), #1400
                   (7000, 10000), #1900
                   (10000, 15000), #2400
                   (15000, 20000), #2900
                   (20000, 30000), #3400
                   (30000, 50000), #4800
                   (50000, 100000), #6900
                   (100000, 3000000)] #8900
    profit = [1400, 1900, 2400, 2900, 3400, 4800, 6900, 8900]
    for i in range(len(profit)):
        if entry_price in range(*price_range[i]):
            return entry_price + profit[i]
