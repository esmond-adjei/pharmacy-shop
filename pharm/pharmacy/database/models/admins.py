from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from pharmacy.database.core import Base


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __str__(self):
        return f"<Admin>: {self.username}"
