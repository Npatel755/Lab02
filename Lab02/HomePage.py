import streamlit as st

st.set_page_config(page_title="Study Tracker", page_icon="📚")

st.title("Study Tracker")
st.write("This app compares sample study hours and tracks your own study sessions.")
st.write(
    "Open Visuals in the sidebar to compare total study hours. "
    "Choose a subject to see how its study hours change each week."
)
st.write(
    "Use Survey to save a subject and study hours for each session. "
    "Visuals also shows your survey totals and a session chart for a subject you choose."
)
st.caption("CS 1301 - Lab 2, Parts 1 and 2")
