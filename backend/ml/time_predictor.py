# # ml/time_predictor.py

# import pandas as pd
# from sklearn.linear_model import LinearRegression
# import joblib  # are only to save/load trained model

# # -----------------------------
# # Function 1: Train the predictor
# # -----------------------------
# def train_time_predictor(features_df, model_path="ml/time_predictor_model.pkl"):
#     """
#     Train a regression model to predict weekly study hours.
#     """
#     # Features used for prediction
#     X = features_df[['avg_study_hours', 'avg_quiz_score', 'days_to_exam', 'weakness_score']]
    
#     # Target: Weekly study hours
#     # For demo purposes, let's create a synthetic target if not already available
#     features_df['weekly_hours_needed'] = (
#         X['weakness_score'] * 0.1 + X['days_to_exam'] * 0.05 + X['avg_study_hours'] * 0.5
#     )
#     y = features_df['weekly_hours_needed']

#     # Train a simple Linear Regression model
#     model = LinearRegression()
#     model.fit(X, y)

#     # Save the trained model for later use
#     joblib.dump(model, model_path)
#     print(f"Model trained and saved at {model_path}")
#     return model

# # -----------------------------
# # Function 2: Predict study hours
# # -----------------------------
# def predict_study_hours(features_df, model_path="ml/time_predictor_model.pkl"):
#     """
#     Predict weekly study hours for each user and subject.
#     """
#     X = features_df[['avg_study_hours', 'avg_quiz_score', 'days_to_exam', 'weakness_score']]
    
#     # Load the trained model
#     model = joblib.load(model_path)
    
#     # Predict and add new column
#     features_df['predicted_hours'] = model.predict(X)
    
#     # Return only relevant columns
#     return features_df[['user_id', 'subject', 'predicted_hours']]


# backend/ml/time_predictor.py

def predict_study_time(features_df):
    """
    Predict weekly study hours for each subject.
    Rule-based now (acts like ML logic).
    """

    predicted_hours = []

    for _, row in features_df.iterrows():

        # Base weekly hours
        base_hours = 5

        # Lower quiz score → more hours needed
        score_factor = (100 - row["avg_quiz_score"]) / 20

        # Exam closer → more urgency
        urgency_factor = max(0, 10 - row["days_to_exam"]) / 5

        total_hours = base_hours + score_factor + urgency_factor
        predicted_hours.append(round(total_hours, 2))

    return predicted_hours

