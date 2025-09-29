
import streamlit as st
import random
import json

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

def get_new_test():
    if len(all_questions) < 25:
        st.error("Der er ikke nok spørgsmål i databasen til at starte en test. Mindst 25 spørgsmål kræves.")
        return []
    return random.sample(all_questions, 25)

st.set_page_config(page_title="Medborgerskabsprøven Øveapp", layout="centered")

if "test" not in st.session_state:
    st.session_state.test = get_new_test()
    st.session_state.answers = [None] * len(st.session_state.test)
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.completed = False

if st.session_state.test:
    st.title("🇩🇰 Medborgerskabsprøven Øveapp")

    q = st.session_state.test[st.session_state.current_question]
    st.subheader(f"Spørgsmål {st.session_state.current_question + 1} af {len(st.session_state.test)}")
    st.markdown(f"**{q['question_da']}**")
    st.markdown(f"*{q['question_en']}*")

    options = [f"{opt['da']} / {opt['en']}" for opt in q["choices"]]
    answer = st.radio("Vælg dit svar:", options, index=st.session_state.answers[st.session_state.current_question] or -1)

    if st.button("Indsend svar"):
        selected = options.index(answer)
        st.session_state.answers[st.session_state.current_question] = selected
        if selected == q["correct"]:
            st.session_state.score += 1

        st.session_state.current_question += 1
        if st.session_state.current_question >= len(st.session_state.test):
            st.session_state.completed = True

    if st.session_state.completed:
        st.success(f"Du fik {st.session_state.score} ud af {len(st.session_state.test)} rigtige.")
        if st.session_state.score >= 20:
            st.balloons()
            st.success("🎉 Tillykke! Du bestod testen.")
        else:
            st.warning("❌ Du bestod ikke testen. Prøv igen.")

        if st.button("Tag testen igen"):
            st.session_state.test = get_new_test()
            st.session_state.answers = [None] * len(st.session_state.test)
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.completed = False
