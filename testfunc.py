import imaplib, email
import os, base64
from datetime import datetime
from email.header import decode_header

from openpyxl.reader.excel import load_workbook

from config import hidden_vars
from core import date_out
from db.sqlite_work import write_goods_for_deliver, sqlite_connection

xiaomi_del_list = [' EU ', ' RU ', ' RUСТБ ', 'Xiaomi ', ' JP ']


def android_profit(entry_price):
    price_range = [(0, 7000),
                   (7000, 10000),
                   (10000, 15000),
                   (15000, 20000),
                   (20000, 30000),
                   (30000, 50000),
                   (50000, 100000),
                   (100000, 3000000)]
    profit = [1400, 1900, 2400, 2900, 3400, 5000, 8000, 10000]
    for i in range(len(profit) - 1):
        if entry_price in range(*price_range[i]):
            return entry_price + profit[i]


def excel_order_list(file, del_list):
    price_list = list()
    price_out = list()
    wb = load_workbook(file)
    ws = wb["Лист1"]
    rows = ws.max_row
    cols = ws.max_column - 1
    for i in range(2, rows):
        string = str()
        for j in range(1, cols + 1):
            cell = ws.cell(row=i, column=j)
            string = string.replace(",", "").replace("/", "")
            for t in del_list:
                string = string.replace(t, ' ')
            string = string + str(cell.value) + ' '
        price_list.append(string.strip(' ').split(' '))
    price_list.sort(key=lambda arr: int(arr[-1]))
    for k in price_list:
        price_out.append((" ".join(k[:-1]), k[-1], android_profit(int(k[-1]))))
    return price_out


def mail_connect():
    global con
    con = imaplib.IMAP4_SSL("imap.mail.ru")
    con.login(hidden_vars.mail_connect.mailbox, hidden_vars.mail_connect.mail_pass)
    con.list()
    con.select('Mobex')
    result, data_connect = con.search(None, "ALL")
    msg_list = list(data_connect[0].decode('UTF-8').replace(' ', ''))
    return msg_list


def mail_processing():
    price_list = list()
    price_out = list()
    unread_msg_list = mail_connect()
    for i in unread_msg_list:
        result, data = con.fetch(i, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        dt_date = date_out(email.utils.parsedate_to_datetime(msg["Date"]))
        subject = decode_header(msg["Subject"])[0][0].decode()
        if 'под заказ, за наличные' in subject:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    transfer_encoding = part.get_all('Content-Transfer-Encoding')
                    if transfer_encoding and transfer_encoding[0] == 'base64':
                        filename_parts = filename.split('?')
                        filename = base64.b64decode(filename_parts[3]).decode(filename_parts[1])
                        with open(filename, 'wb') as new_file:
                            new_file.write(part.get_payload(decode=True))
                        wb = load_workbook(filename)
                        ws = wb["Лист1"]
                        rows = ws.max_row
                        cols = ws.max_column - 1
                        for i in range(2, rows):
                            string = str()
                            for j in range(1, cols + 1):
                                cell = ws.cell(row=i, column=j)
                                string = string + str(cell.value) + ' '
                            price_list.append(string)
                        # price_list.sort(key=lambda arr: int(arr[-1]))
                    print(" ".join(price_list[1]))

                        # write_goods_for_deliver(dt_date,
                        #                         filename,
                        #                         price_out[0],
                        #                         price_out[1],
                        #                         price_out[2])


mail_processing()
