import json

arr = []
arr_main = []

""" CENSURE MODULE """
with open('../cens.txt', encoding='utf8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            arr.append(n)

with open('../cens.json', 'w', encoding='utf8') as e:
    json.dump(arr, e)


