
import streamlit as st
import json
import random

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

def get_new_test():
    return random.sample(all_questions, 25)

if "test" not in st.session_state:
    st.session_state.test = get_new_test()
    st.session_state.answers = [None] * 25
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.submitted = False

def submit_answer():
    q = st.session_state.test[st.session_state.current]
    selected = st.session_state.selected
    st.session_state.answers[st.session_state.current] = selected
    if selected == q["correct"]:
        st.session_state.score += 1
    st.session_state.current += 1
    st.session_state.selected = None

def restart_test():
    st.session_state.test = get_new_test()
    st.session_state.answers = [None] * 25
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.submitted = False

st.title("Medborgerskabsprøven Practice App 🇩🇰🇬🇧")

if st.session_state.current < 25:
    q = st.session_state.test[st.session_state.current]
    st.subheader(f"Spørgsmål {st.session_state.current + 1}")
    st.write(q["da"])
    st.write(q["en"])
    st.radio("Vælg dit svar / Choose your answer:", options=list(range(1, 5)), format_func=lambda i: f"{q['choices'][i-1]}", key="selected")
    st.button("Submit", on_click=submit_answer)
else:
    st.session_state.submitted = True
    st.header("Test Summary")
    st.write(f"Du svarede korrekt på {st.session_state.score} ud af 25 spørgsmål.")
    if st.session_state.score >= 20:
        st.success("Du bestod testen! 🎉")
    else:
        st.error("Du bestod ikke testen. Prøv igen.")
    st.button("Retake Test", on_click=restart_test)
