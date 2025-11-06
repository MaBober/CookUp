from model import Meeting, Participant
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, mapper

metadata = MetaData()

meetings = Table(
    'meetings', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('time', DateTime, nullable=False),
    Column('deadline', DateTime),
    Column('max_participants', Integer, nullable=False),
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
)

participants = Table(
    'participants', metadata,
    Column('meeting_id', Integer, nullable=False),
    Column('user_id', Integer, nullable=False),
)

def start_mappers():
    meetings_mapper = mapper(Meeting, meetings)
    users_mapper = mapper(User, users)
    participants_mapper = mapper(Participant, participants)
