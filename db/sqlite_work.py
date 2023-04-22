from datetime import datetime

from core_vars import sqlite_connection

from db.fdb_work import fb_dir_goods_request


def write_user_enter(*args):
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        f"INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?)", args)
    sqlite_connection.commit()


def read_product(**kwargs):
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        "SELECT {name} FROM PRODUCT_DESC WHERE {code} = {product_code}".format(**kwargs)
    )
    result = sqlite_cur.fetchone()
    try:
        return result
    except TypeError:
        return None


def check_sqlite_db(product_code):
    try:
        result = read_product(name='CODE', code='CODE', product_code=product_code)
        return result
    except TypeError:
        return None


def take_caption_sqlite(product_code):
    result = check_sqlite_db(product_code)
    price = fb_dir_goods_request(column='PRICE_', code=product_code)
    if result:
        line = read_product(name='NAME, DESCRIPT', code='CODE', product_code=product_code)
        descr = '' if line[1] is None else line[1]
        caption = f"Цена {int(price[0][0])} руб.\n{line[0]}\n\n{descr}"
        return caption
    else:
        line = fb_dir_goods_request(column='NAME, PRICE_', code=product_code)
        caption = f"{int(line[0][1])} руб.\n{line[0][0]}"
        write_photo_db(product_code, line[0][0])
        return caption


def write_photo_db(code, name):
    sqlite_cursor = sqlite_connection.cursor()
    sqlite_cursor.execute(f"INSERT INTO PRODUCT_DESC (CODE, NAME) VALUES ('{code}', '{name}')")
    sqlite_connection.commit()


def show_distributor_offer(table):
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        f"SELECT PRODUCT, OUT_COST FROM {table} "
        f"WHERE DATE = (SELECT MAX(DATE) FROM {table}) "
        f"ORDER BY OUT_COST"
    )
    result = sqlite_cur.fetchall()
    try:
        return result
    except TypeError:
        return None


def get_date_from_db(table):
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        f'select max(date) from {table}'
    )
    response = sqlite_cur.fetchone()[0]
    date = response.split('T')[0]
    time = response.split('T')[1]
    old_format_date = datetime.strptime(date, '%Y-%m-%d')
    result = old_format_date.strftime('%d-%m-%Y')
    return str(result) + ' в ' + time


def choose_table():
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = sqlite_cur.fetchall()
    return result
