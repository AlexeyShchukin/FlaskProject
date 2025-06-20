from decimal import Decimal
from pprint import pprint

from sqlalchemy import create_engine, String, Boolean, Numeric, ForeignKey, select, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship, selectinload

engine = create_engine("sqlite:///:memory:")

session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    __abstract__ = True


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


Base.metadata.create_all(engine)

# Задача 1: Наполнение данными
with session_maker() as session:
    electronic = Category(name="Электроника", description="Гаджеты и устройства.")
    books = Category(name="Книги", description="Печатные книги и электронные книги.")
    clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    session.add_all([books, electronic, clothes])

    products = [
        Product(name="Смартфон", price=Decimal("299.99"), in_stock=True, category=electronic),
        Product(name="Ноутбук", price=Decimal("499.99"), in_stock=True, category=electronic),
        Product(name="Научно-фантастический роман", price=Decimal("15.99"), in_stock=True, category=books),
        Product(name="Джинсы", price=Decimal("40.50"), in_stock=True, category=clothes),
        Product(name="Футболка", price=Decimal("20.00"), in_stock=True, category=clothes)
    ]
    session.add_all(products)
    session.commit()

    print()
    print("===== Задача 2: Чтение данных =====")
    print()

    stmt = select(Category).options(selectinload(Category.products))
    result = session.execute(stmt).scalars().all()

    for category in result:
        print(f"{category.name}:")
        for product in category.products:
            print(f"    {product.name} - {product.price}€")

    print()
    print("===== Задача 3: Обновление данных =====")
    print()

    stmt = select(Product).where(Product.name == "Смартфон")
    product = session.execute(stmt).scalars().first()
    product.price = Decimal("349.99")

    session.flush()
    session.refresh(product)

    print(f"{product.name} - {product.price}€")

    print()
    print("===== Задача 4: Агрегация и группировка =====")
    print()

    stmt = select(
        Category.name,
        func.count(Product.id).label("count_products"),
    ).join(Product).group_by(Category.name)

    result = session.execute(stmt).all()

    for category in result:
        print(f"{category.name} - {category.count_products}")

    print()
    print("===== Задача 5: Группировка с фильтрацией =====")
    print()

    stmt = select(
        Category.name,
        func.count(Product.id).label("count_products")
    ).join(Product
           ).group_by(Category.name
                      ).having(func.count(Product.id) > 1)

    result = session.execute(stmt).all()

    for category in result:
        print(f"{category.name} - {category.count_products}")
