import streamlit as st
import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('all_weather_data.csv')

# Display the DataFrame as a table in Streamlit
st.write(df[['location', 'date', 'wind_speed km/h']])

# Creating a bespoke filter to cut down csv data
filtered_df = df[['location', 'date', 'wind_speed km/h']]


# filtered_df = df[df['location'] == 'London']
# st.dataframe(filtered_df[['location', 'date', 'wind_speed km/h']])

# streamlit run csv_to_df.py

# Convert the DataFrame to a CSV file locally
filtered_df.to_csv('location_date_winds_only.csv', index=False)  # index=False prevents pandas from writing row numbers

print("CSV file saved successfully!")