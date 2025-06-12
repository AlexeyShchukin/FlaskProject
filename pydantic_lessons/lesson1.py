from pydantic import BaseModel


class Address(BaseModel):
    city: str
    street: str
    house_number: int
    index: int = None


class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True
    address: Address


address = Address(city="NY", street="Some-street", house_number=13, index=6000)
user = User(id=2, name="Alex", age=27, address=address)

if __name__ == '__main__':
    print(user)
    print(user.address.city)
