import streamlit as st

def init_state():
    if "quiz_active" not in st.session_state:
        st.session_state["quiz_active"] = False

    if "quiz_data" not in st.session_state:
        st.session_state["quiz_data"] = None

    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}

def clear_quiz():
    st.session_state["quiz_active"] = False
    st.session_state["quiz_data"] = None
    st.session_state["quiz_answers"] = {}