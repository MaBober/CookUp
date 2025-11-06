import datetime as dt

from orm import start_mappers
from model import Meeting


def test_meetings_mapper_can_load_meetings(orm_session):

    orm_session.execute(
        'INSERT INTO meetings (id, title, time, deadline, max_participants) VALUES',
        '(1, "Cook with Beaver", "2024-07-01 18:00:00", "2024-06-30 18:00:00", 5),'
        '(2, "Bake a Cake", "2024-07-02 15:00:00", NULL, 10);'
    )

    excepted_meetings = [
        Meeting(
            title="Cook with Beaver",
            time=dt.datetime(2024, 7, 1, 18, 0),
            deadline=dt.datetime(2024, 6, 30, 18, 0),
            max_participants=5
        ),
        Meeting(
            title="Bake a Cake",
            time=dt.datetime(2024, 7, 2, 15, 0),
            deadline=None,
            max_participants=10
        )
    ]

    assert orm_session.query(Meeting).all() == excepted_meetings

def test_meetings_mapper_can_save_meetings(orm_session):

    meeting = Meeting(
        title="Cook with Beaver",
        time=dt.datetime(2024, 7, 1, 18, 0),
        deadline=dt.datetime(2024, 6, 30, 18, 0),
        max_participants=5
    )

    orm_session.add(meeting)
    orm_session.commit()

    saved_meetings = list(orm_session.execute(
        'SELECT title, time, deadline, max_participants FROM meetings WHERE id = :id',
        {'id': meeting.id}
    ))

    assert saved_meetings == [
        (
            "Cook with Beaver",
            dt.datetime(2024, 7, 1, 18, 0),
            dt.datetime(2024, 6, 30, 18, 0),
            5
        )
    ]