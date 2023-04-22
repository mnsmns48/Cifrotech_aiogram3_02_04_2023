from openpyxl.workbook import Workbook

from config import hidden_vars
from core_func import _profit
from core_vars import y, sqlite_connection
from distrib_mail_parsing import check_data_in_distributor

with open('zz_ttt.txt', encoding='utf-8') as f:
    read_result = f.read()


def pars_price_from_mes(price: str, separator: str, table: str, date: str) -> None:
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
    filename = table + '_' + date[:10] + '.xlsx'
    wb.save(f'shippers/{hidden_vars.mail_connect.mail_path}/{filename}')
    y.upload(f'shippers/{hidden_vars.mail_connect.mail_path}/{filename}', f'/shippers/Mobex/{filename}',
             overwrite=True)
    sqlite_cur = sqlite_connection.cursor()
    for item in interval_result_list:
        sqlite_cur.execute(f"INSERT INTO {table} VALUES "
                           f"('{date}', "
                           f"'{item[0]}', "
                           f"'{item[1]}', "
                           f"'{_profit(int(item[1]))}')")
    sqlite_connection.commit()
    print('Запись:', table, date[:10], 'завершена')


pars_price_from_mes(read_result, 'separator_space', 'terra_apple', '2023-04-22T23:17')
