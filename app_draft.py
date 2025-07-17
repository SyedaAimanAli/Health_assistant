import streamlit as st
import numpy as np
import pandas as pd
from model_draft import match_symptoms, predict_disease, get_precautions, get_severity

# Load real symptoms list
severity_df = pd.read_csv("Symptom-severity.csv")
raw_symptoms = severity_df['Symptom'].dropna().str.strip().str.lower().unique()

# Display-friendly symptom names
symptom_display = [s.replace('_', ' ').title() for s in raw_symptoms]
symptom_map = dict(zip(symptom_display, raw_symptoms))

# Page config
st.set_page_config(page_title="CheckHealth - AI Symptom Checker", page_icon="🩺", layout="centered")

# Header
st.image("https://cdn-icons-png.flaticon.com/512/9381/9381449.png", width=80)
st.title("🩺 CheckHealth: AI Symptom Checker")
st.caption("Get quick insights based on your symptoms and find suggested remedies.")

# Tabs layout
tabs = st.tabs(["🔍 Select Symptoms", "📋 Results"])

with tabs[0]:
    selected_display = st.multiselect(
        "Choose up to 5 symptoms:",
        options=symptom_display,
        max_selections=5,
        placeholder="Start typing e.g. Fever, Chest Pain..."
    )
    st.info("You can select up to 5 symptoms to get a prediction.")

# Process prediction if symptoms selected
if selected_display:
    selected_symptoms = [symptom_map[s] for s in selected_display]  # Convert to raw format
    matched = match_symptoms(','.join(selected_symptoms))

    if not matched:
        predicted_disease = "Unknown"
        remedies = ["❌ Couldn’t match symptoms. Try more common ones."]
        severity_score = 0
    else:
        predicted_disease = predict_disease(matched)
        severity_score = get_severity(matched)
        remedies = get_precautions(predicted_disease)

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

        st.markdown("### 🧩 Matched Symptoms:")
        st.info(", ".join([s.replace('_', ' ').title() for s in matched]))
else:
    with tabs[1]:
        st.warning("Please select symptoms from the first tab to see results.")

# Footer
st.markdown("---")
st.caption("⚠️ This tool is for educational purposes only and not a substitute for professional medical advice.")
