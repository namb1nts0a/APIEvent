from sqlalchemy import Column, String, DateTime
from db import Base


class Event(Base):
    __tablename__ = "events"

    event_uid = Column(String, primary_key=True, index=True) # facilitation du recherche ou indexation
    event_timestamp = Column(DateTime)
    event_data = Column(String)