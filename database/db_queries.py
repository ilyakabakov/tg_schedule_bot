from sqlalchemy import select, delete, MetaData, Table, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database.db_creating import async_engine, Client, Question, Meeting, Event

AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


def get_async_session():
    """ Func for getting async session """
    async_session = AsyncSessionLocal()
    return async_session


""" DATABASE WRITE REQUESTS """


async def new_client(state):
    """ Create a new row in the clients table """

    async with state.proxy() as data:
        client = Client(
            name=data['name'],
            phone_number=data['phone_n'],
            gmt=data['gmt'],
            comment=data['comment'])
    async with get_async_session() as a_session:
        a_session.add(client)
        await a_session.commit()


async def new_question(state):
    """ Create a new row in the questions table """

    async with state.proxy() as data:
        question = Question(
            question=data['question'],
            name=data['name'],
            phone_number=data['phone_n'])
    async with get_async_session() as a_session:
        a_session.add(question)
        await a_session.commit()


async def new_meeting(state):
    """ Create a new row in the events table """

    async with state.proxy() as data:
        event = Event(
            id=1,
            naming=data['naming'],
            place=data['place'],
            date=data['date'],
            time=data['time'],
            price=data['price'])
    async with get_async_session() as a_session:
        a_session.add(event)
        await a_session.commit()


async def new_meeting_client(state):
    """ Create a new row in the meetings(event_clients) table """

    async with state.proxy() as data:
        meeting = Meeting(
            full_name=data["full_name"],
            phone_number=data["phone_n"]
        )

    async with get_async_session() as a_session:
        a_session.add(meeting)
        await a_session.commit()


""" DATABASE GET REQUESTS """

async_session = sessionmaker(async_engine,
                             class_=AsyncSession,
                             expire_on_commit=False)


async def get_events_data():
    """ Get from events table """

    async with async_session() as session:
        stmt = select(Event)
        res = await session.execute(stmt)
        rows = res.scalars().all()
        await session.close()
    return rows


async def get_clients_data():
    """ Get all data from clients table """

    async with async_session() as session:
        stmt = select(Client)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        await session.close()
    return rows


async def get_client_data():
    """ Get the last element from clients table """

    async with async_session() as session:
        stmt = select(Client).order_by(desc(Client.client_id)).limit(1)
        result = await session.execute(stmt)
        row = result.scalars().one()
        await session.close()
    return row


async def get_event_clients_data():
    """ Get from meetings(event_clients) table """

    async with async_session() as session:
        stmt = select(Meeting)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        await session.close()
    return rows


async def get_questions_data():
    """" Get from questions table """

    async with async_session() as session:
        stmt = select(Question)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        await session.close()
    return rows


""" DATABASE DELETE REQUESTS """


async def delete_client_data(data):
    """ Delete a row in clients table """

    async with async_session() as session:
        stmt = delete(Client).where(Client.client_id == int(data))
        await session.execute(stmt)
        await session.commit()


async def delete_meeting_client_data(data):
    """ Delete a row in the meetings table """

    async with async_session() as session:
        stmt = delete(Meeting).where(Meeting.client_id == int(data))
        await session.execute(stmt)
        await session.commit()


async def delete_question_data(data):
    """" Delete a row in the question table """

    async with async_session() as session:
        stmt = delete(Question).where(Question.question_id == int(data))
        await session.execute(stmt)
        await session.commit()


async def drop_all_tables():
    """ Drop all tables """

    async with async_engine.begin() as conn:
        async with async_session as session:
            metadata = MetaData()
            metadata.reflect(bind=conn)

            # Получаем список всех таблиц в базе данных
            all_tables = metadata.sorted_tables

            # Удаляем каждую таблицу по очереди
            for table in all_tables:
                await session.execute(Table(table.name, metadata).delete())

            await session.commit()
