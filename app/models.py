from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class EventStatus(str, enum.Enum):
    BUSY = "BUSY"
    SWAPPABLE = "SWAPPABLE"
    SWAP_PENDING = "SWAP_PENDING"

class SwapStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    events = relationship("Event", back_populates="owner")
    sent_requests = relationship("SwapRequest", back_populates="requester", foreign_keys="SwapRequest.requester_id")
    received_requests = relationship("SwapRequest", back_populates="responder", foreign_keys="SwapRequest.responder_id")


class Event(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.BUSY, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"))
    responder_id = Column(Integer, ForeignKey("users.id"))
    my_slot_id = Column(Integer, ForeignKey("Events.id"))
    their_slot_id = Column(Integer, ForeignKey("Events.id"))
    status = Column(Enum(SwapStatus), default=SwapStatus.PENDING)

    requester = relationship("User", back_populates="sent_requests", foreign_keys=[requester_id])
    responder = relationship("User", back_populates="received_requests", foreign_keys=[responder_id])
    my_slot = relationship("Event", foreign_keys=[my_slot_id])
    their_slot = relationship("Event", foreign_keys=[their_slot_id])
