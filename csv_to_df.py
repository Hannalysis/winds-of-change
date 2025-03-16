import streamlit as st
import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('all_weather_data.csv')

# Display the DataFrame as a table in Streamlit
# st.write(df[['location', 'date', 'wind_speed km/h']])

# Show rows where Column1 has the value 2
filtered_df = df[df['location'] == 'London']
st.dataframe(filtered_df[['location', 'date', 'wind_speed km/h']])