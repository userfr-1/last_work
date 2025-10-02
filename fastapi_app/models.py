from pydantic import BaseModel
from typing import Optional, List

class Student(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: Optional[str] = None
    group: Optional[List[str]] = []
    is_line: bool = False
    descriptions: Optional[str] = None
