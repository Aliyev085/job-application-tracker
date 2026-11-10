from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine


class Base(DeclarativeBase):
    pass


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="applied")
    applied_date: Mapped[date] = mapped_column(Date, default=date.today)
    notes: Mapped[str | None] = mapped_column(Text)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Table created!")