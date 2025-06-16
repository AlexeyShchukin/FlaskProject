# Задача 1. Создание модели Mineral
# Создать таблицу минералов с полями:
#
#     id: PK
#     name: уникальное имя (строка, макс. 50)
#     color: строка
#     hardness: значение по шкале Мооса, float
from uuid import uuid4, UUID

from sqlalchemy import UUID as sa_uuid, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from practicum.practicum_2.task3 import Shipment
from sqlalchemy_lessons import Base


class Mineral(Base):
    __tablename__ = "minerals"
    id: Mapped[UUID] = mapped_column(
        sa_uuid(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(50))
    hardness: Mapped[float] = mapped_column(Float)

    shipments_info: Mapped[list["Shipment"]] = relationship("Shipment", back_populates="mineral_info")


