import streamlit as st
import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/dailyobjectives.db')
query = "SELECT * FROM `Daily Objectives`"
df = pd.read_sql(query, conn)

# Streamlit app
st.title("Daily Objectives Viewer")

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

# Display data vertically
if not filtered_data.empty:
    for _, row in filtered_data.iterrows():
        for column in filtered_data.columns:
            if column in ['Youtube', 'PDFs', 'Epic Books']:
                # Display the heading
                st.write(f"**{column}:**")
                
                # Check if the cell is not None and has content
                cell_content = row[column]
                if cell_content:
                    # Split the data into individual items
                    items = cell_content.split('; ')
                    for item in items:
                        # Split each item into title and URL
                        if ':' in item:
                            title, url = item.split(': ', 1)
                            st.write(f"**{title}:** [{url}]({url})")
                        else:
                            st.write(item)
                else:
                    st.write("No data available")
            else:
                st.write(f"**{column}:** {row[column]}")
else:
    st.write("No data available for the selected date and subject.")
