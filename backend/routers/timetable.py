# # routers/timetable.py

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Optional
# from services.features import generate_features
# from services.planner import generate_weekly_timetable
# from datetime import datetime

# router = APIRouter(prefix="/timetable", tags=["Timetable"])

# # ------------------------------
# # Pydantic models for request
# # ------------------------------
# class StudyLog(BaseModel):
#     user_id: int
#     subject: str
#     hours: float
#     date: str  # "YYYY-MM-DD"

# class QuizResult(BaseModel):
#     user_id: int
#     subject: str
#     score: float
#     date: str  # "YYYY-MM-DD"
#     days_to_exam: Optional[int] = None  # optional, can be computed

# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str  # "morning", "evening", etc.
#     hobby: str
#     break_hours: float
#     exam_dates: Dict[str, str]  # {"Math": "2026-02-05"}
#     study_logs: List[StudyLog]
#     quiz_results: List[QuizResult]
#     daily_hours: Dict[str, float]  # {"Mon": 6, "Tue": 5, ...}

# # ------------------------------
# # Timetable generation endpoint
# # ------------------------------
# @router.post("/generate")
# def generate_timetable(request: TimetableRequest):
#     try:
#         # Convert request data to dicts
#         study_logs = [log.dict() for log in request.study_logs]
#         quiz_results = [quiz.dict() for quiz in request.quiz_results]
#         exam_dates = request.exam_dates

#         # ------------------------------
#         # Layer 3: Feature Engineering
#         # ------------------------------
#         features_df = generate_features(
#             study_logs=study_logs,
#             quiz_results=quiz_results,
#             exam_dates=exam_dates
#         )

#         # ------------------------------
#         # Layer 5–6: Generate timetable
#         # ------------------------------
#         timetable = generate_weekly_timetable(
#             features_df=features_df,
#             daily_hours=request.daily_hours,
#             break_hours=request.break_hours,
#             feasible_time=request.feasible_time,
#             hobby=request.hobby
#         )

#         # ------------------------------
#         # Return final timetable JSON
#         # ------------------------------
#         return {
#             "user_id": request.user_id,
#             "timetable": timetable
#         }

#     except Exception as e:
#         # Catch any unexpected errors
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import APIRouter
from models.timetable_models import TimetableRequest
from services.planner import generate_weekly_timetable

router = APIRouter(prefix="/timetable")

@router.post("/generate")
def generate_timetable(request: TimetableRequest):
    """
    Generate a weekly timetable based on:
    - Study logs
    - Quiz results
    - Exam dates
    - Daily hours
    - Hobbies
    - Feasible time
    """
    timetable = generate_weekly_timetable(request)
    return {"user_id": request.user_id, "timetable": timetable}







