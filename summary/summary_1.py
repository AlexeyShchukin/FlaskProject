# 🟦 ЗАДАЧА 1: Patient с alias и default_factory
# Создать базовую модель пациента с алиасами для
# first_name и last_name(CamelCase), и автоматическим временем регистрации.
#
# Требования:
# Поля: first_name, last_name (алиасы: firstName, lastName)
# Поле registration_time: генерируется автоматически через default_factory
# Включить populate_by_name = True
# Добавить описание в json_schema_extra

# 🟦 ЗАДАЧА 2: Валидация имён с field_validator
# Добавить очистку и форматирование имени и фамилии. Проверять
# минимальную длину строки.
#
# Требования:
# Использовать @field_validator для first_name и last_name
# Удалять пробелы по краям
# Преобразовывать к TitleCase
# Минимальная длина после обработки — 2 символа

# 🟦 ЗАДАЧА 3: Возрастная проверка с model_validator
# Добавить логическую проверку на необходимость медицинского
# обследования у мужчин 50+ лет.
#
# Требования:
# Добавить поля age: int, sex: str, cancer_exam_done: Optional[bool]
# Если age > 30, то cancer_exam_done обязательно True
# Использовать @model_validator(mode='after') для проверки зависимости полей
# Сохранить предыдущую валидацию имён

# 🟦 ЗАДАЧА 4: Врач как наследник Person
# Создать базу для врачей как наследников Person. Проверка лицензии.
#
# Требования:
# Базовая модель Person с first_name, last_name, age
# Подкласс Doctor с полями: specialization, license_id
# license_id должен начинаться с "MD-"
# Использовать @field_validator для валидации license_id


# 🟦 ЗАДАЧА 5: Вложенная модель Address в Patient
# Расширить пациента вложенным адресом и добавить валидацию ZIP-кода.
#
# Требования:
# Модель Address: city, street, zip_code
# Модель PatientWithAddress расширяет Patient, добавляет address: Address
# Проверка: zip_code — только 5 цифр
# Использовать @field_validator внутри модели Address

# 🟦 ЗАДАЧА 6: Визит в клинику с alias_generator и UUID
# Цель:
# Создать модель клинического визита с автогенерацией ID и алиасов.
#
# Требования:
# Поля: visit_id (UUID через default_factory), doctor_notes
# Использовать alias_generator (snake_case → camelCase)
# Алиас doctor_notes → notes
# Добавить populate_by_name, json_encoders, json_schema_extra

# 🟦 ЗАДАЧА 7: Условная обязательность поля на основе diagnoses
# Реализовать условную валидацию поля last_glucose_level, если
# среди диагнозов есть диабет.
#
# Требования:
# Поля: name, diagnoses: list[str], last_glucose_level: Optional[float]
# Если "diabetes" есть в списке диагнозов → last_glucose_level обязательно
# Валидация через @model_validator(mode='after')
# JSON-схема содержит пример

# 🟦 ЗАДАЧА 8: PatientWithInsurance с сериализацией UUID, Enum, Decimal, Path
#
# Создать модель пациента с медицинской страховкой, в которой
# используются типы:
#
# UUID (идентификатор)
# Enum (пол)
# Decimal (лимит покрытия)
# Path (путь к полису PDF-файла)
# Всё должно быть корректно сериализовано в JSON.

from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from uuid import UUID, uuid4
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError, model_validator


class Address(BaseModel):
    street: str
    city: str
    zipcode: str

    @field_validator("zipcode")
    @classmethod
    def validate_zipcode(cls, value):
        if not value.isdigit() or len(value) != 5:
            raise ValidationError("Zipcode must be 5 digits")


class Patient(BaseModel):
    first_name: str = Field(alias="FirstName")
    last_name: str = Field(alias="LastName")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    age: int
    sex: str
    cancer_exam_done: bool | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip().title()
        if len(value) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_age(cls, model):
        if model.sex == "m" and model.age > 50:
            model.cancer_exam_done = True
        return model

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
        json_schema_extra={
            "description": "Create Patient Schema",
            "type": "object",
            "properties": {},
            "required": ["first_name", "last_name"],
            "additionalProperties": False
        }
    )


class Doctor(Patient):
    specialization: str
    license_id: str

    @field_validator("license_id")
    @classmethod
    def validate_license_id(cls, value):
        if not value.startswith("MD-"):
            raise ValidationError("License ID must start with MD-")
        return value


class PatientWithAddress(Patient):
    address: Address


def to_camel(string: str) -> str:
    return re.sub(r'_([a-zA-Z])', lambda m: m.group(1).upper(), string)


class ClinicVisit(BaseModel):
    visit_id: UUID = Field(default_factory=uuid4)
    doctor_notes: str = Field(..., alias='notes')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={
            UUID: str
        },
        json_schema_extra={
            "example": {
                "visitId": "d3b07384-d9a8-4d32-bf25-98b0e4f2d72d",
                "notes": "Пациент жалуется на головную боль."
            }
        }
    )


class PatientDiagnosis(BaseModel):
    name: str
    diagnoses: list[str]
    last_glucose_level: float | None = None

    @model_validator(mode="after")
    @classmethod
    def check_glucose_level_for_diabetes(cls, model):
        if "diabetes" in model.diagnoses:
            raise ValidationError("last_glucose_level is required if patient has diabetes")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "diagnoses": ["diabetes", "hypertension"],
                "last_glucose_level": 5.8
            }
        }
    )


class Sex(StrEnum):
    male = "male"
    female = "female"


class PatientWithInsurance(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    sex: Sex
    coverage_limit: Decimal
    policy_path: Path

    model_config = ConfigDict(
        json_encoders={
            UUID: str,
            Decimal: float,
            Path: str
        }
    )


if __name__ == '__main__':
    patient = Patient(first_name="  john", last_name=" doe ", age=55, sex="m")
    get_patient = Patient.model_validate_json(patient.model_dump_json())
    print(patient)
    print(get_patient)

    doctor = Doctor(
        first_name="Vasya",
        last_name="pupkin",
        age=55,
        sex="m",
        specialization="Chirurg",
        license_id="MD-45467892"
    )
    print(doctor)

    address = Address(street="street", city="NY", zipcode="68003")
    patient_with_address = PatientWithAddress(
        first_name="bob",
        last_name="marly ",
        age=55,
        sex="m",
        address=address
    )
    print(patient_with_address)

    patient_with_insurance = PatientWithInsurance(
        sex=Sex.male,
        coverage_limit=Decimal("10000.50"),
        policy_path=Path("/path/to/policy.pdf")
    )

    print(patient_with_insurance.model_dump_json())
