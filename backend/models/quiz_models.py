from pydantic import BaseModel
from typing import List

class StudyContent(BaseModel):
    user_id: int
    subject: str
    content: str

from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel
from typing import List, Dict, Optional


class QuizRequest(BaseModel):
    user_id: int
    subject: str
    difficulty: str

    mcq_count: int = 5
    short_count: int = 2
    long_count: int = 1

    multi_select: bool = False


class EvalRequest(BaseModel):
    correct_answers: Dict
    student_answers: Dict
