# models/progress_models.py
from pydantic import BaseModel
from typing import List

class SlotProgress(BaseModel):
    subject: str
    start_time: str
    end_time: str
    type: str  # study / break / revision
    completed: bool = False

class DailyProgress(BaseModel):
    user_id: int
    date: str
    slots: List[SlotProgress]

class WeeklyProgressReport(BaseModel):
    user_id: int
    week_start: str
    week_end: str
    total_planned_hours: float
    total_completed_hours: float
    subject_wise_completion: dict  # e.g., {"Math": 4/6, "Physics": 3/6}
