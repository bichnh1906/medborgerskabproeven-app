
import streamlit as st
import json
import random

# Load question pool
with open("final_pool_for_streamlit.json", "r", encoding="utf-8") as f:
    question_pool = json.load(f)

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(question_pool, 25)
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answers = []

# Get current question
q = st.session_state.questions[st.session_state.current]

st.title("Medborgerskabsprøven Øveværktøj / Citizenship Test Practice Tool")

st.markdown(f"**Spørgsmål {st.session_state.current + 1} / Question {st.session_state.current + 1}**")
st.markdown(f"**DA:** {q['question_da']}")
st.markdown(f"**EN:** {q.get('question_en', '')}")

options = list(q["answers_da"].keys())
for opt in options:
    st.markdown(f"- **{opt}**: {q['answers_da'][opt]} / {q['answers_en'].get(opt, '')}")

selected = st.radio("Vælg dit svar / Choose your answer:", options, key=st.session_state.current)

if st.button("Bekræft / Submit"):
    st.session_state.answers.append(selected)
    correct = q["correct_option"]
    if selected == correct:
        st.session_state.score += 1
        st.success(f"Korrekt! / Correct! ({correct})")
    else:
        st.error(f"Forkert / Incorrect. Korrekt svar er / Correct answer is: {correct}")
    st.session_state.current += 1

    if st.session_state.current >= 25:
        st.markdown("---")
        st.subheader("Resultat / Result")
        st.markdown(f"**Score:** {st.session_state.score} / 25")
        if st.session_state.score >= 20:
            st.success("Du bestod testen! / You passed the test!")
        else:
            st.error("Du bestod ikke testen. / You did not pass the test.")
        st.markdown("Genstart appen for at prøve igen. / Restart the app to try again.")
        st.stop()
