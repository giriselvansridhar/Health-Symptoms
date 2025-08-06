import streamlit as st
import time

# ----------------------------------------
# Disease and symptom database
disease_data = {
    "Flu": ["fever", "cough", "sore throat", "body ache", "fatigue"],
    "COVID-19": ["fever", "dry cough", "loss of smell", "fatigue", "shortness of breath"],
    "Malaria": ["fever", "chills", "sweating", "nausea", "headache"],
    "Diabetes": ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
    "Hypertension": ["headache", "dizziness", "chest pain", "shortness of breath"],
    "Common Cold": ["cough", "sore throat", "runny nose", "sneezing", "mild fever"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "blurred vision"]
}

# Unique symptoms
all_symptoms = sorted(set(symptom for symptoms in disease_data.values() for symptom in symptoms))

# Prediction logic
def predict_disease(selected_symptoms):
    scores = {}
    for disease, symptoms in disease_data.items():
        match_count = len(set(selected_symptoms) & set(symptoms))
        score = match_count / len(symptoms)
        scores[disease] = round(score * 100, 1)
    best_match = max(scores, key=scores.get)
    return best_match, scores

# ----------------------------------------
# Page config
st.set_page_config(page_title="Symptom Checker", page_icon="🩺", layout="wide")

# ----------------------------------------
# Header
st.markdown("<h2 style='text-align: center;'>🩺 Symptom Checker</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter symptoms on the left to view likely conditions on the right.</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------------------
# Columns Layout
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Step 1: Enter Your Symptoms")

    input_mode = st.radio("Input Method:", ["Type Symptoms", "Pick from List"], horizontal=True)

    if input_mode == "Type Symptoms":
        typed_input = st.text_input("Comma-separated symptoms:", placeholder="e.g. fever, nausea, headache")
        selected_symptoms = [s.strip().lower() for s in typed_input.split(",") if s.strip()]
    else:
        selected_symptoms = st.multiselect("Select symptoms (limited view):", options=all_symptoms, max_selections=5)

    submit = st.button("Check Condition")

with right_col:
    st.subheader("Step 2: Predicted Result")

    if submit:
        if not selected_symptoms:
            st.warning("Please enter or select symptoms.")
        else:
            with st.spinner("Analyzing..."):
                time.sleep(1)
                predicted, scores = predict_disease(selected_symptoms)
            
            st.success(f"Most likely: **{predicted}**")

            st.markdown("#### Match Breakdown")
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            for disease, score in sorted_scores:
                st.markdown(f"- **{disease}** → {score}% match")

# ----------------------------------------
# Footer
st.markdown("---")
st.markdown("<small style='color: gray;'>This tool is for educational use only. Consult a doctor for real diagnosis.</small>", unsafe_allow_html=True)
