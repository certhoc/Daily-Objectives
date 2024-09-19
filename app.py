import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO

# Streamlit app
st.title("Daily Objectives Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload your SQLite database", type=["db"])

if uploaded_file is not None:
    try:
        # Load database from uploaded file
        with BytesIO(uploaded_file.read()) as db_file:
            conn = sqlite3.connect(db_file)
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
                    st.write(f"**{column}:** {row[column]}")
        else:
            st.write("No data available for the selected date and subject.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.write("Please upload a SQLite database file.")
