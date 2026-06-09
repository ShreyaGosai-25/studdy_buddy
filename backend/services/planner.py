






# # services/planner.py

# from typing import Dict
# import pandas as pd

# # ------------------------------
# # Generate priority per subject
# # ------------------------------
# def generate_priority(features_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Calculate priority score for each subject.
#     Higher weakness_score and closer exams => higher priority.
#     """
#     df = features_df.copy()
#     # Priority formula: weakness_score + (100 - avg_quiz_score) + urgency (days_to_exam inverse)
#     df['priority'] = df['weakness_score'] + (100 - df['avg_quiz_score']) + (1 / (df['days_to_exam'] + 1) * 100)
#     return df.sort_values(by='priority', ascending=False)

# # ------------------------------
# # Generate weekly timetable
# # ------------------------------
# def generate_weekly_timetable(
#     features_df: pd.DataFrame,
#     daily_hours: Dict[str, float],
#     break_hours: float,
#     feasible_time: str,
#     hobby: str
# ) -> Dict[str, Dict]:
#     """
#     Distribute subjects across the week based on priority.
#     Every day has all subjects. Weak subjects get more time.
#     """
#     # Get priority
#     df_priority = generate_priority(features_df)

#     subjects = df_priority['subject'].tolist()
#     priorities = df_priority['priority'].tolist()
#     total_priority = sum(priorities)

#     # Timetable dictionary
#     timetable = {}

#     for day, hours in daily_hours.items():
#         available_hours = max(hours - break_hours, 0)
#         day_schedule = []

#         for subject, priority in zip(subjects, priorities):
#             # Allocate time proportional to priority
#             allocated_time = round((priority / total_priority) * available_hours, 1)
#             day_schedule.append(f"{subject} - {allocated_time}h")

#         # Add break slot
#         day_schedule.append(f"Break ({hobby}) - {break_hours}h")

#         timetable[day] = {
#             "preferred_time": feasible_time,
#             "schedule": day_schedule
#         }

#     return timetable




























# from datetime import datetime, timedelta
# from models.timetable_models import TimetableRequest, TimetableSlot
# import random

# def generate_weekly_timetable(request: TimetableRequest) -> dict:
#     week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#     timetable = {}

#     for day in week_days:
#         daily_hours = request.daily_hours.get(day, 0)
#         if daily_hours == 0:
#             timetable[day] = []
#             continue

#         slots = []
#         current_time = datetime.strptime("09:00", "%H:%M")  # start time
#         end_time = current_time + timedelta(hours=daily_hours)
#         study_logs = request.study_logs.copy()
#         hobbies = request.hobbies.copy()

#         while current_time < end_time and study_logs:
#             # Pick a subject
#             log = study_logs.pop(0)
#             subject_hours = min(log.hours, (end_time - current_time).seconds / 3600)
#             slot_end = current_time + timedelta(hours=subject_hours)
#             slots.append(TimetableSlot(
#                 subject=log.subject,
#                 start_time=current_time.strftime("%H:%M"),
#                 end_time=slot_end.strftime("%H:%M"),
#                 type="study"
#             ))
#             current_time = slot_end

#             # Add a break if time remains
#             if current_time < end_time and request.break_hours > 0:
#                 break_duration = min(0.5, (end_time - current_time).seconds / 3600)
#                 slot_end = current_time + timedelta(hours=break_duration)
#                 hobby = random.choice(hobbies)
#                 slots.append(TimetableSlot(
#                     subject="Break",
#                     start_time=current_time.strftime("%H:%M"),
#                     end_time=slot_end.strftime("%H:%M"),
#                     type="break",
#                     hobby=hobby
#                 ))
#                 current_time = slot_end

#         # Add revision slots for exams within 7 days
#         for quiz in request.quiz_results:
#             if quiz.days_to_exam <= 7:
#                 slot_start = current_time
#                 slot_end = slot_start + timedelta(hours=1)
#                 if slot_end <= end_time:
#                     slots.append(TimetableSlot(
#                         subject=f"Revision: {quiz.subject}",
#                         start_time=slot_start.strftime("%H:%M"),
#                         end_time=slot_end.strftime("%H:%M"),
#                         type="revision"
#                     ))
#                     current_time = slot_end

#         timetable[day] = [slot.dict() for slot in slots]

#     return timetable










# final

# from datetime import datetime, timedelta
# from models.timetable_models import TimetableRequest, TimetableSlot

# def generate_weekly_timetable(request: TimetableRequest) -> dict:
#     """
#     Generates a weekly timetable with:
#     - Study slots (max available hours)
#     - Break slots labeled as hobbies (rotating)
#     - Revision slots for exams within 7 days
#     """

#     week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#     timetable = {}

#     # Hobby rotation index (global so it changes across days)
#     hobby_index = 0
#     hobbies = request.hobbies or []

#     for day in week_days:
#         daily_hours = request.daily_hours.get(day, 0)

#         if daily_hours <= 0:
#             timetable[day] = []
#             continue

#         slots = []
#         current_time = datetime.strptime("09:00", "%H:%M")
#         day_end_time = current_time + timedelta(hours=daily_hours)

#         # Copy study logs so original request is untouched
#         study_logs = request.study_logs.copy()

#         while current_time < day_end_time and study_logs:
#             log = study_logs.pop(0)

#             remaining_hours = (day_end_time - current_time).seconds / 3600
#             study_hours = min(log.hours, remaining_hours, 2)  # max 2 hrs/session

#             if study_hours <= 0:
#                 break

#             study_end = current_time + timedelta(hours=study_hours)

#             # Study slot
#             slots.append(TimetableSlot(
#                 subject=log.subject,
#                 start_time=current_time.strftime("%H:%M"),
#                 end_time=study_end.strftime("%H:%M"),
#                 type="study"
#             ))

#             current_time = study_end

#             # Add hobby break if time remains
#             if (
#                 current_time < day_end_time
#                 and request.break_hours > 0
#                 and hobbies
#             ):
#                 remaining_hours = (day_end_time - current_time).seconds / 3600
#                 break_duration = min(0.5, remaining_hours)

#                 break_end = current_time + timedelta(hours=break_duration)

#                 # Rotate hobby
#                 hobby = hobbies[hobby_index % len(hobbies)]
#                 hobby_index += 1

#                 slots.append(TimetableSlot(
#                     subject=hobby,                  # 🔥 hobby name shown
#                     start_time=current_time.strftime("%H:%M"),
#                     end_time=break_end.strftime("%H:%M"),
#                     type="break"
#                 ))

#                 current_time = break_end

#         # Add revision slots (exam within 7 days)
#         for quiz in request.quiz_results:
#             if quiz.days_to_exam <= 3:
#                 if current_time + timedelta(hours=1) <= day_end_time:
#                     revision_end = current_time + timedelta(hours=1)

#                     slots.append(TimetableSlot(
#                         subject=f"Revision: {quiz.subject}",
#                         start_time=current_time.strftime("%H:%M"),
#                         end_time=revision_end.strftime("%H:%M"),
#                         type="revision"
#                     ))

#                     current_time = revision_end

#         # Convert Pydantic models to dict
#         timetable[day] = [slot.dict() for slot in slots]

#     return timetable




# final2
from datetime import datetime, timedelta
from backend.models.timetable_models import TimetableRequest, TimetableSlot


def generate_weekly_timetable(request: TimetableRequest):

    week_days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    timetable = {d: [] for d in week_days}

    hobbies = request.hobbies or ["Music", "Walk", "Meditation"]
    hobby_index = 0

    today = datetime.today()

    # ---------------- STYLE ---------------- #
    if request.study_style == "pomodoro":
        study_block = 25 / 60
        break_block = 5 / 60

    elif request.study_style == "deep_work":
        study_block = 1.5
        break_block = 0.25
    else:
        study_block = 1
        break_block = 0.15

    # ---------------- ENERGY ---------------- #
    if request.energy_level == "high":
        study_block *= 1.25
    elif request.energy_level == "low":
        study_block *= 0.7

    # ---------------- PRIORITY ---------------- #
    revision_priority = []

    for exam in request.exam_dates:

        exam_date = datetime.strptime(exam.date, "%Y-%m-%d")
        days_left = (exam_date - today).days

        marks = 50
        for q in request.quiz_results or []:
            if q.subject == exam.subject:
                marks = q.marks

        score = days_left - ((100 - marks) / 10)

        revision_priority.append({
            "subject": exam.subject,
            "days_left": days_left,
            "marks": marks,
            "score": score
        })

    revision_priority.sort(key=lambda x: x["score"])

    # ---------------- WEEK LOAD ---------------- #
    weekly_hours = sum(request.daily_hours.values())
    burnout = weekly_hours > 40

    # ---------------- SUBJECTS SAFE ---------------- #
    subject_topics = getattr(request, "subject_topics", {}) or {}
    wrong_topics = getattr(request, "wrong_topics", {}) or {}

    # ---------------- GENERATE ---------------- #
    for day in week_days:

        daily_hours = request.daily_hours.get(day, 0)
        if daily_hours <= 0:
            timetable[day] = []
            continue

        start_str, _ = request.feasible_time.split("-")
        current_time = datetime.strptime(start_str, "%H:%M")
        end_time = current_time + timedelta(hours=daily_hours)

        slots = []

        break_counter = 0

        # ---------------- TOPICS ---------------- #
        for subject, topics in subject_topics.items():

            for topic in topics:

                if current_time >= end_time:
                    break

                slots.append(TimetableSlot(
                    subject=f"{subject} - {topic}",
                    start_time=current_time.strftime("%H:%M"),
                    end_time=(current_time + timedelta(hours=study_block)).strftime("%H:%M"),
                    type="study"
                ))

                current_time += timedelta(hours=study_block)

                # smart breaks (not after every topic)
                break_counter += 1

                if break_counter % 2 == 0 and current_time < end_time:

                    hobby = hobbies[hobby_index % len(hobbies)]
                    hobby_index += 1

                    slots.append(TimetableSlot(
                        subject=f"🧘 {hobby}",
                        start_time=current_time.strftime("%H:%M"),
                        end_time=(current_time + timedelta(hours=break_block)).strftime("%H:%M"),
                        type="break"
                    ))

                    current_time += timedelta(hours=break_block)

        # ---------------- WEAK TOPICS ---------------- #
        for subject, topics in wrong_topics.items():

            for topic in topics:

                if current_time >= end_time:
                    break

                slots.append(TimetableSlot(
                    subject=f"⚠ Revision {subject} - {topic}",
                    start_time=current_time.strftime("%H:%M"),
                    end_time=(current_time + timedelta(hours=1)).strftime("%H:%M"),
                    type="revision"
                ))

                current_time += timedelta(hours=1)

        # ---------------- EXAMS ---------------- #
        for rev in revision_priority:

            if current_time >= end_time:
                break

            slots.append(TimetableSlot(
                subject=f"🎯 Exam Revision {rev['subject']}",
                start_time=current_time.strftime("%H:%M"),
                end_time=(current_time + timedelta(hours=1)).strftime("%H:%M"),
                type="revision"
            ))

            current_time += timedelta(hours=1)

        # ---------------- BURNOUT ---------------- #
        if burnout:

            slots.append(TimetableSlot(
                subject="🧘 Recovery Break",
                start_time=current_time.strftime("%H:%M"),
                end_time=(current_time + timedelta(minutes=30)).strftime("%H:%M"),
                type="recovery"
            ))

        timetable[day] = [s.dict() for s in slots]

    # ---------------- MOTIVATION ---------------- #
    motivation = "Stay consistent. You are improving daily."

    if revision_priority:
        weak = min(revision_priority, key=lambda x: x["marks"])
        motivation = (
            f"You are weakest in {weak['subject']} "
            f"({weak['marks']}%). Focus here first."
        )

    return {
        "timetable": timetable,
        "motivation": motivation,
        "weekly_hours": weekly_hours,
        "burnout_risk": burnout
    }