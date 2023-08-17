import json
import os

cwd = os.getcwd()

f_name = os.path.join(cwd, 'database/content.json')

with open(f_name, 'r', encoding="utf-8") as file:
    data_json = json.load(file)

""" Coroutines for response from json data """


async def array_json(user: str, query: str):
    try:
        data = await get_data_json(user)
        return data[query]
    except Exception as ex:
        print(f'Func array_json failed ERROR: {ex}')


async def get_data_json(user: str):
    return data_json.get(user)
