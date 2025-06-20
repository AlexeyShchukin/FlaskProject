# Aufgabe 2: Stellen Sie eine Verbindung zu einer lokalen SQLite3-Datenbank her.
# Was können Sie über create_engine() sagen?
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, selectinload

url = "sqlite:///:memory:"
engine = create_engine(url, echo=True)


class Base(DeclarativeBase):
    __abstract__ = True


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    country: Mapped[str] = mapped_column(String(50))


# Aufgabe 3: Erstellen Sie ein Modell Bank, das Banken darstellt.
# Die Modellklasse soll folgende Felder enthalten:
# id: Primärschlüssel, Ganzzahl
# name: Name der Bank, Zeichenkette
# address: Adresse der Bank, Zeichenkette
# swift_code: SWIFT-Code, Zeichenkette
# rating: Bewertung, Ganzzahl (z. B. von 1 bis 5)
# Erstellen Sie danach die Tabelle in der Datenbank und fügen Sie 3 Datensätze hinzu.

class Bank(Base):
    __tablename__ = "banks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(255))
    swift_code: Mapped[str] = mapped_column(String(50))
    rating: Mapped[int] = mapped_column(Integer)

    branches: Mapped[list["Branch"]] = relationship("Branch", back_populates="bank")

    def __repr__(self):
        return f"Bank: {self.id=} {self.name=} {self.address=} {self.swift_code=}, {self.rating=}"


# Aufgabe 5: Erstellen Sie ein Modell Branch, das Bankfilialen darstellt.
# Es soll folgende Felder enthalten:
# id: Primärschlüssel
# bank_id: Fremdschlüssel, verweist auf Bank.id
# name: Name der Filiale
# address: Adresse der Filiale
# phone: Telefonnummer (optional)
# Richten Sie eine „Viele-zu-Eins“-Beziehung zwischen Filiale und Bank ein
# sowie eine „Eins-zu-Viele“-Beziehung von Bank zu Filialen.


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.id"))

    bank: Mapped["Bank"] = relationship("Bank", back_populates="branches")


Base.metadata.create_all(engine)

person = Person(
    name="Alex",
    age=37,
    country="Germany"
)

session = Session(engine)
session.add(person)
session.commit()

stmt = session.query(Person)
raw = session.execute(stmt).scalars().first()

print(raw.__dict__)

session.close()

banks = [
    Bank(name="Sparkasse Berlin", address="Alexanderplatz 1, 10178 Berlin", swift_code="SPKBDEBBXXX", rating=4),
    Bank(name="Deutsche Bank", address="Taunusanlage 12, 60325 Frankfurt", swift_code="DEUTDEFFXXX", rating=5),
    Bank(name="Commerzbank", address="Kaiserstraße 16, 60311 Frankfurt", swift_code="COBADEFFXXX", rating=4),
]

session = Session(engine)
session.add_all(banks)
session.commit()

new_bank = Bank(
    name="Testbank AG",
    address="Hauptstraße 1, 12345 Musterstadt",
    swift_code="TESTDEFFXXX",
    rating=4,
    branches=[
        Branch(name="Testbank Nord", address="Nordstraße 10, 12345 Musterstadt", phone="030-123456"),
        Branch(name="Testbank Süd", address="Südallee 5, 12345 Musterstadt", phone="030-789765")
    ]
)

session = Session(engine)
session.add(new_bank)

stmt = session.query(
    Bank.name,
    Branch.name.label("branch_name"),
    Branch.address.label("branch_address")
).options(
    selectinload(Bank.branches)
)
result = session.execute(stmt).all()

for b in result:
    print(b.name, b.branch_name, b.branch_address)
