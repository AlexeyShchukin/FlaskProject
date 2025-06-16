# Задача 7. Связь Salon и Shipment через M2M
#
# Один Shipment может быть доставлен в несколько салонов
# Один Salon может принимать разные Shipment
# Настроить Many-to-Many через таблицу salon_shipment_association
from sqlalchemy import Table, Column, ForeignKey

from sqlalchemy_lessons import Base

salon_shipment_association = Table(
    "salon_shipments",
    Base.metadata,
    Column("salon_id", ForeignKey("salons.id"), primary_key=True),
    Column("shipment_id", ForeignKey("shipments.id"), primary_key=True)
)

