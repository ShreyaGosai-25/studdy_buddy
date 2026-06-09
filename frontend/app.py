










import streamlit as st
import random
import requests
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



API_URL = "http://127.0.0.1:8000"
# ---------- SESSION STATE FIX ----------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "timetable" not in st.session_state:
    st.session_state.timetable = None

# Initialize session state
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "theme" not in st.session_state:
    st.session_state.theme = "bright"

# Page config
st.set_page_config(page_title="StudySync", layout="wide", initial_sidebar_state="expanded")

# Theme definitions
THEMES = {
    "bright": {
    "primary": "#CE8490",
    "secondary": "#4B1A4B",
    "accent": "#FE978E",

    "bg": "#898AA6",          # page background
    "card_bg": "#515A66",     # cards

    "text": "#FFFFFF",        # dark blue
    "text_secondary": "#263166",

    "border": "#DC7A91",

    "success": "#A95862",

    "chart_color": "#FFFFFF"
}, 
    "dark": {
        "primary": "#506789",  # Steel blue
        "secondary": "#bebcd3",  # Light lavender
        "accent": "#abb1cf",  # Periwinkle accent
        "bg": "#091423",  # Deep navy background
        "card_bg": "#1e2c53",  # Dark blue cards
        "text": "#bebcd3",  # Light lavender text
        "text_secondary": "#abb1cf",  # Periwinkle secondary
        "border": "#263166",  # Dark purple border
        "success": "#506789",
        "chart_color": "#bebcd3"
    }
}

current_theme = THEMES[st.session_state.theme]

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    .stApp {{
        background: {current_theme['bg']};
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 80px;
        z-index: 999;
        background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']});
        border: none;
        border-radius: 50px;
        padding: 12px 24px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    /* Header styling */
    h1, h2, h3 {{
        color: {current_theme['text']} !important;
        font-weight: 700 !important;
    }}
    
    /* Card styling */
    .custom-card {{
        background: {current_theme['card_bg']};
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid {current_theme['border']};
        transition: all 0.3s ease;
    }}
    
    .custom-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }}
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        background: {current_theme['card_bg']} !important;
        color: {current_theme['text']} !important;
        border: 2px solid {current_theme['border']} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: {current_theme['primary']} !important;
        box-shadow: 0 0 0 3px {current_theme['primary']}33 !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px {current_theme['primary']}40;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px {current_theme['primary']}60;
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        background: {current_theme['card_bg']};
        padding: 15px;
        border-radius: 12px;
        border: 2px solid {current_theme['border']};
    }}
    
    /* Checkbox styling */
    .stCheckbox > label {{
        background: {current_theme['card_bg']};
        padding: 10px 15px;
        border-radius: 8px;
        border: 2px solid {current_theme['border']};
        transition: all 0.3s ease;
    }}
    
    .stCheckbox > label:hover {{
        border-color: {current_theme['primary']};
        background: {current_theme['primary']}15;
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        background: {current_theme['card_bg']} !important;
        border: 2px solid {current_theme['border']} !important;
        border-radius: 12px !important;
    }}
    
    /* Metrics */
    .metric-card {{
        background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']});
        border-radius: 16px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {{
        background: {"#1E293B" if st.session_state.theme == "bright" else current_theme['card_bg']};
        border-right: 2px solid {current_theme['border']};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: {current_theme['card_bg']} !important;
        border: 2px solid {current_theme['border']} !important;
        border-radius: 12px !important;
        color: {current_theme['text']} !important;
    }}
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {{
        background: {current_theme['primary']}20 !important;
        border-left: 4px solid {current_theme['primary']} !important;
        border-radius: 8px !important;
        color: {current_theme['text']} !important;
    }}
    
    /* Divider */
    hr {{
        border-color: {current_theme['border']} !important;
        margin: 30px 0 !important;
    }}
    
    /* Form styling */
    .stForm {{
        background: {current_theme['card_bg']};
        border: 2px solid {current_theme['border']};
        border-radius: 16px;
        padding: 20px;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {current_theme['card_bg']};
        border-radius: 12px;
        padding: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {current_theme['text']};
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']});
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# Theme toggle button
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🌓 Toggle Theme", key="theme_toggle"):
        st.session_state.theme = "dark" if st.session_state.theme == "bright" else "bright"
        st.rerun()

# Header
st.markdown(f"""
<div style='background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']}); 
            padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
    <h1 style='color: white !important; margin: 0; font-size: 3em;'>🎓 StudySync</h1>
    <p style='color: rgba(255,255,255,0.9); font-size: 1.2em; margin-top: 10px;'>
        Your AI-Powered Study Companion
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {current_theme['primary']}, {current_theme['secondary']});
                border-radius: 16px; margin-bottom: 20px;'>
        <h2 style='color: white !important; margin: 0;'>📚 Menu</h2>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigate to:",
        ["📅 Generate Timetable", "📝 Track Tasks", "🧠 Study & Quiz", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style='background: {current_theme['card_bg']}; padding: 15px; border-radius: 12px; 
                border: 2px solid {current_theme['border']}; margin-top: 20px;'>
        <h4 style='color: {current_theme['text']}; margin-top: 0;'>⚙️ Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
  


# ---------------- GENERATE TIMETABLE ---------------- #

if menu == "📅 Generate Timetable":

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("📅 Generate Weekly Timetable")

    col1, col2 = st.columns(2)

    with col1:
        user_id_local = st.number_input("👤 User ID", min_value=1, value=1)
        feasible_time = st.text_input("⏰ Study Time", "09:00-21:00")

    with col2:
        hobbies = st.multiselect(
            "🎨 Hobbies",
            ["Music", "Reading", "Exercise", "Gaming", "Meditation"],
            default=["Music", "Reading"]
        )

        break_hours = st.number_input("☕ Break Hours", 0, 4, 1)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DAILY HOURS ---------------- #
    st.subheader("📊 Daily Hours")
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    cols = st.columns(7)

    daily_hours = {}
    for i, d in enumerate(days):
        with cols[i]:
            daily_hours[d] = st.number_input(d, 0, 12, 5, key=f"day_{d}")

    # ---------------- SUBJECTS ---------------- #
    st.subheader("📚 Subjects")

    subjects = st.text_input("Subjects", "Maths, Physics, Chemistry").split(",")
    subjects = [s.strip() for s in subjects if s.strip()]

    study_logs, exam_dates, quiz_results = [], [], []

    for s in subjects:

        c1, c2, c3 = st.columns(3)

        with c1:
            hrs = st.number_input(f"{s} hours", 1, 12, 2)

        with c2:
            exam = st.date_input(f"{s} exam", value=date.today())

        with c3:
            marks = st.number_input(f"{s} marks", 0, 100, 70)

        study_logs.append({
            "user_id": user_id_local,
            "subject": s,
            "hours": hrs,
            "date": str(date.today())
        })

        exam_dates.append({
            "subject": s,
            "date": str(exam)
        })

        quiz_results.append({
            "subject": s,
            "marks": marks
        })

    # ---------------- SUBMIT ---------------- #
    if st.button("✨ Generate Timetable"):

        payload = {
            "user_id": user_id_local,
            "feasible_time": feasible_time,
            "hobbies": hobbies,
            "break_hours": break_hours,
            "daily_hours": daily_hours,
            "study_logs": study_logs,
            "exam_dates": exam_dates,
            "quiz_results": quiz_results
        }

        res = requests.post(f"{API_URL}/timetable/generate", json=payload)

        if res.status_code == 200:

            timetable = res.json()
            st.session_state["timetable"] = timetable

            st.success("✅ Generated!")

            for day, slots in timetable.items():

                st.markdown(f"## 📅 {day}")

                for slot in slots:
                    st.markdown(f"""
                    **{slot['subject']}**  
                    ⏰ {slot['start_time']} - {slot['end_time']}  
                    🏷 {slot['type']}
                    """)

# ---------------- TRACK TASKS ---------------- #
elif menu == "📝 Track Tasks":

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.header("📝 Weekly Progress Tracker")

    timetable = st.session_state.get("timetable", {})

    if not timetable:
        st.warning("⚠️ Please generate a timetable first!")

    else:

        total_tasks = 0
        completed_tasks = 0

        subject_total = {}
        subject_completed = {}

        consistency_days = 0

        st.subheader("📅 Mark Completed Tasks")

        for day, slots in timetable.items():

            st.markdown(f"### 📆 {day}")

            day_completed = 0
            day_total = 0

            for idx, slot in enumerate(slots):

                if slot["type"] not in ["study", "revision"]:
                    continue

                day_total += 1
                total_tasks += 1

                subject = slot["subject"]

                if "Revision:" in subject:
                    subject = subject.replace("Revision: ", "")

                subject_total[subject] = (
                    subject_total.get(subject, 0) + 1
                )

                key = f"{day}_{idx}"

                done = st.checkbox(
                    f"{slot['subject']} ({slot['start_time']} - {slot['end_time']})",
                    key=key
                )

                if done:

                    completed_tasks += 1
                    day_completed += 1

                    subject_completed[subject] = (
                        subject_completed.get(subject, 0) + 1
                    )

            if day_total > 0 and day_completed > 0:
                consistency_days += 1

        st.markdown("---")

        progress_percent = (
            completed_tasks / total_tasks * 100
            if total_tasks > 0 else 0
        )

        consistency_percent = (
            consistency_days / 7 * 100
        )

        productivity_score = (
            progress_percent * 0.7
            +
            consistency_percent * 0.3
        )

        st.subheader("🎯 Weekly Progress")

        st.metric(
            "Tasks Completed",
            f"{completed_tasks}/{total_tasks}"
        )

        st.progress(progress_percent / 100)

        st.success(
            f"{progress_percent:.1f}% completed"
        )

        st.markdown("---")

        st.subheader("📊 Subject-wise Completion")

        subject_data = []

        for subject in subject_total:

            completed = subject_completed.get(subject, 0)

            total = subject_total[subject]

            percent = (
                completed / total * 100
                if total > 0 else 0
            )

            subject_data.append({
                "Subject": subject,
                "Completion": percent
            })

        if subject_data:

            df = pd.DataFrame(subject_data)

            fig = px.bar(
                df,
                x="Subject",
                y="Completion",
                title="Subject Completion (%)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("---")

        st.subheader("📈 Consistency")

        st.metric(
            "Active Days",
            f"{consistency_days}/7"
        )

        st.progress(consistency_percent / 100)

        st.write(
            f"Consistency Score: {consistency_percent:.1f}%"
        )

        st.markdown("---")

        st.subheader("🏆 Productivity Score")

        st.metric(
            "Score",
            f"{productivity_score:.1f}/100"
        )

        if productivity_score >= 90:

            quote = """
🏆 Exceptional work!

You are operating at an elite level.
Keep this momentum going.
"""

        elif productivity_score >= 75:

            quote = """
🚀 Excellent progress!

You're building strong habits and moving steadily toward your goals.
"""

        elif productivity_score >= 60:

            quote = """
💪 Good effort!

Stay consistent and your results will compound over time.
"""

        elif productivity_score >= 40:

            quote = """
📚 Progress is still progress.

Focus on completing one task at a time.
"""

        else:

            quote = """
🌱 Every expert started somewhere.

Today is a great day to restart and build momentum.
"""

        st.success(quote)

        if total_tasks > 0 and completed_tasks == total_tasks:

            st.balloons()

            st.success(
                "🎉 Amazing! You completed every task this week!"
            )

    st.markdown("</div>", unsafe_allow_html=True)
# # ---------------- STUDY & QUIZ ---------------- #
elif menu == "🧠 Study & Quiz":

    import datetime

    # ================= HARD ISOLATION RESET ================= #
    if st.session_state.get("active_menu") != "🧠 Study & Quiz":
        st.session_state["quiz_active"] = False
        st.session_state["quiz_data"] = None
        st.session_state["quiz_answers"] = {}

    st.session_state["active_menu"] = "🧠 Study & Quiz"

    # ================= HEADER ================= #
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("🧠 Study Vault & Smart Quiz")

    col1, col2 = st.columns(2)
    with col1:
        quiz_user_id = str(st.text_input("👤 User ID", value="1"))
    with col2:
        quiz_subject = st.selectbox(
            "📖 Subject",
            ["Math", "Physics", "Chemistry"],
            key="quiz_subject"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= NOTES ================= #
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("📤 Step 1: Manage Your Notes")

    content = st.text_area(
        "Paste your study notes here:",
        height=200,
        key="note_input"
    )

    if st.button("💾 Save to Vault"):
        if content.strip():
            res = requests.post(
                f"{API_URL}/study/add",
                data={
                    "user_id": quiz_user_id,
                    "subject": quiz_subject,
                    "content": content
                }
            )

            if res.status_code == 200:
                st.success("✅ Notes saved successfully!")
            else:
                st.error(res.text)
        else:
            st.warning("⚠️ Please enter notes first")

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= QUIZ GENERATION ================= #
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("🎯 Generate Quiz")

    diff = st.selectbox("🎚️ Difficulty", ["easy", "medium", "hard"])

    col1, col2 = st.columns(2)

    with col1:
        mcq_count = st.number_input("MCQs", 1, 20, 5)

    with col2:
        short_count = st.number_input("Short Questions", 0, 10, 2)

    long_count = st.number_input("Long Questions", 0, 10, 1)

    multi_select = st.checkbox("Enable Multi-Select MCQs")

    # ================= GENERATE QUIZ ================= #
    if st.button("🚀 Generate Quiz Now"):

        try:
            res = requests.post(
                f"{API_URL}/quiz/generate",
                json={
                    "user_id": int(quiz_user_id),
                    "subject": quiz_subject,
                    "difficulty": diff,
                    "mcq_count": mcq_count,
                    "short_count": short_count,
                    "long_count": long_count,
                    "multi_select": multi_select
                }
            )

            data = res.json()

            if not data.get("success"):
                st.error(data.get("error", "Quiz generation failed"))
                if data.get("raw_output"):
                    st.code(data["raw_output"])

            else:
                # ✅ FULL ISOLATION STORAGE
                st.session_state["quiz_active"] = True
                st.session_state["quiz_data"] = data.get("quiz", {})
                st.session_state["quiz_answers"] = {}

                st.success("✅ Quiz Generated!")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= DISPLAY QUIZ (STRICT ISOLATION) ================= #
if (
    st.session_state.get("quiz_active") is True
    and st.session_state.get("quiz_data") is not None
):

    quiz = st.session_state["quiz_data"]

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("✍️ Quiz")

    answers = st.session_state.get("quiz_answers", {})

    mcqs = quiz.get("mcqs", [])
    shorts = quiz.get("short_questions", [])
    longs = quiz.get("long_questions", [])

    # ---------------- MCQs ---------------- #
    if mcqs:
        st.markdown("### 📝 Multiple Choice Questions")

        for i, q in enumerate(mcqs):

            st.write(f"**Q{i+1}. {q['question']}**")

            if q.get("multi_select", False):
                selected = st.multiselect(
                    "Choose:",
                    q["options"],
                    key=f"mcq_{i}"
                )
            else:
                selected = st.radio(
                    "Choose:",
                    q["options"],
                    key=f"mcq_{i}"
                )

            answers[f"mcq_{i}"] = selected

    # ---------------- SHORT ---------------- #
    if shorts:
        st.markdown("### ✏️ Short Questions")

        for i, q in enumerate(shorts):

            st.write(f"**Q{i+1}. {q['question']}**")

            answers[f"short_{i}"] = st.text_input(
                "Your Answer",
                key=f"short_answer_{i}"
            )

    # ---------------- LONG ---------------- #
    if longs:
        st.markdown("### 📚 Long Questions")

        for i, q in enumerate(longs):

            st.write(f"**Q{i+1}. {q['question']}**")

            answers[f"long_{i}"] = st.text_area(
                "Your Answer",
                key=f"long_answer_{i}"
            )

    # ================= SUBMIT ================= #
    if st.button("✅ Submit Quiz"):

        st.markdown("## 📊 Quiz Analysis")

        mcq_score = 0
        mcq_total = len(mcqs)
        wrong_topics = []

        # ---------------- MCQ CHECK (FIXED COLORS) ---------------- #
        for i, q in enumerate(mcqs):

            user_answer = answers.get(f"mcq_{i}")
            correct_answer = q["answer"]

            if user_answer == correct_answer:
                mcq_score += 1

                st.markdown(
                    f"""
                    <div style="
                        background-color:#d1f7d6;
                        color:#0b2e13;
                        padding:10px;
                        border-radius:8px;
                        margin-bottom:8px;
                        font-weight:600;
                    ">
                    ✅ MCQ {i+1}: Correct
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div style="
                        background-color:#ffd6d6;
                        color:#3b0a0a;
                        padding:10px;
                        border-radius:8px;
                        margin-bottom:8px;
                        font-weight:600;
                    ">
                    ❌ MCQ {i+1}: Wrong
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<span style='color:#111;font-weight:500;'>Your Answer: {user_answer}</span>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<span style='color:#111;font-weight:500;'>Correct Answer: {correct_answer}</span>",
                    unsafe_allow_html=True
                )

                if q.get("explanation"):
                    st.info(q["explanation"])

                wrong_topics.append(q["question"])

            st.divider()

        # ---------------- SHORT ---------------- #
        for i, q in enumerate(shorts):
            try:
                response = requests.post(
                    f"{API_URL}/quiz/evaluate-written",
                    json={
                        "question": q["question"],
                        "expected_answer": q["answer"],
                        "student_answer": answers.get(f"short_{i}", "")
                    }
                )

                result = response.json()

                st.markdown(
                    f"""
                    <div style="
                        background-color:#eef2ff;
                        color:#111;
                        padding:10px;
                        border-radius:8px;
                        margin-bottom:8px;
                    ">
                    ✏️ Short Q{i+1} <br>
                    Score: {result.get('score',0)}/{result.get('out_of',10)} <br>
                    Feedback: {result.get('feedback','')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Evaluation failed: {e}")

            st.divider()

        # ---------------- LONG ---------------- #
        for i, q in enumerate(longs):
            try:
                response = requests.post(
                    f"{API_URL}/quiz/evaluate-written",
                    json={
                        "question": q["question"],
                        "expected_answer": q["answer"],
                        "student_answer": answers.get(f"long_{i}", "")
                    }
                )

                result = response.json()

                st.markdown(
                    f"""
                    <div style="
                        background-color:#eef2ff;
                        color:#111;
                        padding:10px;
                        border-radius:8px;
                        margin-bottom:8px;
                    ">
                    📚 Long Q{i+1} <br>
                    Score: {result.get('score',0)}/{result.get('out_of',10)} <br>
                    Feedback: {result.get('feedback','')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Evaluation failed: {e}")

            st.divider()

        # ---------------- FINAL SCORE ---------------- #
        percentage = round((mcq_score / mcq_total) * 100, 2) if mcq_total else 0

        st.markdown("## 🏆 Final Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("MCQ Score", f"{mcq_score}/{mcq_total}")

        with col2:
            st.metric("Percentage", f"{percentage}%")

        if percentage >= 80:
            st.success("🎉 Excellent understanding!")
        elif percentage >= 60:
            st.warning("👍 Good, but revise a bit.")
        else:
            st.error("📚 Needs improvement.")

        if wrong_topics:
            st.markdown("### 📖 Weak Topics")
            for t in wrong_topics:
                st.write(f"• {t}")

        st.session_state["quiz_active"] = False
        st.session_state["quiz_data"] = None
        st.session_state["quiz_answers"] = {} 


# ---------------- AI ASSISTANT ---------------- #
elif menu == "🤖 AI Assistant":

    # ================= THEME OUTPUT STYLE ================= #
    if st.session_state.get("theme", "bright") == "bright":
        st.markdown("""
        <style>
        .ai-output {
            color: #001F3F!important;
            background-color: #898AA6;
            padding: 10px;
            border-radius: 10px;
            border-left: 4px solid #36454F;
            font-weight: 10000;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("🤖 AI Study Assistant")

    # ================= SESSION STATE FIX ================= #
    if "assistant_user_id" not in st.session_state:
        st.session_state.assistant_user_id = 1

    if "assistant_subject" not in st.session_state:
        st.session_state.assistant_subject = "Math"

    # ================= INPUT ================= #
    raw_text = st.text_area(
        "📝 Paste your study material:",
        height=300,
        key="assistant_text_input"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.assistant_user_id = st.number_input(
            "👤 User ID",
            min_value=1,
            value=st.session_state.assistant_user_id,
            key="assistant_user_id_input"
        )

    with col2:
        st.session_state.assistant_subject = st.selectbox(
            "📖 Subject",
            ["Math", "Physics", "Chemistry", "Biology", "CS"],
            index=["Math", "Physics", "Chemistry", "Biology", "CS"].index(
                st.session_state.assistant_subject
            ),
            key="assistant_subject_input"
        )

    # ================= SAVE NOTES ================= #
    if st.button("🚀 Process & Index", type="primary"):

        if raw_text.strip():

            try:
                res = requests.post(
                    f"{API_URL}/study/add",
                    data={
                        "user_id": str(st.session_state.assistant_user_id),
                        "subject": str(st.session_state.assistant_subject),
                        "content": raw_text
                    }
                )

                if res.status_code == 200:
                    st.success("✅ Notes saved!")
                else:
                    st.error(f"❌ Failed: {res.text}")

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("⚠️ Empty text!")

    st.markdown("---")

    # ================= TABS ================= #
    tab1, tab2 = st.tabs(["📋 Smart Summary", "💬 Ask Anything"])

    # ---------------- TAB 1: SUMMARY ---------------- #
    with tab1:

        st.subheader("📋 Smart Summary")

        if st.button("✨ Generate Summary", use_container_width=True):

            try:
                res = requests.get(
                    f"{API_URL}/study/summarize",
                    params={
                        "user_id": str(st.session_state.assistant_user_id),
                        "subject": str(st.session_state.assistant_subject)
                    }
                )

                if res.status_code == 200:

                    data = res.json()
                    summary = data.get("summary", "")

                    if summary:

                       st.markdown("### 📝 Summary")

                       clean_summary = summary.replace("\n", "<br>")

                       st.markdown(
        f"<div class='ai-output'>{clean_summary}</div>",
        unsafe_allow_html=True
    )

                    else:
                        st.warning("⚠️ Empty summary")

                else:
                    st.error(f"API Error: {res.text}")

            except Exception as e:
                st.error(f"Summary Error: {e}")

    # ---------------- TAB 2: Q&A ---------------- #
    with tab2:

        st.subheader("💬 Ask Anything")

        q = st.text_input("Ask a question:", key="assistant_query")

        if st.button("Ask", use_container_width=True):

            if not q.strip():
                st.warning("Enter a question")

            else:

                try:
                    res = requests.post(
                        f"{API_URL}/study/query",
                        json={
                            "user_id": str(st.session_state.assistant_user_id),
                            "subject": str(st.session_state.assistant_subject),
                            "query": q
                        }
                    )

                    if res.status_code == 200:
                        answer = res.json().get("answer", "No answer")

                        st.markdown("### 💡 Answer")

                        # 🔥 BLUE ANSWER STYLE
                        st.markdown(
                            f"<div class='ai-output'>{answer}</div>",
                            unsafe_allow_html=True
                        )

                    else:
                        st.error(f"Query failed: {res.text}")

                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)