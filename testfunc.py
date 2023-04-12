from core_func import title_formatting
from db.sqlite_work import show_distributor_offer

response = show_distributor_offer('Xiaomi под заказ')
for n in response:
    print(title_formatting('Xiaomi под заказ', n[1]))