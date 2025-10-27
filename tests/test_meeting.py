import pytest
import datetime as dt

base_now = dt.datetime.now()

meeting_data = {
    "title": "Gotuj z Boberem",
    "time": base_now + dt.timedelta(days=80),
    "deadline": base_now + dt.timedelta(days=79),
    "max_participants": 10
}

def test_joining_meeting_reduces_available_slots():

    meeting = Meeting(
        title=meeting_data["title"],
        time=meeting_data["time"],
        deadline=meeting_data["deadline"],
        max_participants=meeting_data["max_participants"]
    )

    participant = Participant(user_id=1)

    initial_slots = meeting.available_slots
    meeting.join(participant)
    assert meeting.available_slots == initial_slots - 1

def test_joining_full_meeting_raises_exception():

    meeting = Meeting(
        title=meeting_data["title"],
        time=meeting_data["time"],
        deadline=meeting_data["deadline"],
        max_participants=1
    )
    participant_1 = Participant(user_id=1)
    participant_2 = Participant(user_id=2)
    meeting.join(participant_1)

    with pytest.raises(MeetingFullException):
        meeting.join(participant_2)

def test_joining_after_time_limit_raises_exception():

    meeting = Meeting(
        title=meeting_data["title"],
        time=base_now + dt.timedelta(days=2),
        deadline=base_now + dt.timedelta(days=-1),
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)

    with pytest.raises(CannotJoinAfterDeadlineException):
        meeting.join(participant)

def test_user_can_join_on_time_limit():
    meeting = Meeting(
        title=meeting_data["title"],
        time=base_now + dt.timedelta(days=2),
        deadline=base_now,
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)

    meeting.join(participant)
    assert meeting.available_slots == meeting_data["max_participants"] - 1

def test_leaving_meeting_increases_available_slots():

    meeting = Meeting(
        title=meeting_data["title"],
        time=meeting_data["time"],
        deadline=meeting_data["deadline"],
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)
    meeting.join(participant)

    meeting.leave(participant)
    assert meeting.available_slots == meeting_data["max_participants"]

def test_user_cannot_join_meeting_twice():
    meeting = Meeting(
        title=meeting_data["title"],
        time=meeting_data["time"],
        deadline=meeting_data["deadline"],
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)
    meeting.join(participant)

    with pytest.raises(UserAlreadyJoinedException):
        meeting.join(participant)

def test_user_cannot_leave_meeting_after_time_limit():
    meeting = Meeting(
        title=meeting_data["title"],
        time=base_now + dt.timedelta(days=2),
        deadline=base_now + dt.timedelta(days=1),
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)
    meeting.deadline = base_now - dt.timedelta(minutes=1)
    meeting.join(participant)

    with pytest.raises(CannotLeaveAfterDeadlineException):
        meeting.leave(participant)

def user_can_leave_meeting_on_time_limit():
    meeting = Meeting(
        title=meeting_data["title"],
        time=base_now + dt.timedelta(days=2),
        deadline=base_now,
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)
    meeting.join(participant)

    meeting.leave(participant)
    assert meeting.available_slots == meeting_data["max_participants"]
    

def test_user_cannot_leave_meeting_if_not_joined():
    meeting = Meeting(
        title=meeting_data["title"],
        time=meeting_data["time"],
        deadline=meeting_data["deadline"],
        max_participants=meeting_data["max_participants"]
    )
    participant = Participant(user_id=1)

    with pytest.raises(UserNotJoinedException):
        meeting.leave(participant)
