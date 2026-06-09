# ml/weakness_model.py

import pandas as pd

def classify_weakness(features_df):
    """
    Classify subjects as weak/moderate/strong based on quiz score & weakness_score
    """
    def weakness_label(row):
        if row['weakness_score'] >= 40:
            return 'weak'
        elif row['weakness_score'] >= 20:
            return 'moderate'
        else:
            return 'strong'

    features_df['weakness_level'] = features_df.apply(weakness_label, axis=1)
    return features_df[['user_id', 'subject', 'weakness_level']]
