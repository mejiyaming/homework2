from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from decimal import Decimal, ROUND_HALF_UP

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

    gpa = 0.0
    if total_credits > 0:
        raw_gpa = total_points / total_credits
        gpa = float(Decimal(str(raw_gpa)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))  # <- 요기 바뀐 부분!

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
