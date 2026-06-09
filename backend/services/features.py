# services/features.py

from datetime import datetime, timedelta
import pandas as pd

# Sample function to create features from study logs and quiz results
def generate_features(study_logs, quiz_results, exam_dates):
    """
    Convert raw logs into ML-ready features.

    Args:
        study_logs (list of dict): [{"user_id":1, "subject":"Math", "hours":2, "date":"2026-01-23"}, ...]
        quiz_results (list of dict): [{"user_id":1, "subject":"Math", "score":80, "date":"2026-01-20"}, ...]
        exam_dates (dict): {"Math": "2026-02-05", "Science": "2026-02-10"}

    Returns:
        pd.DataFrame: ML-ready features per user and subject
    """

    # Convert to DataFrames
    df_study = pd.DataFrame(study_logs)
    df_quiz = pd.DataFrame(quiz_results)

    # Convert date strings to datetime
    df_study['date'] = pd.to_datetime(df_study['date'])
    df_quiz['date'] = pd.to_datetime(df_quiz['date'])

    features = []

    users = df_study['user_id'].unique()
    subjects = df_study['subject'].unique()

    for user in users:
        for subject in subjects:
            # Filter logs
            user_study = df_study[(df_study['user_id'] == user) & (df_study['subject'] == subject)]
            user_quiz = df_quiz[(df_quiz['user_id'] == user) & (df_quiz['subject'] == subject)]

            if user_study.empty and user_quiz.empty:
                continue

            # Feature 1: Average study hours
            avg_study_hours = user_study['hours'].mean() if not user_study.empty else 0

            # Feature 2: Average quiz score
            avg_quiz_score = user_quiz['score'].mean() if not user_quiz.empty else 0

            # Feature 3: Days to exam
            exam_date = pd.to_datetime(exam_dates.get(subject))
            last_study_date = user_study['date'].max() if not user_study.empty else datetime.today()
            days_to_exam = max((exam_date - last_study_date).days, 0)

            # Feature 4: Weakness score (simple example: higher if quiz low)
            weakness_score = max(100 - avg_quiz_score, 0)

            # Append features
            features.append({
                "user_id": user,
                "subject": subject,
                "avg_study_hours": avg_study_hours,
                "avg_quiz_score": avg_quiz_score,
                "days_to_exam": days_to_exam,
                "weakness_score": weakness_score
            })

    return pd.DataFrame(features)
