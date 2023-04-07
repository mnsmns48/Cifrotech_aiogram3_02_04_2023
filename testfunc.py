import yadisk
from config import hidden_vars
from core import ya_time_converter

files = dict()
y = yadisk.YaDisk(token=hidden_vars.misc_path.yadisk)

for i in list(y.listdir('shippers')):
    files[i['name']] = [ya_time_converter(i['modified']), i['file']]

print(list(files.keys()))
