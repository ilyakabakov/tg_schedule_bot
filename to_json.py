import json


arr = []

""" CENSURE MODULE """
with open('cens.txt', encoding='utf8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            arr.append(n)

with open('cens.json', 'w', encoding='utf8') as e:
    json.dump(arr, e)

""" Opening files """

f_name = 'master.json'
arr_j = []

with open(f_name, 'r', encoding='utf8') as file:
    data_j = json.load(file)

for query in data_j:
    for text in data_j[query]['queries']:
        arr_j.append(text)


def read_from_file():
    with open('bio.txt', 'r', encoding='utf8') as f:
        data = f.read()
        return str(data)


def read_price():
    with open('price.txt', 'r', encoding='utf8') as f:
        data = f.read()
    return str(data)



