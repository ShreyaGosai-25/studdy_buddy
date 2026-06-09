from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    name = Column(String)
    difficulty = Column(Integer)  # 1=easy, 2=medium, 3=hard
    exam_date = Column(Date)

class StudyLog(Base):
    __tablename__ = "study_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    subject = Column(String)
    hours = Column(Float)
    date = Column(Date)
class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    subject = Column(String)
    score = Column(Float)  # 0–100
    date = Column(Date)
class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    day = Column(String)       # Monday, Tuesday...
    subject = Column(String)
    duration = Column(Float)  # hours
    type = Column(String)     # study / revision
