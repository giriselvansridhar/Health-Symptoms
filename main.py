import streamlit as st
import pandas as pd
import time
import urllib.parse


disease_data = {
    "Flu": ["fever", "cough", "sore throat", "body ache", "fatigue"],
    "COVID-19": ["fever", "dry cough", "loss of smell", "fatigue", "shortness of breath"],
    "Malaria": ["fever", "chills", "sweating", "nausea", "headache"],
    "Diabetes": ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
    "Hypertension": ["headache", "dizziness", "chest pain", "shortness of breath"],
    "Common Cold": ["cough", "sore throat", "runny nose", "sneezing", "mild fever"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "blurred vision"]
}


doctor_map = {
    "Flu": "General Practitioner",
    "COVID-19": "General Practitioner or Infectious Disease Specialist",
    "Malaria": "Infectious Disease Specialist",
    "Diabetes": "Endocrinologist",
    "Hypertension": "Cardiologist",
    "Common Cold": "General Practitioner",
    "Migraine": "Neurologist"
}


minor_diseases = {"Flu", "Common Cold", "Migraine"}


def predict_disease(selected_symptoms):
    scores = {}
    for disease, symptoms in disease_data.items():
        match_count = len(set(selected_symptoms) & set(symptoms))
        score = match_count / len(symptoms)
        scores[disease] = round(score * 100, 1)
    best_match = max(scores, key=scores.get)
    return best_match, scores

st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺", layout="wide")

st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 0px;
        color: #1a6ed8;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #cccccc;
        margin-bottom: 2rem;
    }
    .section-title {
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #aaaaaa;
    }
    .result-box {
        background-color: #123524;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .link {
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='main-title'>🩺 AI Symptom Checker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter your symptoms and get a prediction with doctor suggestions</div>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-title'>Step 1: Input Symptoms</div>", unsafe_allow_html=True)
    symptom_input = st.text_input("Describe your symptoms (comma-separated):", placeholder="e.g. fever, headache, nausea")
    submitted = st.button("🔍 Predict Disease")

with col2:
    st.markdown("<div class='section-title'>Step 2: Result & Suggestions</div>", unsafe_allow_html=True)

    if submitted:
        selected = [s.strip().lower() for s in symptom_input.split(",") if s.strip()]
        if not selected:
            st.warning("Please enter some symptoms first.")
        else:
            with st.spinner("Analyzing your symptoms..."):
                time.sleep(1.5)
                prediction, scores = predict_disease(selected)

            st.markdown(f"<div class='result-box'>Most likely condition: {prediction}</div>", unsafe_allow_html=True)

            recommended_doctor = doctor_map.get(prediction, "General Practitioner")
            st.markdown(f"**Suggested Specialist:** _{recommended_doctor}_")

            search_term = urllib.parse.quote_plus(recommended_doctor)
            st.markdown(f'🔗 [Find on Zocdoc](https://www.zocdoc.com/search?searchSource=Homepage&query={search_term})')
            st.markdown(f'🗺️ [Google Maps Nearby](https://www.google.com/maps/search/{search_term}+near+me)')

            if prediction in minor_diseases:
                st.info("💡 This may be a minor condition. Consider using a **telemedicine** service.")

            # Match Scores
            st.markdown("### 📊 Match Scores:")
            df = pd.DataFrame(scores.items(), columns=["Disease", "Match (%)"])
            st.dataframe(df.sort_values("Match (%)", ascending=False), use_container_width=True)
    else:
        st.markdown("<i>Results will appear here once you submit your symptoms.</i>", unsafe_allow_html=True)

# -----------------------
# Disclaimer
st.markdown("""
---
> ⚠️ **Disclaimer**: This tool is for educational use only and does not replace professional medical advice. Always consult a licensed healthcare provider.
""")
