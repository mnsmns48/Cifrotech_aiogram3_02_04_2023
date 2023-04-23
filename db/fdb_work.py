import fdb

from config import hidden_vars

fdb_connection = fdb.connect(dsn=hidden_vars.db.dsn, user=hidden_vars.db.user, password=hidden_vars.db.password)


def goods_list(*args):
    cur = fdb_connection.cursor()
    cur.execute(
        f"SELECT SQ.CODE, SQ.NAME, Sum(QUANTITY), SQ.PRICE_ FROM ("
        f"SELECT dg.CODE, dg.NAME, dst.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SESSION_TABLE dst "
        f"WHERE dg.CODE = dst.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -dst2.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SALE_TABLE dst2 "
        f"WHERE dg.CODE = dst2.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -dbt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_BALANCE_TABLE dbt "
        f"WHERE dg.CODE = dbt.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, +drt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_RETURN_TABLE drt "
        f"WHERE dg.CODE = drt.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -det.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_EXPRESSION_TABLE det "
        f"WHERE dg.CODE = det.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]}) SQ "
        f"GROUP BY SQ.CODE, SQ.NAME, SQ.PRICE_ "
        f"HAVING SUM(SQ.QUANTITY) >= 1 "
        f"ORDER BY SQ.PRICE_"

    )

    return cur.fetchall()


def fb_dir_goods_request(**kwargs):
    cur = fdb_connection.cursor()
    cur.execute(
        "SELECT {column} FROM DIR_GOODS WHERE CODE = {code}".format(**kwargs)
    )
    return cur.fetchall()


def sales_one_day(**kwargs: str):
    cur = fdb_connection.cursor()
    cur.execute(
        "SELECT dr.DOC_DATE, dg.NAME, drt.QUANTITY, drt.PRICE2, drt.SUMMA2, dr.NONCASH  \
         FROM DOC_RETURN dr, DOC_RETURN_TABLE drt, DIR_GOODS dg \
         WHERE dr.DOC_DATE LIKE '{date}%' AND dr.CODE = drt.CODE AND drt.GOOD = dg.CODE \
         ORDER BY DOC_DATE".format(**kwargs))
    result_returns: list = cur.fetchall()
    returns = []
    amount_returns_cash_ = []
    amount_returns_card_ = []
    if result_returns:
        for row in result_returns:
            return_time: str = str(row[0])[11:16]
            return_item: str = row[1]
            return_quantity: int = int(row[2])
            return_one_unit: int = int(row[3])
            return_summ: int = int(row[4])
            return_cash_form = '\nВозвращено на карту' if int(row[5]) else '\nВозвращено наличными'
            if int(row[5]) == 1:
                amount_returns_card_.append(int(row[4]))
            else:
                amount_returns_cash_.append(int(row[4]))
            returns.append(f"  ↜{return_time}↜ {return_item}\n{return_quantity}-{return_one_unit} → "
                           f"{return_summ} {return_cash_form}")
    cur.execute(
        "SELECT ds.DOC_DATE, dg.NAME, dst.QUANTITY, dst.PRICE2, dst.SUMMA2, ds.NONCASH \
         FROM DOC_SALE ds, DOC_SALE_TABLE dst , DIR_GOODS dg \
         WHERE ds.DOC_DATE LIKE '{date}%' AND ds.CODE = dst.CODE AND dst.GOOD = dg.CODE \
         ORDER BY DOC_DATE".format(**kwargs))
    result_sales: list = cur.fetchall()
    if not result_sales:
        sales = []
    else:
        sales = []
        amount_sales_cash_ = []
        amount_sales_card_ = []
        for row in result_sales:
            sales_time: str = str(row[0])[11:16]
            sales_item: str = row[1]
            sales_quantity: int = int(row[2])
            sales_one_unit: int = int(row[3])
            sales_summ: int = int(row[4])
            sales_cash_form = '\n ━━Оплата━картой' if int(row[5]) else ''
            if int(row[5]) == 1:
                amount_sales_card_.append(int(row[4]))
            else:
                amount_sales_cash_.append(int(row[4]))
            sales.append(f"  ↝{sales_time}↝  {sales_item}\n{sales_quantity}-{sales_one_unit} → "
                         f"{sales_summ}━{sales_cash_form}")
    if result_sales:
        line = 'Дата: ' + str(kwargs.get('date')) + '\n'
        for i in sales:
            line = line + ''.join(i) + '\n'
        if result_returns:
            line = line + '\n----ВОЗВРАТЫ----\n\n'
            for y in returns:
                line = line + ''.join(y) + '\n'
        cash_ = sum(amount_sales_cash_) - sum(amount_returns_cash_)
        non_cash_ = sum(amount_sales_card_) - sum(amount_returns_card_)
        line = line + '\nНаличными: ' + str(cash_)
        line = line + '\nКартой: ' + str(non_cash_)
        line = line + '\nИТОГО: ' + str(cash_ + non_cash_)
        return line

    else:
        return 'Нет продаж'
