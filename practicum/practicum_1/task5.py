# Создать класс, который принимает данные пользователя в формате JSON и валидирует их на уровне типов данных.
#
#
# Данные включают:
# имя пользователя
# возраст
# email
# адрес (город, улица, номера дома)
# \
from pydantic import EmailStr, BaseModel, ValidationError

from pydantic_lessons.lesson1 import Address

json_string = """{
    "name": "John Doe",
    "age": 22,
    "email": "john.doe@example.com",
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Address

try:
    user_object = User.model_validate_json(json_string)
    print(user_object)
    print(user_object.age)
    print(user_object.model_dump_json(indent=4))
except ValidationError as e:
    print(e)
