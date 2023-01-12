import sqlite3 as sql
from create_bot import bot


def sql_start():
    global base, cur
    base = sql.connect('reserved.db')
    cur = base.cursor()
    if base:
        print('Database connected')
    base.execute(
        'CREATE TABLE IF NOT EXISTS clients(client_id INTEGER PRIMARY KEY, name VARCHAR(128), phone_n VARCHAR(32) NOT NULL, gmt VARCHAR(64) NOT NULL, comment TEXT)'
    )
    base.execute(
        'CREATE TABLE IF NOT EXISTS questions(question_id INTEGER PRIMARY KEY, question TEXT, name VARCHAR(128), phone_n VARCHAR(32) NOT NULL)'
    )
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO clients(name, phone_n, gmt, comment) VALUES(?, ?, ?, ?)',
            tuple(data.values()
                  )
        )
        base.commit()


async def sql_add_command2(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO questions(question, name, phone_n) VALUES(?, ?, ?)',
            tuple(data.values()
                  )
        )
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM clients').fetchall():
        await bot.send_message(message.from_user.id,
                               f'ID: {ret[0]}\n'
                               f'Name: {ret[1]}\n'
                               f'Phone number: {ret[2]}\n'
                               f'Timezone: {ret[3]}\n'
                               f'Comment: {ret[-1]}')


async def sql_read_two():
    return cur.execute('SELECT * FROM clients').fetchall()


async def sql_read_three():
    return cur.execute('SELECT * FROM questions').fetchall()


async def sql_read_questions(message):
    for row in cur.execute('SELECT * FROM questions').fetchall():
        await bot.send_message(message.from_user.id,
                               f'ID: {row[0]}\n'
                               f'Имя: {row[2]}\n'
                               f'Номер телефона: {row[3]}\n'
                               f'Вопрос: \n{row[1]}\n')


async def sql_delete_command(data):
    cur.execute('DELETE FROM clients WHERE client_id == ?', (data,))
    base.commit()


async def sql_delete_command_q(data):
    cur.execute('DELETE FROM questions WHERE question_id == ?', (data,))
    base.commit()


async def delete_all_data():
    cur.execute('DROP TABLE IF EXISTS clients')
    cur.execute('DROP TABLE IF EXISTS questions')
    base.commit()
