from pydantic import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from sqlalchemy_lessons import Base


class User(Base):
    __tablename__ = "user"
    id: int = mapped_column(Integer, primary_key=True)
    name: str = mapped_column(String(20))
    age: int = mapped_column(Integer, nullable=True)


class UserCreateSchema(BaseModel):
    name: str
    age: int | None = None

    model_config = {
        "from_attributes": True
    }


user_input_data = {  # Raw data
    "name": "Alice",
    "age": 34
}

validated_data = UserCreateSchema.model_validate(user_input_data).model_dump()

user = User(**validated_data)

session.add(user)
session.commit()
session.close()
