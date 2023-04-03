import sqlite3

from db.fdb_work import fb_dir_goods_request, cursor


def write_user_enter(*args):
    sqlite_connection = sqlite3.connect('db/cifrotech_db', check_same_thread=False)
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        f"INSERT INTO USERS ("
        f"TIME, "
        f"ID, "
        f"FIRST_NAME, "
        f"LAST_NAME, "
        f"USERNAME, "
        f"MESSAGE_ID, "
        f"TEXT) VALUES (?, ?, ?, ?, ?, ?, ?)", args)
    sqlite_connection.commit()


def read_product(**kwargs):
    sqlite_connection = sqlite3.connect('db/cifrotech_db', check_same_thread=False)
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
    price = fb_dir_goods_request(cur=cursor, column='PRICE_', code=product_code)
    if result:
        line = read_product(name='NAME, DESCRIPT', code='CODE', product_code=product_code)
        descr = '' if line[1] is None else line[1]
        caption = f"Цена {int(price[0][0])} руб.\n{line[0]}\n\n{descr}"
        return caption
    else:
        line = fb_dir_goods_request(cur=cursor, column='NAME, PRICE_', code=product_code)
        caption = f"{int(line[0][1])} руб.\n{line[0][0]}"
        write_photo_db(product_code, line[0][0])
        return caption


def write_photo_db(code, name):
    sqlite_connection = sqlite3.connect('db/cifrotech_db', check_same_thread=False)
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(f'INSERT INTO PRODUCT_DESC (CODE, NAME) VALUES ({code}, {name})')
    sqlite_connection.commit()