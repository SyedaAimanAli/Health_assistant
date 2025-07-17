import streamlit as st
from model_draft import match_symptoms, predict_disease, get_precautions, get_severity

st.set_page_config(page_title="AI Health Assistant", page_icon="🩺")
st.title("🩺 AI Health Assistant")
st.markdown("Enter your symptoms (like *chest pain*, *runny nose*, etc.) separated by commas:")

user_input = st.text_input("Your symptoms", placeholder="e.g. runny nose, chest pain, headache")

if st.button("Check Health"):
    matched = match_symptoms(user_input)
    
    if not matched:
        st.error("❌ Couldn't identify symptoms. Please enter valid or more common symptom names.")
    else:
        disease = predict_disease(matched)
        severity = get_severity(matched)
        remedies = get_precautions(disease)

        st.success(f"🧬 Likely Condition: **{disease}**")
        st.info(f"🔍 Matched Symptoms: `{', '.join(matched)}`")
        st.metric("📊 Severity Score (0–5)", round(severity, 2))

        st.markdown("### 🩹 Suggested Remedies")
        if remedies:
            for r in remedies:
                st.write(f"• {r}")
        else:
            st.write("No specific remedies found.")
