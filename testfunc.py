from datetime import datetime

from core_func import date_out
from core_vars import sqlite_connection


def newest_price():
    sqlite_cur = sqlite_connection.cursor()
    sqlite_cur.execute(
        f"SELECT NT.DATE, NT.PRODUCT, NT.OUT_COST FROM ("

        f"SELECT ta.DATE, ta.PRODUCT, ta.OUT_COST FROM terra_apple ta "
        f"WHERE ta.DATE = (SELECT MAX(ta.DATE) FROM terra_apple ta) "
        f"UNION "

        f"SELECT oa.DATE, oa.PRODUCT, oa.OUT_COST FROM optmobex_apple oa "
        f"WHERE oa.DATE = (SELECT MAX(oa.DATE) FROM optmobex_apple oa) "
        f"UNION "

        f"SELECT ra.DATE, ra.PRODUCT, ra.OUT_COST FROM r_apple ra "
        f"WHERE ra.DATE = (SELECT MAX(ra.DATE) FROM r_apple ra) "
        f") NT "

        f"ORDER BY NT.DATE DESC, NT.OUT_COST"
    )
    result = sqlite_cur.fetchall()
    return result

k = []
apple_price = newest_price()
for i in apple_price:
    if i[0] == apple_price[0][0]:
        k.append(i)