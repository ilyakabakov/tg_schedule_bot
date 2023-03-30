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

""" PARSER FOR JSON FILE """

f_name = 'database/master.json'

with open(f_name, 'r', encoding='utf8') as file:
    data_json = json.load(file)


def array_json(query: str):
    array = []
    data = data_json[query]
    for text in data['queries']:
        array.append(text)
    return array[0]
