from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

GRADE_TO_POINTS = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentData(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/gpa")
async def calculate_gpa(data: StudentData):
    total_points = 0.0
    total_credits = 0

    for course in data.courses:
        grade_point = GRADE_TO_POINTS.get(course.grade, 0.0)
        total_points += grade_point * course.credits
        total_credits += course.credits

    gpa = round(total_points / total_credits + 1e-8, 3) if total_credits else 0.0

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
