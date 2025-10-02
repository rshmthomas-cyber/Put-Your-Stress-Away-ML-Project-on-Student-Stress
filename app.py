import streamlit as st
import pandas as pd
import joblib
import os
import tempfile



st.set_page_config(page_title="Stress-type Predictor", layout="wide")

# ---------- Feature list (use the exact column names used during training) ----------
FEATURES = [
    "Gender",
    "Age",
    "Have you recently experienced stress in your life?",
    "Have you noticed a rapid heartbeat or palpitations?",
    "Are you finding difficulty to concentrate in studies?",
    "Do you face any sleep problems or difficulties falling asleep?",
    "Have you been dealing with anxiety or tension recently?.1",
    "Have you been getting headaches more often than usual?",
    "Do you get irritated easily?",
    "Do you have trouble concentrating on your academic tasks?",
    "Have you been feeling sadness or low mood?",
    "Have you been experiencing any illness or health issues?",
    "Do you often feel lonely or isolated?",
    "Do you feel overwhelmed with your academic workload?",
    "Are you in competition with your peers, and does it affect you?",
    "Do you find that your relationship often causes you stress?",
    "Are you facing any difficulties with your professors or instructors?",
    "Is your working environment unpleasant or stressful?",
    "Do you struggle to find time for relaxation and leisure activities?",
    "Is your hostel or home environment causing you difficulties?",
    "Do you lack confidence in your academic performance?",
    "Do you lack confidence in your choice of academic subjects?",
    "Academic and extracurricular activities conflicting for you?",
    "Do you attend classes regularly?",
    "Have you gained/lost weight?"
]

CLASS_MAP = {
    0: "Distress (Negative Stress)",
    1: "Eustress (Positive Stress)",
    2: "No Stress"
}

st.title("Know Your Stress")
st.caption("Answer each survey question (except Age and Gender) in a scale of 0–5. Gender as Male/Female. Age is numeric.")

# --- Model loader (local or upload) ---
#uploaded = st.file_uploader("Upload model file (joblib) — optional", type=["joblib", "pkl"])
model = None


if os.path.exists("trained_model.joblib"):
    try:
        model = joblib.load("trained_model.joblib")
        #st.success("Loaded model from model.joblib in app folder.")
    except Exception as e:
        st.error(f"Failed to load model.joblib: {e}")
        st.stop()

else:
    st.warning("No model found. Upload a joblib file or put `model.joblib` in this folder.")
    st.stop()

# Determine expected columns
if hasattr(model, "feature_names_in_"):
    expected_cols = list(model.feature_names_in_)
else:
    expected_cols = FEATURES
    st.info("Model does not expose feature_names_in_. Using the FEATURES list defined in this app — ensure it matches training exactly.")

# --- Input form ---
with st.form("input_form"):
    c1, c2 = st.columns([1,1])
    with c1:
        gender = st.radio("Gender", options=["Male", "Female"], index=0)
    with c2:
        age = st.number_input("Age (years)", min_value=10, max_value=120, value=20, step=1)

    # Map gender (adjust if your training used different encoding)
    gender_map = {"Male": 0, "Female": 1}

    # Survey questions (0-5 scale). We'll create sliders for each.
    question_cols = expected_cols[2:] if len(expected_cols) >= 3 else FEATURES[2:]
    # lay out sliders in two columns for compactness
    cols = st.columns(2)
    slider_values = {}
    for i, q in enumerate(question_cols):
        with cols[i % 2]:
            # integer slider 0-5
            slider_values[q] = st.slider(q, min_value=0, max_value=5, value=0, step=1, key=f"s_{i}")

    submit = st.form_submit_button("Predict")

if submit:
    # build input dict
    input_dict = {}
    input_dict["Gender"] = int(gender_map.get(gender, 0))
    input_dict["Age"] = int(age)

    for q, val in slider_values.items():
        input_dict[q] = int(val)

    # Check missing columns
    missing = [c for c in expected_cols if c not in input_dict]
    if missing:
        st.error("Missing features expected by the model: " + ", ".join(missing))
        st.stop()

    # Create DataFrame in exact order
    input_df = pd.DataFrame([input_dict], columns=expected_cols)
    st.subheader("Inputs (sent to model)")
    st.write(input_df.T)

    # Predict
    try:
        pred = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.info("Check that column names, order, and encodings match what the model was trained on.")
        st.stop()

    human_label = CLASS_MAP.get(int(pred), str(pred))
    st.success(f"Predicted stress type: **{human_label}**")

    # Show probabilities if available
    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(input_df)[0]
            probs_df = pd.DataFrame({
                "class": [int(c) for c in model.classes_],
                "label": [CLASS_MAP.get(int(c), str(c)) for c in model.classes_],
                "probability": probs
            }).sort_values("probability", ascending=False)
            st.subheader("Prediction probabilities")
            st.write(probs_df.reset_index(drop=True))
        except Exception:
            st.info("Model has `predict_proba` but failed to compute probabilities. If you used SVC, it must be trained with probability=True for this to work.")

    # Download
    out = input_df.copy()
    out["prediction_class"] = int(pred)
    out["prediction_label"] = human_label
    csv = out.to_csv(index=False).encode("utf-8")
    st.download_button("Download input + prediction (CSV)", data=csv, file_name="prediction.csv", mime="text/csv")
