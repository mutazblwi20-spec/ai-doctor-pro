import streamlit as st
import plotly.graph_objects as go
from database import save_patient, get_patients
from image_ai import analyze_image

st.set_page_config(page_title="AI Doctor Pro", layout="wide")

st.title("🩺 AI Doctor Pro Platform")

# =====================
# TABS
# =====================
tab1, tab2, tab3 = st.tabs([
    "🧠 Diagnosis",
    "🖼 Medical Image AI",
    "📂 Patient History"
])

# =====================
# TAB 1 — DIAGNOSIS
# =====================
with tab1:

    name = st.text_input("Patient Name")
    age = st.slider("Age",1,100,30)
    heart = st.slider("Heart Rate",40,180,75)
    pressure = st.slider("Blood Pressure",80,200,120)

    risk = (age*0.4 + heart*0.3 + pressure*0.3)/3

    diagnosis = "مصاب" if risk>60 else "غير مصاب"

    if st.button("Run Diagnosis"):

        save_patient(name, age, risk, diagnosis)

        st.success(f"Diagnosis: {diagnosis}")
        st.metric("Risk Score", round(risk,2))

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            gauge={'axis':{'range':[0,100]}}
        ))
        st.plotly_chart(fig)

# =====================
# TAB 2 — IMAGE AI
# =====================
with tab2:

    uploaded = st.file_uploader("Upload Medical Image")

    if uploaded:
        result, color = analyze_image(uploaded)

        if color=="red":
            st.error(result)
        else:
            st.success(result)

        st.image(uploaded)

# =====================
# TAB 3 — HISTORY
# =====================
with tab3:

    data = get_patients()

    st.subheader("Saved Patients")

    if data:
        st.table(data)
    else:
        st.info("No patients saved yet.")
