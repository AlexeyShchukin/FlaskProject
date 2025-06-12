from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    description: str = Field(None, description="Product description")
    price: Decimal = Field(gt=0, max_digits=6, decimal_places=2)  # 1000.00
    in_stock: bool = Field(default=True, alias="available")


product = Product(
    name="Chair",
    price=Decimal("9.23"),
    available=False
)


if __name__ == '__main__':
    print(product)
    print(product.price)