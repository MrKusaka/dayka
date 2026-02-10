from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class Weekday(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class TaskAdd(BaseModel):
    weekday: Weekday
    title: str
