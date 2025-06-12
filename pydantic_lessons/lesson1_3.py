from datetime import datetime

from pydantic import BaseModel, HttpUrl, EmailStr, Field, field_validator, ValidationError

from pydantic_lessons.lesson1_2 import Product


class User(BaseModel):
    full_name: str
    age: int
    email: EmailStr
    homepage: HttpUrl
    # products: list[Product] = []  # WRONG!!!
    products: list[Product] = Field(default_factory=list)

    class Config:
        str_strip_whitespace = True  # удаляет справа и слева все пробелы
        validate_assignment = True  # валидация изменений уже созданных объектов
        json_encoders = {
            datetime: lambda value: value.strftime("%d-%m-%Y %H:%M")
        }

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        allowed_domains = {'example.com', 'gmail.com'}
        email_domain = value.split('@')[-1]
        if email_domain not in allowed_domains:
            raise ValidationError('Email must be  form one of  allowed domains: {" , ".join(allowed_domains)}")"')
        return value


user = User(
    full_name="J. Johanson",
    age=32,
    email="j.johanson@google.com",
    homepage="https://example.com"
)

user.email = "example@mail.ru"

print(user)
print(user.model_dump_json(indent=4))

# def foo(data: list | None = None):
#     if not data:
#         data = []
