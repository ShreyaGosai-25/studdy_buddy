from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.tracking_service import log_study_time, log_quiz_result

router = APIRouter(
    prefix="/track",
    tags=["Tracking"]
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ API: LOG STUDY ------------------
@router.post("/study")
def track_study(
    user_id: int,
    subject: str,
    hours: float,
    db: Session = Depends(get_db)
):
    return log_study_time(db, user_id, subject, hours)


# ------------------ API: LOG QUIZ ------------------
@router.post("/quiz")
def track_quiz(
    user_id: int,
    subject: str,
    score: float,
    db: Session = Depends(get_db)
):
    return log_quiz_result(db, user_id, subject, score)
