from abc import ABC, abstractmethod

from model import Meeting

class AbstractRepository(ABC):

    @abstractmethod
    def add(self, entity):
        raise NotImplementedError()
    
    @abstractmethod
    def get(self, entity_id):
        raise NotImplementedError()

    
class SQLAlchemyMeetingRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, meeting):
        self.session.add(meeting)

    def get(self, meeting_id):
        return self.session.query(Meeting).filter_by(id=meeting_id).one()