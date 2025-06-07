from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 점수 데이터를 받을 모델
class GradeInput(BaseModel):
    score: int
    credit: int  # 지금은 사용하지 않지만 받아둠

class GradesRequest(BaseModel):
    grades: List[GradeInput]

# 변환 결과 모델
class GradeResult(BaseModel):
    score: int
    grade: str

class GradesResponse(BaseModel):
    results: List[GradeResult]

# 점수 → 등급 매핑 함수
def convert_to_grade(score: int) -> str:
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A0"
    elif score >= 85:
        return "B+"
    elif score >= 80:
        return "B0"
    elif score >= 75:
        return "C+"
    elif score >= 70:
        return "C0"
    elif score >= 65:
        return "D+"
    elif score >= 60:
        return "D0"
    else:
        return "F"

@app.post("/grades", response_model=GradesResponse)
def get_grades(data: GradesRequest):
    results = []
    for item in data.grades:
        grade = convert_to_grade(item.score)
        results.append({"score": item.score, "grade": grade})
    return {"results": results}
