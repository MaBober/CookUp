import datetime as dt

from dataclasses import dataclass
from typing import Optional

from errors import (
    MeetingFullException,
    CannotJoinAfterDeadlineException, 
    CannotLeaveAfterDeadlineException,
    UserNotJoinedException,
    UserAlreadyJoinedException
)
from utils import normalize_to_minutes

class User:
    def __init__(self, first_name: str, last_name: str, email: str):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        

@dataclass(frozen=True)
class Participant:
    user_id: int


class Meeting:
    def __init__(self, title: str, time: dt.datetime, deadline: Optional[dt.datetime], max_participants: int):
        self.id = None
        self.title = title
        self.time = normalize_to_minutes(time)
        self.deadline = normalize_to_minutes(deadline) if deadline else None
        self.max_participants = max_participants
        self._participants = set()

    def _ensure_can_join(self, participant: Participant) -> None:
        if self.participants_amount >= self.max_participants:
            raise MeetingFullException()

        if self.deadline and normalize_to_minutes(dt.datetime.now()) > self.deadline:
            raise CannotJoinAfterDeadlineException()
        
        if participant in self._participants:
            raise UserAlreadyJoinedException()
        
    def _ensure_can_leave(self, participant: Participant) -> None:
        if self.deadline and normalize_to_minutes(dt.datetime.now()) > self.deadline:
            raise CannotLeaveAfterDeadlineException()

        if participant not in self._participants:
            raise UserNotJoinedException()

    def join(self, participant: Participant) -> bool:

        self._ensure_can_join(participant)
        self._participants.add(participant)

        return True

    def leave(self, participant: Participant) -> bool:

        self._ensure_can_leave(participant)
        self._participants.remove(participant)

        return True
    
    @property
    def available_slots(self) -> int:
        return self.max_participants - self.participants_amount
    
    @property
    def participants_amount(self) -> int:
        return len(self._participants)



