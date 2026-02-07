from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class TasksOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    weekday: Mapped[str]
    is_done: Mapped[bool] = mapped_column(default=False)