import sqlite3 as sql

from create_bot import bot
from keyboards.admin_kb import admins_menu_kb


def sql_start():
    global base, cur
    try:
        base = sql.connect('database/reserved.db')
        cur = base.cursor()
        if base:
            print('Database connected')
        base.execute(
            'CREATE TABLE IF NOT EXISTS clients(client_id INTEGER PRIMARY KEY, name VARCHAR(128), phone_n VARCHAR(32) NOT NULL, gmt VARCHAR(64) NOT NULL, comment TEXT)'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS questions(question_id INTEGER PRIMARY KEY, question TEXT, name VARCHAR(128), phone_n VARCHAR(32) NOT NULL)'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS meetings(client_id INTEGER PRIMARY KEY, full_name VARCHAR(128), phone_n VARCHAR(32) NOT NULL)'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, naming TEXT, place TEXT, date VARCHAR(128), time VARCHAR(32), price VARCHAR(32))'
        )
        base.commit()
    except sql.Error:
        if base:
            base.rollback()
            print('Query was failed!')


""" CLIENTS PART """


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO clients(name, phone_n, gmt, comment) VALUES(?, ?, ?, ?)',
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
                               f'Comment: {ret[-1]}',
                               reply_markup=admins_menu_kb
                               )


async def sql_read_two():
    return cur.execute('SELECT * FROM clients').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM clients WHERE client_id == ?', (data,))
    base.commit()


""" QUESTIONS PART """


async def sql_add_command2(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO questions(question, name, phone_n) VALUES(?, ?, ?)',
            tuple(data.values()
                  )
        )
        base.commit()


async def sql_read_three():
    return cur.execute('SELECT * FROM questions').fetchall()


async def sql_read_questions(message):
    for row in cur.execute('SELECT * FROM questions').fetchall():
        await bot.send_message(message.from_user.id,
                               f'ID: {row[0]}\n'
                               f'Имя: {row[2]}\n'
                               f'Номер телефона: {row[3]}\n'
                               f'Вопрос: \n{row[1]}\n',
                               reply_markup=admins_menu_kb
                               )


async def sql_delete_command_q(data):
    cur.execute('DELETE FROM questions WHERE question_id == ?', (data,))
    base.commit()


"""EVENTS PART"""


async def sql_add_command_events(state):
    async with state.proxy() as data:
        cur.execute(
            'REPLACE  INTO events(id, naming, place, date, time, price) VALUES(1, ?, ?, ?, ?, ?)',
            tuple(data.values()
                  )
        )
        base.commit()


async def sql_read_events():
    return cur.execute('SELECT * FROM events').fetchall()


"""MEETING PART"""


async def sql_add_command_meeting(state):
    try:
        async with state.proxy() as data:
            cur.execute(
                'INSERT INTO meetings(full_name, phone_n) VALUES(?, ?)',
                tuple(data.values()
                      )
            )
            base.commit()
    except Exception as ex:
        print(f'Error: {ex}')


async def sql_read_meeting():
    try:
        return cur.execute('SELECT * FROM meetings').fetchall()
    except Exception as ex:
        print(f'Error: {ex}')


async def sql_delete_command_meet(data):
    cur.execute('DELETE FROM meetings WHERE client_id == ?', (data,))
    base.commit()


""" FOR ALL TABLES """


async def delete_all_data():
    cur.execute('DROP TABLE IF EXISTS clients')
    cur.execute('DROP TABLE IF EXISTS questions')
    cur.execute('DROP TABLE IF EXISTS meetings')
    base.commit()
