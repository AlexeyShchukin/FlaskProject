# Задача 2. Создание модели Salon
# Создать модель элитного бутика. Поля:
#
# id: PK
# name: название
# location: строка
# Пара (name, location) должна быть уникальна.
from sqlalchemy import Integer, String, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from practicum.practicum_2.task3 import Shipment
from sqlalchemy_lessons import Base


class Salon(Base):
    __tablename__ = "salons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(150))

    __table_args__ = (
        UniqueConstraint('name', 'location', name='unq_name_location'),
        Index('idx_name_location', 'name', 'location')
    )

    shipments_info: Mapped[list["Shipment"]] = relationship(
        "Shipment",
        secondary="salon_shipment_association",
        backpopulates="salons_info")