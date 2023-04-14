# from openpyxl.workbook import Workbook
#
# file = open("text.txt")
# text = file.read()
# lis = list()
# risk = list()
# for line in text.split('\n'):
#     if '  -  ' in line:
#         lis.append(line)
# for i in lis:
#     risk.append([i.split('  -  ')[0], int(i.split('  -  ')[1])])
# wb = Workbook()
# ws = wb.active
# ws.title = "Лист1"
# for i in risk:
#     ws.append(i)
# wb.save('1.xlsx')
#     if '  -  ' not in lst[i]:
#         del lst[i]
#     i += 1
#
# print(lst)

#
# for i in ls:
#     if i == ls[0]:
#         sp.append(text[:i] + ' - ' + text[i + 4:text.find('\n', i)])
#         count = len(text[:text.find('\n', i)])
#     elif i != ls[-1]:
#         sp.append(text[text.find('\n', count+1):i] + ' - ' + text[i + 4:text.find('\n', i)])
#         # count = len(text[:text.find('\n', i)])
#
#     # else:
#     #     sp.append(text[text.find('\n', i, ls[-2])+2:i] + ' - ' + text[i + 4:text.find('\n', i)])
#
# for i in sp:
#     print(i)
