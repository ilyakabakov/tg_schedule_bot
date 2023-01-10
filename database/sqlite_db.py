import sqlite3 as sql
from create_bot import bot


def sql_start():
    global base, cur
    base = sql.connect('reserved.db')
    cur = base.cursor()
    if base:
        print('Database connected')
    base.execute(
        'CREATE TABLE IF NOT EXISTS clients(client_id INTEGER PRIMARY KEY, name varchar(128), phone_n varchar(32) NOT NULL, gmt varchar(64) NOT NULL, comment TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO clients(name, phone_n, gmt, comment) VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM clients').fetchall():
        await bot.send_message(message.from_user.id,
                               f'ID: {ret[0]}\nName: {ret[1]}\nPhone number: {ret[2]}\nTimezone: {ret[3]}\nComment: {ret[-1]}')


async def sql_read_two():
    return cur.execute('SELECT * FROM clients').fetchall()


res = []


async def sql_read_only_one(state):
    global res
    async with state.proxy() as data:
        res = cur.execute("SELECT * FROM clients WHERE client_id == ?", (data,)).fetchall()
        base.commit()
        return res


async def sql_delete_command(data):
    cur.execute('DELETE FROM clients WHERE client_id == ?', (data,))
    base.commit()


async def delete_all_data():
    cur.execute('DROP TABLE IF EXISTS clients')
    base.commit()
