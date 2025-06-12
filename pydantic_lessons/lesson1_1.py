from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class TestType(StrEnum):
    BLOOD = "blood"
    XRAY = "xray"
    MRI = "mri"


class LabTestBase(BaseModel):
    patient_id: int
    test_type: TestType
    test_date: date


class LabTestRequest(LabTestBase):
    notes: str | None = None


class LabTestResponse(LabTestBase):
    id: int
    result: str | None = None
    is_completed: bool

    def is_urgent(self) -> bool:
        if not self.result:
            return False

        if "гемоглобин" in self.result.lower():
            match_patt = re.search(r"(\d+)\s*г/л", self.result.lower())

            if match_patt:
                value = int(match_patt.group(1))
                return value < 80 or value > 150

        return False


request_data = {
    "patient_id": 101,
    "test_type": "blood",
    "test_date": "2025-06-11",
    "notes": "Анализ натощак"
}

response_data = {
    "id": 5001,
    "patient_id": 101,
    "test_type": "blood",
    "test_date": "2025-06-11",
    "is_completed": True,
    "result": "Гемоглобин: 50 г/л"
}

valid_request = LabTestRequest(**request_data)
valid_response = LabTestResponse(**response_data)

print(valid_request)
print(valid_response)

print({"urgent": valid_response.is_urgent()})
