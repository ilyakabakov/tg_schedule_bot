import json


arr = []

""" CENSURE MODULE """
with open('database/cens.txt', encoding='utf8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            arr.append(n)

with open('database/cens.json', 'w', encoding='utf8') as e:
    json.dump(arr, e)

""" Opening files """

f_name = 'database/master.json'
array_json = []

with open(f_name, 'r', encoding='utf8') as file:
    data_json = json.load(file)

for query in data_json:
    for text in data_json[query]['queries']:
        array_json.append(text)
