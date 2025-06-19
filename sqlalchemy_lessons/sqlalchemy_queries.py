from datetime import datetime, timezone
from typing import Any

from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session

from sqlalchemy_lessons import engine
from sqlalchemy_lessons.db_connector import DBConnector
from sqlalchemy_lessons.social_blogs_models import User
from sqlalchemy_lessons.social_blogs_schemas import UserResponseSchema, UserUpdateSchema


def create_user(session: Session, raw_data: dict[str, Any]) -> UserResponseSchema:
    try:
        validated_data = UserResponseSchema.model_validate(raw_data)

        user = User(**validated_data.model_dump())

        session.add(user)

        # если нужен объект в сессии дальше, вместо коммита используем флаш и рефреш
        session.flush()  # загружает объект в базу без коммита
        session.refresh(user)  # зафиксирует объект в базе

        session.commit()

        return UserResponseSchema.model_validate(user)
    except ValueError as err:
        raise err
    except(IntegrityError, DataError) as db_err:
        session.rollback()
        raise db_err


def get_user_by_id(session: Session, user_id: int) -> UserResponseSchema:
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return UserResponseSchema.model_validate(user)


def update_user(session: Session, user_id: int, raw_data: dict[str, Any]) -> UserResponseSchema:
    user = session.get(User, user_id)  # NEW
    if not user:
        raise ValueError("User not found")

    validated_data = UserUpdateSchema.model_validate(raw_data)

    for field, value in validated_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    session.flush()
    session.refresh(user)
    session.commit()

    return UserResponseSchema.model_validate(user)


def delete_user(session: Session, user_id: int) -> dict[str, str]:
    user = session.get(User, user_id)  # NEW
    if not user:
        raise ValueError("User not found")

    session.delete(user)
    session.commit()

    return {"message": "User was successfully deleted"}


with DBConnector(engine=engine) as session:
    data = {
        "first_name": "Alex",
        "last_name": "Grey",
        "email": "a.grey@gmail.com",
        "password": "MySecurePassword",
        "repeat_password": "MySecurePassword",
        "phone": "+1 255 777 9999",
        "role_id": 3
    }

    try:
        new_user = create_user(session=session, raw_data=data)

        print("🟢 User Created!")
        print(new_user.model_dump_json(indent=4))
    except Exception as err:
        print(f"Error: {err}")

with DBConnector(engine=engine) as session:
    try:
        user = get_user_by_id(session=session, user_id=1)

        print("🟢 User found!")
        print(user.model_dump_json(indent=2))
    except ValueError as err:
        print(err)

with DBConnector(engine=engine) as session:
    try:
        updated_user = update_user(
            session=session,
            user_id=27,
            raw_data={
                "last_name": "UPDATED LASTNAME",
                "rating": 5.8,
                "updated_at": datetime.now(tz=timezone.utc)
            }
        )

        print("🟢 User found and updated!")
        print(updated_user.model_dump_json(indent=3))
    except ValueError as err:
        print(err)
