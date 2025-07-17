import pandas as pd
import re

# Load data
dataset = pd.read_csv("dataset.csv")
precautions = pd.read_csv("symptom_precaution.csv")
severities = pd.read_csv("Symptom-severity.csv")
descriptions = pd.read_csv("symptom_Description.csv")

# Normalize all symptoms
def normalize(symptom):
    symptom = symptom.lower().strip()
    symptom = re.sub(r'[\s\-]+', '_', symptom)  # Convert space or dash to underscore
    return symptom

known_symptoms = severities['Symptom'].apply(normalize).unique()

# Match user input symptoms to known symptoms
def match_symptoms(user_input):
    raw = [s.strip() for s in user_input.split(',')]
    cleaned = [normalize(s) for s in raw]
    matched = [sym for sym in cleaned if sym in known_symptoms]
    return matched

def predict_disease(user_symptoms):
    all_symptoms = dataset.columns[:-1]
    best_match = None
    max_match_count = 0

    for _, row in dataset.iterrows():
        row_symptoms = set([normalize(s) for s in row[all_symptoms] if pd.notna(s)])
        match_count = len(set(user_symptoms) & row_symptoms)
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = row['Disease']

    return best_match

def get_precautions(disease):
    row = precautions[precautions['Disease'].str.lower() == disease.lower()]
    if not row.empty:
        return row.iloc[0][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].dropna().tolist()
    return []

def get_severity(symptoms):
    severity_scores = severities.copy()
    severity_scores['Symptom'] = severity_scores['Symptom'].apply(normalize)
    severity_dict = severity_scores.set_index('Symptom')['weight'].to_dict()
    total = sum([severity_dict.get(s, 0) for s in symptoms])
    return total / max(len(symptoms), 1)
