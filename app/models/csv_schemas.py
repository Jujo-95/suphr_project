from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: Optional[str]
    department_id: int
    job_id: int

class DepartmentsCreate(BaseModel):
    id: int
    department: str

class JobsCreate(BaseModel):
    id: int
    job: str