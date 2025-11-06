from model import Meeting, Participant
from repository import SQLAlchemyMeetingRepository

import datetime as dt

def insert_meeting(orm_session):

    orm_session.execute(
        '''
        INSERT INTO meetings (title, time, deadline, max_participants)
        VALUES (:title, :time, :deadline, :max_participants)
        ''',
        {
            'title': "Learn Python",
            'time': dt.datetime(2024, 8, 15, 10, 0),
            'deadline': dt.datetime(2024, 8, 14, 10, 0),
            'max_participants': 10
        }
    )

    [meeting_id] = orm_session.execute(
        'SELECT id FROM meetings WHERE title = :title',
        {'title': "Learn Python"}
    ).fetchone()

    return meeting_id

def insert_participant(orm_session, meeting_id):

    orm_session.execute(
        '''
        INSERT INTO participants (meeting_id, user_id)
        VALUES (:meeting_id, :user_id)
        ''',
        {
            'meeting_id': meeting_id,
            'user_id': 1
        }
    )


def test_repository_can_save_a_meeting(orm_session):

    meeting = Meeting(
        title="Cook with Beaver",
        time=dt.datetime(2024, 7, 1, 18, 0),
        deadline=dt.datetime(2024, 6, 30, 18, 0),
        max_participants=5
    )

    repo = SQLAlchemyMeetingRepository(orm_session)
    repo.add(meeting)
    orm_session.commit()

    saved_meetings = list(orm_session.execute(
        'SELECT title, time, deadline, max_participants FROM meetings'
    ))

    assert saved_meetings == [
        (
            "Cook with Beaver",
            dt.datetime(2024, 7, 1, 18, 0),
            dt.datetime(2024, 6, 30, 18, 0),
            5
        )
    ]

def test_repository_can_retrieve_a_meeting_with_participants(orm_session):
    meeting_id = insert_meeting(orm_session)
    insert_participant(orm_session, meeting_id)
    repo = SQLAlchemyMeetingRepository(orm_session)
    retrieved = repo.get(meeting_id)
    expected = Meeting(
        title="Learn Python",
        time=dt.datetime(2024, 8, 15, 10, 0),
        deadline=dt.datetime(2024, 8, 14, 10, 0),
        max_participants=10
    )

    assert retrieved == expected
    assert retrieved.participants_amount == 1
    assert retrieved.available_slots == 9
    assert retrieved._participants == {Participant(user_id=1)}