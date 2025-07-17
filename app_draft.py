import streamlit as st
from model_draft import match_symptoms, predict_disease, get_precautions, get_severity
import pandas as pd

# Load symptom data
severity_df = pd.read_csv("Symptom-severity.csv")
raw_symptoms = severity_df['Symptom'].dropna().str.strip().str.lower().unique()

# Format for dropdown
symptom_display = [sym.replace('_', ' ').title() for sym in raw_symptoms]
symptom_map = dict(zip(symptom_display, raw_symptoms))

# App UI
st.set_page_config(page_title="Health Assistant", page_icon="🩺")
st.title("🩺 AI Health Assistant")
st.markdown("Describe your symptoms below. We’ll predict the most likely disease and provide remedies.")

# Dropdown
selected_display = st.multiselect(
    "Choose your symptoms:",
    options=symptom_display,
    placeholder="Start typing like 'Fever', 'Headache'...",
)

# ONE button only, one key
if st.button("Check Health", key="health_button"):
    if not selected_display:
        st.warning("Please select at least one symptom.")
    else:
        selected_symptoms = [symptom_map[s] for s in selected_display]
        matched = match_symptoms(','.join(selected_symptoms))

        if not matched:
            st.error("No match found. Please select more common symptoms.")
        else:
            disease = predict_disease(matched)
            severity = get_severity(matched)
            remedies = get_precautions(disease)

            st.success(f"🔍 **Likely Disease:** {disease}")
            st.info(f"🧪 **Matched Symptoms:** {', '.join([s.replace('_', ' ').title() for s in matched])}")
            st.write(f"📊 **Severity Level (0–5):** {round(severity, 2)}")

            st.markdown("### 🩹 Suggested Remedies:")
            for item in remedies:
                st.write(f"• {item}")

# Optional styling
st.markdown(
    """
    <style>
    .css-1v0mbdj p {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
