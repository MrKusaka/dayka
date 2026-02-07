from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class Weekday(str, Enum):
    MONDAY = "monday"
    user = "user"
    guest = "guest"


class TaskAdd(BaseModel):
    weekday: Weekday = Field(
        example=Weekday.MONDAY,  # Ключевой параметр!
        description="Выберите день недели"
    )
    title: str
