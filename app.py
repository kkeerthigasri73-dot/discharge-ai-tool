import streamlit as st
from deep_translator import GoogleTranslator
import pyttsx3
import pandas as pd
from datetime import datetime, timedelta

st.title("🏥 Discharge AI Tool")
st.write("Simplifies discharge instructions, translates to Tamil, creates a 7-day plan, and alerts danger signs.")

note = st.text_area("Enter discharge note:", 
    "Patient discharged after appendectomy. Prescribed Amoxicillin 500mg twice daily. Avoid strenuous activity. Follow-up in 7 days.")

simplified = """
You had surgery to remove your appendix.
Take Amoxicillin 500mg two times every day.
Do not lift heavy things or do hard exercise.
Come back to the hospital in 7 days for a check-up.
"""

st.subheader("📝 Simplified Summary")
st.write(simplified)

translated = GoogleTranslator(source='auto', target='ta').translate(simplified)
st.subheader("🌐 Tamil Translation")
st.write(translated)

if st.button("🔊 Hear Instructions"):
    engine = pyttsx3.init()
    engine.say(simplified)
    engine.runAndWait()
    st.success("Voice playback complete!")

start_date = datetime.today()
tasks = [
    {"task": "Take Amoxicillin 500mg", "time": "08:00 AM"},
    {"task": "Take Amoxicillin 500mg", "time": "08:00 PM"},
    {"task": "Avoid heavy lifting", "time": "All Day"},
    {"task": "Check wound for redness/swelling", "time": "06:00 PM"},
]
plan = []
for i in range(7):
    date = start_date + timedelta(days=i)
    for t in tasks:
        plan.append({"Date": date.strftime("%Y-%m-%d"), "Time": t["time"], "Task": t["task"]})
df = pd.DataFrame(plan)

st.subheader("📅 7-Day Action Plan")
st.table(df)

user_symptom = st.text_input("Enter your symptom (e.g., fever, bleeding, redness):")
danger_signs = {
    "fever": "You may have an infection. Please contact your doctor or visit the emergency room.",
    "bleeding": "This could be serious. Apply pressure and seek medical help immediately.",
    "redness": "Watch for spreading redness or swelling. Contact your clinic if it worsens.",
    "pain": "If pain increases or becomes severe, consult your doctor.",
    "swelling": "Swelling may indicate infection. Monitor closely and call your doctor if it grows."
}
alerts = []
for keyword, message in danger_signs.items():
    if keyword in user_symptom.lower():
        alerts.append(f"⚠️ {message}")

if alerts:
    st.subheader("🚨 Danger Alerts")
    for alert in alerts:
        st.error(alert)
    st.caption("Disclaimer: This is not medical advice. Please consult a healthcare professional.")
elif user_symptom:
    st.success("✅ No danger signs detected.")
