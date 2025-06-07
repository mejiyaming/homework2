from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Subject(BaseModel):
    name: str
    credit: int
    grade: str

class GPARequest(BaseModel):
    subjects: List[Subject]

class GPAResponse(BaseModel):
    gpa: float

grade_to_point = {
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

@app.post("/calculate-gpa", response_model=GPAResponse)
def calculate_gpa(data: GPARequest):
    total_points = 0.0
    total_credits = 0

    for subject in data.subjects:
        point = grade_to_point.get(subject.grade.upper(), 0.0)
        total_points += point * subject.credit
        total_credits += subject.credit

    if total_credits == 0:
        return {"gpa": 0.0}

    gpa = total_points / total_credits
    return {"gpa": round(gpa, 2)}
