# Задача 3. Создание модели Shipment
# Модель поставки минерала. Поля:
#
# id: PK
# shipment_date: дата
# destination: строка
# mineral_id: FK
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from practicum.practicum_2.task1 import Mineral
from practicum.practicum_2.task2 import Salon
from sqlalchemy_lessons import Base


class Shipment(Base):
    __tablename__ = "shipments"
    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_data: Mapped[datetime] = mapped_column(DateTime)
    destination: Mapped[str] = mapped_column(String(150))
    mineral_id: Mapped[UUID] = mapped_column(ForeignKey("mineral.id"))  # O2M (one to many)

    mineral_info: Mapped["Mineral"] = relationship("Mineral", back_populates="shipment_info")
    salons_info: Mapped[list["Salon"]] = relationship(
        "Salon",
        secondary="salon_shipment_association",
        back_populates="shipments_info"
    )