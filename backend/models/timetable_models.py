# from pydantic import BaseModel
# from typing import List, Dict
# from .tracking_models import StudyLog, QuizResult  # ✅ import them correctly

# class TimetableSlot(BaseModel):
#     subject: str
#     start_time: str  # e.g., "09:00"
#     end_time: str    # e.g., "11:00"
#     type: str        # "study", "break", "revision", "hobby"

# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str
#     hobbies: List[str]
#     break_hours: float
#     exam_dates: Dict[str, str]  # subject: date
#     study_logs: List[StudyLog]
#     quiz_results: List[QuizResult]
#     daily_hours: Dict[str, float]  # "Mon": 6, "Tue": 5, etc.


# # backend/models/timetable_models.py
# from pydantic import BaseModel
# from typing import List, Dict, Optional

# class StudyLog(BaseModel):
#     user_id: int
#     subject: str
#     hours: int
#     date: str

# # Each slot in the timetable
# class TimetableSlot(BaseModel):
#     day: str          # e.g., "Mon", "Tue"
#     start_time: str   # e.g., "08:00"
#     end_time: str     # e.g., "10:00"
#     subject: str
#     type: str         # "study", "break", "hobby", etc.

# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str
#     hobbies: List[str]
#     break_hours: int
#     exam_dates: Dict[str, str]     # e.g., {"Math": "2026-02-05"}
#     study_logs: List[StudyLog]
#     daily_hours: Dict[str, int]    # e.g., {"Mon": 6, "Tue": 6}







# final


# from typing import List, Dict, Optional
# from pydantic import BaseModel

# # Study logs sent by user
# class StudyLog(BaseModel):
#     user_id: int
#     subject: str
#     hours: int  # must be integer
#     date: str  # "YYYY-MM-DD"

# # Exam info
# class QuizResult(BaseModel):
#     subject: str
#     days_to_exam: int

# # Individual timetable slot
# class TimetableSlot(BaseModel):
#     subject: str
#     start_time: str
#     end_time: str
#     type: str  # "study", "break", "revision"

# # Main request for timetable generation
# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str  # e.g., "09:00-21:00"
#     hobbies: List[str]
#     break_hours: int
#     study_logs: List[StudyLog]
#     daily_hours: Dict[str, int]  # e.g., {"Mon":6, "Tue":6, ...}
#     quiz_results: Optional[List[QuizResult]] = []








# from pydantic import BaseModel
# from typing import List, Dict

# class StudyLog(BaseModel):
#     user_id: int
#     subject: str
#     hours: int
#     date: str  # YYYY-MM-DD

# class TimetableSlot(BaseModel):
#     subject: str
#     start_time: str  # HH:MM
#     end_time: str    # HH:MM
#     type: str        # study / break / revision

# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str  # e.g., "09:00-21:00"
#     hobbies: List[str]
#     break_hours: float
#     daily_hours: Dict[str, float]  # e.g., {"Mon":6, "Tue":6, ...}
#     study_logs: List[StudyLog]
#     exam_dates: Dict[str, str]  # subject -> exam date (YYYY-MM-DD)









# from pydantic import BaseModel
# from typing import List, Dict, Optional

# class StudyLog(BaseModel):
#     user_id: int
#     subject: str
#     hours: int  # integer hours
#     date: str  # "YYYY-MM-DD"

# class ExamDate(BaseModel):
#     subject: str
#     date: str  # "YYYY-MM-DD"

# class TimetableSlot(BaseModel):
#     subject: str
#     start_time: str
#     end_time: str
#     type: str  # "study", "break", "revision"

# class TimetableRequest(BaseModel):
#     user_id: int
#     feasible_time: str  # "09:00-21:00"
#     hobbies: List[str]
#     break_hours: float  # hours per break
#     daily_hours: Dict[str, float]  # e.g., {"Mon": 6, "Tue": 6, ...}
#     study_logs: List[StudyLog]
#     exam_dates: List[ExamDate]








# final 2
from pydantic import BaseModel
from typing import List, Optional, Dict


class StudyLog(BaseModel):
    user_id: int
    subject: str
    hours: int
    date: str


class ExamDate(BaseModel):
    subject: str
    date: str  # YYYY-MM-DD


class QuizResult(BaseModel):
    subject: str
    marks: int  # out of 100


class TimetableSlot(BaseModel):
    subject: str
    start_time: str
    end_time: str
    type: str  # study, revision, hobby_break, recovery


class TimetableRequest(BaseModel):
    user_id: int

    # Available study time
    feasible_time: str  # "09:00-21:00"

    # Weekly study hours
    daily_hours: Dict[str, int]

    # Existing features
    hobbies: Optional[List[str]] = []
    break_hours: int = 1

    study_logs: List[StudyLog]
    exam_dates: List[ExamDate]
    quiz_results: Optional[List[QuizResult]] = []

    # -------------------------
    # NEW PERSONALIZATION
    # -------------------------

    # Study preference
    study_preference: str = "evening"
    # morning / afternoon / evening / night

    # Energy level
    energy_level: str = "medium"
    # low / medium / high

    # Productivity style
    study_style: str = "balanced"
    # pomodoro / deep_work / balanced

    # Sleep schedule
    sleep_time: str = "23:00"
    wake_time: str = "07:00"

    # Topic-level planning
    subject_topics: Dict[str, List[str]] = {}

    # Weak topics from quiz analysis
    wrong_topics: Dict[str, List[str]] = {}
