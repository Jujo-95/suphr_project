from pydantic import BaseModel
from datetime import datetime


class EmployeeCreate(BaseModel):
    id: float
    name: str
    datetime: str
    department_id: float
    job_id: float


class DepartmentsCreate(BaseModel):
    id: int
    department: str

class JobsCreate(BaseModel):
    id: int
    job: str