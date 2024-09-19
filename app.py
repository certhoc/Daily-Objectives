import streamlit as st
import pandas as pd
import sqlite3
import os

# Streamlit app
st.title("Daily Objectives Viewer")

# Path to the database file in your GitHub repository
db_path = os.path.join("data", "dailyobjectives.db")

try:
    # Connect to the SQLite database file
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM 'Daily Objectives'"
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    # Date Picker
    selected_date = st.date_input("Select a Date", pd.to_datetime("today"))

    # Format the date to MM/DD/YYYY
    formatted_date = selected_date.strftime("%m/%d/%Y")
    st.write(f"Selected Date: {formatted_date}")

    # Dropdown Menu for Subject
    subjects = df['Subject'].unique()
    selected_subject = st.selectbox("Select a Subject", subjects)

    # Filter data based on selected date and subject
    filtered_data = df[(df['Date'] == formatted_date) & (df['Subject'] == selected_subject)]

    # Display data vertically without numbering entries
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            for column in filtered_data.columns:
                if column in ['PDFs', 'Youtube', 'Epic Books'] and pd.notna(row[column]):
                    # Assuming the format is "Title|URL"
                    title_url = row[column].split('|', 1)
                    if len(title_url) == 2:
                        title, url = title_url
                        # Display clickable link with title
                        st.markdown(f"**{column}:** [{title}]({url})")
                else:
                    st.write(f"**{column}:** {row[column]}")
    else:
        st.write("No data available for the selected date and subject.")
except Exception as e:
    st.error(f"An error occurred: {e}")
