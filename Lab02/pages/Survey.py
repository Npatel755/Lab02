# Collect study sessions and append them to data.csv.
import csv
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Study Survey", page_icon="📝")

# Use the same CSV file no matter which folder the app is started from.
data_path = Path(__file__).parent.parent / "data.csv"

st.title("Study Session Survey 📝")
st.write("Enter a subject and the hours you spent on one study session.")
st.write("Use the same subject name each time to keep your sessions together.")

with st.form("survey_form"):
    category_input = st.text_input("What subject did you study? (Example: Programming)")
    value_input = st.text_input("How many hours did you study? (Example: 1.5)")
    submitted = st.form_submit_button("Submit Data")

if submitted:
    subject = category_input.strip().title()

    if subject == "" or value_input.strip() == "":
        st.error("Please enter both a subject and your study hours.")
    else:
        # Text input is a string, so convert the hours before saving them.
        try:
            hours = float(value_input)
        except ValueError:
            st.error("Study hours must be a number, such as 1 or 1.5.")
        else:
            if not 0 < hours <= 24:
                st.error("Enter a number of hours greater than 0 and at most 24.")
            else:
                needs_header = not data_path.exists() or data_path.stat().st_size == 0
                # Append mode keeps previous responses. csv.writer handles commas.
                with open(data_path, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if needs_header:
                        writer.writerow(["Category", "Value"])
                    writer.writerow([subject, hours])

                st.success("Your study session has been saved!")
                st.write(f"Subject: {subject} | Study hours: {hours}")

st.divider()
st.header("Saved Study Sessions")

if data_path.exists() and data_path.stat().st_size > 0:
    current_data_df = pd.read_csv(data_path)
    if current_data_df.empty:
        st.info("No sessions yet. Submit your first study session above.")
    else:
        st.dataframe(current_data_df)
        st.write("Open Visuals in the sidebar to see charts of your responses.")
else:
    st.info("No sessions yet. Submit your first study session above.")
