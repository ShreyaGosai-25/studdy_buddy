from sqlalchemy.orm import Session
from models import StudyLog, QuizResult
from datetime import date


# ------------------ STUDY LOG ------------------
def log_study_time(
    db: Session,
    user_id: int,
    subject: str,
    hours: float
):
    study = StudyLog(
        user_id=user_id,
        subject=subject,
        hours=hours,
        date=date.today()
    )

    db.add(study)
    db.commit()
    db.refresh(study)

    return study


# ------------------ QUIZ RESULT ------------------
def log_quiz_result(
    db: Session,
    user_id: int,
    subject: str,
    score: float
):
    quiz = QuizResult(
        user_id=user_id,
        subject=subject,
        score=score,
        date=date.today()
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz
