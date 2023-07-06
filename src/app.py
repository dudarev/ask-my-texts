"""
Streamlit app that accepts a user's question and returns an answer using OpenAI's GPT-3.
"""

import os
import streamlit as st

from answer_questions import answer_question
from good_questions import GOOD_QUESTIONS
from sources import get_sources_markdown

# a developer may specify an OpenAI API key in `.env` file
# (see `.env.example` for an example)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

st.sidebar.title("Ask My Texts")
st.sidebar.markdown(
    """
This demo app uses OpenAI's GPT-3.5 API to answer questions based on the text of the stories 
"[The Tale of Peter Rabbit](https://en.wikisource.org/wiki/The_Tale_of_Peter_Rabbit_(1901))",
"[The Tale of Squirrel Nutkin](https://en.wikisource.org/wiki/The_Tale_of_Squirrel_Nutkin)",
"[The Tale of Benjamin Bunny](https://en.wikisource.org/wiki/The_Tale_of_Benjamin_Bunny)", and 
"[The Tale of Two Bad Mice](https://en.wikisource.org/wiki/The_Tale_of_Two_Bad_Mice)" 
by Beatrix Potter.
"""
)


st.sidebar.markdown("## Settings")


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="Paste your OpenAI API key here (sk-...)",
    help="You can get your API key from https://platform.openai.com/account/api-keys.\n"
    "The key will be stored in your browser's local storage.\n"
    "It's needed to get non-cached answers.",
    value=st.session_state.get("OPENAI_API_KEY", ""),
)
if api_key_input:
    set_openai_api_key(api_key_input)


st.sidebar.markdown(
    """
---
See [README](https://github.com/dudarev/ask-my-texts/blob/main/README.md) if you want to setup this app with your own texts.
"""
)


input = st.text_input("Question", key="question")


if "expand_examples" not in st.session_state:
    st.session_state.expand_examples = True


if st.button("Ask") or input:
    question = st.session_state.question
    with st.spinner("Requesting..."):
        open_api_key = os.environ.get("OPENAI_API_KEY") or st.session_state.get(
            "OPENAI_API_KEY", ""
        )
        answer = answer_question(question, open_api_key)
    answer_expander = st.expander("Answer", expanded=True)
    if question:
        answer_expander.write(answer["answer"])
        if answer.get("sources"):
            sources_expander = st.expander("Sources", expanded=True)
            sources_expander.write(get_sources_markdown(answer["sources"]))
    else:
        answer_expander.write("Please enter a question.")
    st.session_state.expand_examples = False


def click_example_question_button(q):
    st.session_state.update(question=q)
    st.session_state.update(expand_examples=False)


examples_expander = st.expander(
    "Example questions (cached answers)", expanded=st.session_state.expand_examples
)
for q in GOOD_QUESTIONS:
    examples_expander.button(
        q,
        on_click=click_example_question_button,
        args=(q,),
    )
