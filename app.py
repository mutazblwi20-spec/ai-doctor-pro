import streamlit as st
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="AI Doctor Pro ULTRA",
    page_icon="🩺",
    layout="wide"
)

# =====================================
# DARK MODE
# =====================================
mode = st.sidebar.toggle("🌙 Dark Mode")

if mode:
    bg = "#0e1117"
    text = "white"
else:
    bg = "#f5faff"
    text = "black"

st.markdown(f"""
<style>
body {{
 background:{bg};
 color:{text};
}}
.card {{
 background:white;
 padding:20px;
 border-radius:15px;
 box-shadow:0 5px 20px rgba(0,0,0,0.15);
}}
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================
st.title("🩺 AI Doctor Pro ULTRA")
st.caption("Next-Generation AI Medical Assistant")

# =====================================
# DASHBOARD INPUTS
# =====================================
st.sidebar.header("Patient Data")

age = st.sidebar.slider("Age",1,100,30)
heart = st.sidebar.slider("Heart Rate",40,180,75)
pressure = st.sidebar.slider("Blood Pressure",80,200,120)
chol = st.sidebar.slider("Cholesterol",100,350,180)
glucose = st.sidebar.slider("Glucose",60,250,100)
sleep = st.sidebar.slider("Sleep Hours",1,12,7)
activity = st.sidebar.slider("Activity hrs/week",0,14,3)

smoking = st.sidebar.selectbox("Smoking",["No","Yes"])
diabetes = st.sidebar.selectbox("Diabetes",["No","Yes"])

# =====================================
# AI RISK ENGINE
# =====================================
risk = (
    age*0.3 +
    heart*0.2 +
    pressure*0.25 +
    chol*0.1 +
    glucose*0.15
)

if smoking=="Yes":
    risk+=15
if diabetes=="Yes":
    risk+=20

risk -= sleep*2
risk -= activity*1.5

risk_score = max(0,min(100,risk/5))

# =====================================
# GAUGE CHART
# =====================================
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk_score,
    title={'text':"Health Risk Index"},
    gauge={
        'axis':{'range':[0,100]},
        'steps':[
            {'range':[0,40],'color':'green'},
            {'range':[40,70],'color':'orange'},
            {'range':[70,100],'color':'red'}
        ]
    }
))
st.plotly_chart(gauge,use_container_width=True)

# =====================================
# SMART RECOMMENDATIONS
# =====================================
advice=[]

if risk_score>70:
    status="HIGH RISK ⚠️"
    advice.append("Visit a doctor immediately.")
if pressure>140:
    advice.append("Reduce salt intake.")
if chol>220:
    advice.append("Adopt low-fat diet.")
if sleep<6:
    advice.append("Improve sleep schedule.")
if activity<2:
    advice.append("Increase physical activity.")

if not advice:
    advice.append("Maintain current healthy lifestyle.")

st.subheader("🧠 Smart Medical Recommendations")
for a in advice:
    st.write("✅",a)

# =====================================
# AI DOCTOR CHAT
# =====================================
st.subheader("🤖 AI Doctor Chat (Demo)")

if "chat" not in st.session_state:
    st.session_state.chat=[]

user_msg = st.text_input("Ask AI Doctor...")

if user_msg:
    response = f"""
Based on your risk score ({round(risk_score,1)}),
focus on heart health, balanced diet, and monitoring vitals.
"""
    st.session_state.chat.append(("You",user_msg))
    st.session_state.chat.append(("Doctor AI",response))

for role,msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")

# =====================================
# PDF REPORT
# =====================================
def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,pagesize=A4)
    styles = getSampleStyleSheet()

    story=[]
    story.append(Paragraph("AI Doctor Pro Medical Report",styles['Title']))
    story.append(Spacer(1,12))

    story.append(Paragraph(f"Risk Score: {round(risk_score,1)}",styles['Normal']))
    story.append(Spacer(1,12))

    for a in advice:
        story.append(Paragraph(a,styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

pdf = generate_pdf()

st.download_button(
    "📄 Download Medical Report PDF",
    pdf,
    file_name="AI_Doctor_Report.pdf"
)

# =====================================
# MEDICAL DASHBOARD
# =====================================
st.subheader("🏥 Health Dashboard")

col1,col2,col3 = st.columns(3)

col1.metric("Risk Score",round(risk_score,1))
col2.metric("Heart Rate",heart)
col3.metric("Blood Pressure",pressure)

st.success("System Analysis Complete ✅")
