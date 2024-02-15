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


async def new_client(data):
    """ Create a new row in the clients table """
    # get_data = data
    client = Client(
        name=data.get('name'),
        phone_number=data.get('phone'),
        gmt=data.get('gmt'),
        comment=data.get('comment')
    )
    async with get_async_session() as a_session:
        a_session.add(client)
        await a_session.commit()


async def new_question(data):
    """ Create a new row in the questions table """

    question = Question(
        question=data.get('question'),
        name=data.get('name'),
        phone_number=data.get('phone_n'))
    async with get_async_session() as a_session:
        a_session.add(question)
        await a_session.commit()


async def new_meeting(data):
    """ Create a new row in the events table """

    event = Event(
            id=1,
            naming=data.get('naming'),
            place=data.get('place'),
            date=data.get('date'),
            time=data.get('time'),
            price=data.get('price'))
    async with get_async_session() as a_session:
        a_session.add(event)
        await a_session.commit()


async def new_meeting_client(data):
    """ Create a new row in the meetings(event_clients) table """

    meeting = Meeting(
            full_name=data.get("full_name"),
            phone_number=data.get("phone_n")
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

            # Get list of all tables in database
            all_tables = metadata.sorted_tables

            # Delete all tables
            for table in all_tables:
                await session.execute(Table(table.name, metadata).delete())

            await session.commit()
