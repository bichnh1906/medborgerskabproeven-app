import streamlit as st
import random
import json

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Initialize session state
if "questions" not in st.session_state or st.session_state.get("retake", False):
    st.session_state.questions = random.sample(all_questions, 25)
    st.session_state.answers = [None] * 25
    st.session_state.correct_count = 0
    st.session_state.submitted = False
    st.session_state.retake = False

st.title("Medborgerskabsprøven Practice App 🇩🇰🇬🇧")

# Display questions
for i, q in enumerate(st.session_state.questions):
    st.markdown(f"**{i+1}. {q['question_da']}**")
    st.markdown(f"*{q['question_en']}*")
    selected = st.radio(
        label="",
        options=list(range(4)),
        format_func=lambda x: f"{q['choices_da'][x]} / {q['choices_en'][x]}",
        index=st.session_state.answers[i] if st.session_state.answers[i] is not None else -1,
        key=f"q{i}"
    )
    st.session_state.answers[i] = selected
    st.markdown("---")

# Submit button
if st.button("Submit Answers"):
    st.session_state.correct_count = sum(
        1 for i, q in enumerate(st.session_state.questions)
        if st.session_state.answers[i] == q["correct_index"]
    )
    st.session_state.submitted = True

# Show results
if st.session_state.submitted:
    st.header("Results")
    st.write(f"Correct Answers: {st.session_state.correct_count} / 25")
    if st.session_state.correct_count >= 20:
        st.success("Congratulations! You passed the test 🎉")
    else:
        st.error("You did not pass the test. Try again!")

    st.header("Summary")
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"**{i+1}. {q['question_da']}**")
        st.markdown(f"*{q['question_en']}*")
        st.markdown(f"Your answer: {q['choices_da'][st.session_state.answers[i]]} / {q['choices_en'][st.session_state.answers[i]]}")
        st.markdown(f"Correct answer: {q['choices_da'][q['correct_index']]} / {q['choices_en'][q['correct_index']]}")
        st.markdown(f"**Explanation:** {q['explanation_da']}")
        st.markdown(f"*{q['explanation_en']}*")
        st.markdown("---")

    if st.button("Retake Test"):
        st.session_state.retake = True
        st.experimental_rerun()
