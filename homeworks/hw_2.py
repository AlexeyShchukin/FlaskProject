import re

from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    @classmethod
    def validate_user(cls, model):
        if not re.match(r"^[A-Za-z ]+$", model.name):
            raise ValueError("Name must contain only letters. Space is allowed")
        if model.is_employed and model.age not in range(18, 66):
            raise ValueError("Inadmissible age for employment")
        return model


json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""


def validate_data(data: str):
    user_object = User.model_validate_json(data)
    return user_object.model_dump_json()


if __name__ == '__main__':
    print(validate_data(json_input))
