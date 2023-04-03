import fdb

from config import hidden_vars

con = fdb.connect(dsn=hidden_vars.db.dsn, user=hidden_vars.db.user, password=hidden_vars.db.password)
cursor = con.cursor()


def goods_list(cur, *args):
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
        f"FROM DIR_GOODS dg, DOC_EXPSESSION_TABLE det "
        f"WHERE dg.CODE = det.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]}) SQ "
        f"GROUP BY SQ. CODE, SQ.NAME, SQ.PRICE_ "
        f"HAVING SUM(SQ.QUANTITY) >= 1 "
        f"ORDER BY SQ.PRICE_"

    )

    return cur.fetchall()


def fb_dir_goods_request(cur, **kwargs):
    cur.execute(
        "SELECT {column} FROM DIR_GOODS WHERE CODE = {code}".format(**kwargs)
    )
    return cur.fetchall()
