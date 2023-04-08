import imaplib, email
from datetime import datetime
from email.header import decode_header

from config import hidden_vars
from core import date_out

letters = list()


def mail_connect():
    global con
    con = imaplib.IMAP4_SSL("imap.mail.ru")
    con.login(hidden_vars.mail_connect.mailbox, hidden_vars.mail_connect.mail_pass)
    con.list()
    con.select('Mobex')
    result, data_connect = con.search(None, "UNSEEN")
    msg_list = list(data_connect[0].decode('UTF-8').replace(' ', ''))
    return msg_list


def mail_processing():
    unread_msg_list = mail_connect()
    for i in unread_msg_list:
        result, data = con.fetch(i, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        dt_date = date_out(email.utils.parsedate_to_datetime(msg["Date"]))
        subject = decode_header(msg["Subject"])[0][0].decode()
        if 'под заказ, за наличные' in subject:
            print(dt_date, subject)


if mail_connect():
    mail_processing()
else:
    print('Нет новых писем')
