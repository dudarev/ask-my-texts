import streamlit as st

if "options" not in st.session_state:
    st.session_state["options"] = ""


def sidebar_callback():
    st.session_state["options"] = st.session_state["sidebar"]


def button1_callback():
    st.session_state["options"] = "Another question"


def button2_callback():
    st.session_state["options"] = "Yet another question"


placeholder = st.empty()

st.sidebar.selectbox(
    "Examples:",
    (
        "Question one",
        "Question two",
        "Question three",
        "Question four",
        "Question five",
    ),
    key="sidebar",
    on_change=sidebar_callback,
)

st.button("Another question", on_click=button1_callback)
st.button("Yet another question", on_click=button2_callback)

with placeholder:
    text = st.text_area(f"", max_chars=1000, key="options")
