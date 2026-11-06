import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Study Charts", page_icon="📊")


data_path = Path(__file__).parent.parent / "data.json"
with open(data_path, "r", encoding="utf-8") as file:
    data = json.load(file)

st.title(data["title"])
st.write(data["description"])
subjects = list(data["study_hours"])

st.header("Part 1: Sample Study Data (JSON)")

st.header("Total study hours")
totals = []
for subject in subjects:
    totals.append(sum(data["study_hours"][subject]))

bar_data = pd.DataFrame({"Subject": subjects, "Total hours": totals})
bar_chart = alt.Chart(bar_data).mark_bar().encode(
    x="Subject",
    y="Total hours",
).properties(title="Total study hours by subject")
st.altair_chart(bar_chart)



st.header("Study hours by week")
if "subject" not in st.session_state:
    st.session_state["subject"] = subjects[0]

st.selectbox("Choose a subject", subjects, key="subject")
subject = st.session_state["subject"]
line_data = pd.DataFrame({
    "Week": data["weeks"],
    "Study hours": data["study_hours"][subject],
})
st.line_chart(line_data, x="Week", y="Study hours")


st.divider()
st.header("Part 2: Survey Study Sessions (CSV)")
st.write("These charts use the study sessions saved on the Survey page.")

csv_path = Path(__file__).parent.parent / "data.csv"
if not csv_path.exists() or csv_path.stat().st_size == 0:
    st.info("Visit Survey and enter study sessions to create the CSV charts.")
else:
    survey_data = pd.read_csv(csv_path)
    if survey_data.empty:
        st.info("Visit Survey and enter study sessions to create the CSV charts.")
    else:
        # Static chart: totals depend only on the saved CSV responses.
        st.subheader("Total surveyed study hours by subject")
        survey_totals = survey_data.groupby("Category", as_index=False)["Value"].sum()
        survey_bar = alt.Chart(survey_totals).mark_bar().encode(
            x=alt.X("Category:N", title="Subject"),
            y=alt.Y("Value:Q", title="Total study hours"),
        ).properties(title="Total study hours from survey responses")
        st.altair_chart(survey_bar)

        # Dynamic chart: save the selected subject between Streamlit reruns.
        st.subheader("Study hours across sessions for a subject")
        survey_subjects = sorted(survey_data["Category"].unique())
        if "survey_subject" not in st.session_state:
            st.session_state["survey_subject"] = survey_subjects[0]

        st.selectbox("Choose a survey subject", survey_subjects, key="survey_subject")
        selected_subject = st.session_state["survey_subject"]
        subject_data = survey_data[survey_data["Category"] == selected_subject]
        session_data = pd.DataFrame({
            "Session": range(1, len(subject_data) + 1),
            "Study hours": subject_data["Value"].tolist(),
        })
        st.write(f"Study sessions for {selected_subject}, in the order they were submitted.")
        st.line_chart(session_data, x="Session", y="Study hours")
        if len(subject_data) == 1:
            st.caption("Add another session for this subject to see a line between sessions.")
