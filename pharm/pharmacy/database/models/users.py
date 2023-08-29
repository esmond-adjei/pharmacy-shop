from datetime import date

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Date

from pharmacy.database.core import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    date_or_birth: Mapped[date | None] = mapped_column(Date)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<User>: {self.username}'
