"""
Streamlit app that accepts a user's question and returns an answer using OpenAI's GPT-3.
"""

from pathlib import Path
import streamlit as st

from answer_questions import answer_question
from good_questions import GOOD_QUESTIONS


st.title("Ask My Texts")

st.markdown(
    """
This demo app uses OpenAI's GPT-3.5 API to answer questions based on the text of the stories
"The Tale of Peter Rabbit",
"The Tale of Squirrel Nutkin",
"The Tale of Benjamin Bunny", and
"The Tale of Two Bad Mice"
by Beatrix Potter.
"""
)

input = st.text_input("", key="question")


if "expand_examples" not in st.session_state:
    st.session_state.expand_examples = True


if st.button("Ask") or input:
    question = st.session_state.question
    answer_expander = st.expander("Answer", expanded=True)
    if question:
        answer_expander.write(answer := answer_question(question)["answer"])
    else:
        answer_expander.write("Please enter a question.")
    st.session_state.expand_examples = False


def click_example_question_button(q):
    st.session_state.update(question=q)
    st.session_state.update(expand_examples=False)


expander = st.expander("Example questions", expanded=st.session_state.expand_examples)
for q in GOOD_QUESTIONS:
    expander.button(
        q,
        on_click=click_example_question_button,
        args=(q,),
    )
