from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import EventStatus


# ---------- USER SCHEMAS ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# ---------- TOKEN SCHEMAS ----------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


# ---------- EVENT SCHEMAS ----------
class EventBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    title: str
    start_time: datetime
    end_time: datetime
    status: EventStatus = EventStatus.BUSY


class EventUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[EventStatus] = None


class EventResponse(EventBase):
    id: int
    status: str
    owner_id: int

    class Config:
        orm_mode = True


# ---------- SWAP REQUEST SCHEMAS ----------
class SwapRequestCreate(BaseModel):
    my_slot_id: int
    their_slot_id: int


class SwapResponseAction(BaseModel):
    accepted: bool


class SwapRequestResponse(BaseModel):
    id: int
    requester_id: int
    responder_id: int
    my_slot_id: int
    their_slot_id: int
    status: str

    class Config:
        orm_mode = True
