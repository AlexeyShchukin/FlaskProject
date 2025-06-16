from decimal import Decimal

from sqlalchemy import create_engine, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship

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

with session_maker() as session:
    category = Category(name="Sport", description="Sport goods")
    product = Product(
        name="Power Tower Adidas Performance",
        price=Decimal("399.99"),
        in_stock=True,
        category=category
    )

    session.add(category)
    session.add(product)

    session.commit()

    products = session.query(Product).join(Product.category).all()
    for p in products:
        print(f"[{p.category.name}] {p.name}: {p.price} Euro")
