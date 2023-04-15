import sqlite3

import yadisk

from config import hidden_vars

y = yadisk.YaDisk(token=hidden_vars.misc_path.yadisk)
sqlite_connection = sqlite3.connect('db/cifrotech_db', check_same_thread=False)
