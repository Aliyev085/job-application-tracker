from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Status(str, Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    company: str
    position: str
    status: Status = "applied"
    applied_date: date | None = None
    notes: str | None = None


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    position: str
    status: str
    applied_date: date
    notes: str | None


class ApplicationUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    company: str | None = None
    position: str | None = None
    status: Status | None = None
    applied_date: date | None = None
    notes: str | None = None