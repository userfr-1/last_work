import json
from fastapi import FastAPI, HTTPException
from .models import Student
from pathlib import Path

app = FastAPI(title="FastAPI Student CRUD")

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "storage.json"


if not FILE_PATH.exists():
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)


def read_students():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_students(students):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)


@app.post("/students/", response_model=Student)
def create_student(student: Student):
    students = read_students()


    if any(s["id"] == student.id for s in students):
        raise HTTPException(status_code=400, detail="Bunday ID mavjud")

    students.append(student.dict())
    write_students(students)
    return student


@app.get("/students/")
def get_students():
    return read_students()
