import streamlit as st
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(page_title="CheckHealth - AI Symptom Checker", page_icon="🩺", layout="centered")

# Title & Header
st.image("https://cdn-icons-png.flaticon.com/512/9381/9381449.png", width=80)
st.title("🩺 CheckHealth: AI Symptom Checker")
st.caption("Get quick insights based on your symptoms and find suggested remedies.")

# Sample list of symptoms
symptom_list = [
    "Fever", "Cough", "Fatigue", "Headache", "Nausea", "Vomiting", "Diarrhea",
    "Sore throat", "Shortness of breath", "Chest pain", "Rash", "Joint pain",
    "Loss of appetite", "Chills", "Muscle pain", "Dizziness", "Abdominal pain"
]

# Sample disease prediction logic (for demo purposes)
disease_map = {
    frozenset(["Fever", "Cough", "Fatigue"]): ("Flu", ["Rest and drink fluids", "Take fever reducer"]),
    frozenset(["Headache", "Nausea", "Vomiting"]): ("Migraine", ["Avoid light", "Take prescribed medication"]),
    frozenset(["Chest pain", "Shortness of breath"]): ("Heart Issue", ["Seek immediate medical attention"]),
    frozenset(["Diarrhea", "Abdominal pain"]): ("Food Poisoning", ["Stay hydrated", "Eat light food"]),
}

severity_weights = {
    "Fever": 2, "Cough": 2, "Fatigue": 1, "Headache": 1, "Nausea": 1, "Vomiting": 2,
    "Diarrhea": 2, "Sore throat": 1, "Shortness of breath": 4, "Chest pain": 5,
    "Rash": 1, "Joint pain": 1, "Loss of appetite": 1, "Chills": 2,
    "Muscle pain": 2, "Dizziness": 3, "Abdominal pain": 2
}

# Tabs for layout
tabs = st.tabs(["🔍 Select Symptoms", "📋 Results"])

with tabs[0]:
    selected = st.multiselect("Choose up to 5 symptoms:", symptom_list, max_selections=5)
    st.info("You can select up to 5 symptoms to get a prediction.")

if selected:
    selected_set = frozenset(selected)

    # Default prediction
    predicted_disease = "Unknown"
    remedies = ["No remedy found. Please consult a doctor."]

    # Match a known disease
    for sym_set, (disease, rem) in disease_map.items():
        if sym_set.issubset(selected_set):
            predicted_disease = disease
            remedies = rem
            break

    # Calculate average severity
    severity_score = np.mean([severity_weights.get(sym, 1) for sym in selected])
    severity_percent = int((severity_score / 5) * 100)

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🧠 **Predicted Condition:** {predicted_disease}")
            st.write(f"🔥 **Severity Level:** {round(severity_score, 2)} / 5")
            st.progress(severity_percent)
        with col2:
            st.markdown("### 🩹 Suggested Remedies:")
            for r in remedies:
                st.markdown(f"- {r}")

        st.markdown("### 🧩 Your Symptoms:")
        st.info(", ".join(selected))
else:
    with tabs[1]:
        st.warning("Please select symptoms from the first tab to see results.")

# Footer
st.markdown("---")
st.caption("⚠️ This tool is for educational purposes only and not a substitute for professional medical advice.")
