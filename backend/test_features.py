# from services.features import generate_features

# # Sample Layer 2 outputs
# study_logs = [
#     {"user_id": 1, "subject": "Math", "hours": 2, "date": "2026-01-23"},
#     {"user_id": 1, "subject": "Science", "hours": 1, "date": "2026-01-23"},
#     {"user_id": 2, "subject": "Math", "hours": 1.5, "date": "2026-01-22"}
# ]

# quiz_results = [
#     {"user_id": 1, "subject": "Math", "score": 80, "date": "2026-01-20"},
#     {"user_id": 1, "subject": "Science", "score": 70, "date": "2026-01-22"},
#     {"user_id": 2, "subject": "Math", "score": 60, "date": "2026-01-21"}
# ]

# exam_dates = {
#     "Math": "2026-02-05",
#     "Science": "2026-02-10"
# }

# # Generate features
# features_df = generate_features(study_logs, quiz_results, exam_dates)

# # Print results
# print(features_df)


# from services.features import generate_features
# from ml.time_predictor import train_time_predictor, predict_study_hours

# # Step 1: Sample Layer 2 logs
# study_logs = [
#     {"user_id": 1, "subject": "Math", "hours": 2, "date": "2026-01-23"},
#     {"user_id": 1, "subject": "Science", "hours": 1, "date": "2026-01-23"},
#     {"user_id": 2, "subject": "Math", "hours": 1.5, "date": "2026-01-22"}
# ]

# quiz_results = [
#     {"user_id": 1, "subject": "Math", "score": 80, "date": "2026-01-20"},
#     {"user_id": 1, "subject": "Science", "score": 70, "date": "2026-01-22"},
#     {"user_id": 2, "subject": "Math", "score": 60, "date": "2026-01-21"}
# ]

# exam_dates = {
#     "Math": "2026-02-05",
#     "Science": "2026-02-10"
# }

# # Step 2: Generate Layer 3 features
# features_df = generate_features(study_logs, quiz_results, exam_dates)
# print("Layer 3 Features:")
# print(features_df)

# # Step 3: Train ML model
# train_time_predictor(features_df)

# # Step 4: Predict weekly study hours
# predictions = predict_study_hours(features_df)
# print("\nLayer 4 Predictions:")
# print(predictions)







# from services.features import generate_features
# from ml.weakness_model import classify_weakness

# study_logs = [
#     {"user_id": 1, "subject": "Math", "hours": 2, "date": "2026-01-23"},
#     {"user_id": 1, "subject": "Science", "hours": 1, "date": "2026-01-23"},
#     {"user_id": 2, "subject": "Math", "hours": 1.5, "date": "2026-01-22"}
# ]

# quiz_results = [
#     {"user_id": 1, "subject": "Math", "score": 80, "date": "2026-01-20"},
#     {"user_id": 1, "subject": "Science", "score": 70, "date": "2026-01-22"},
#     {"user_id": 2, "subject": "Math", "score": 60, "date": "2026-01-21"}
# ]

# exam_dates = {"Math": "2026-02-05", "Science": "2026-02-10"}

# # Generate Layer 3 features
# features_df = generate_features(study_logs, quiz_results, exam_dates)

# # Classify weaknesses
# weakness_df = classify_weakness(features_df)
# print(weakness_df)








import pandas as pd
from services.planner import calculate_priority, generate_personalized_timetable

predictions_df = pd.DataFrame({
    "user_id": [1, 1, 1],
    "subject": ["Math", "Science", "English"],
    "predicted_hours": [6, 4, 3],
    "weakness_level": ["weak", "moderate", "strong"]
})

exam_dates = {
    "Math": "2026-02-05",
    "Science": "2026-02-10",
    "English": "2026-02-20"
}

daily_hours = {
    "Monday": 4,
    "Tuesday": 5,
    "Wednesday": 3,
    "Thursday": 5,
    "Friday": 4,
    "Saturday": 6,
    "Sunday": 5
}

priority_df = calculate_priority(predictions_df, exam_dates)

timetable = generate_personalized_timetable(
    priority_df,
    daily_hours,
    most_feasible_time="morning",
    hobby="Music"
)

for day, plan in timetable.items():
    print(day, plan)


