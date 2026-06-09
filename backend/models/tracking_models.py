from pydantic import BaseModel
from typing import List

class StudyLog(BaseModel):
    user_id: int
    subject: str
    hours: float
    date: str  # YYYY-MM-DD

class QuizResult(BaseModel):
    user_id: int
    subject: str
    score: int
    date: str  # YYYY-MM-DD
    days_to_exam: int
