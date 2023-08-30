from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pharmacy.database.core import Base


class Inventory(Base):
    __tablename__ = 'inventories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def __str__(self):
        return f"<Item>: {self.name}"
