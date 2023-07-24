import json
import os

cwd = os.getcwd()

f_name = os.path.join(cwd, 'database/content.json')

with open(f_name, 'r', encoding="utf-8") as file:
    data_json = json.load(file)

""" Coroutines for response from json data """
async def array_json(user: str, query: str):
    try:
        array = []
        data = await get_data_json(user)

        for text in data[query]:
            array.append(text)
        return array[0]
    except Exception as ex:
        print(f'Func array_json failed ERROR: {ex}')


async def get_data_json(user: str):
    return data_json.get(user)
