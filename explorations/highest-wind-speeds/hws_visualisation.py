""" 
This visualisation is pulled from the csv created in 'prepare_hws_vis.py', which
uses the final query defined from the 'hws-query-process.md' document.
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path
# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Loading the wind data 
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "queries" / "highest_wind_speeds.csv"
df = pd.read_csv(CSV_PATH)

# --- Streamlit layout ---
st.title("~~~ Highest Wind Speed Map ~~~")
st.markdown("Locations where wind speeds of 60km/h and above, occurenced more than once")
col1, col2 = st.columns([4, 1]) 

# --- Create the folium map ---
map_center = [df["latitude"].mean(), df["longitude"].mean()]

with col1:
    m = folium.Map(location=map_center, zoom_start=6.25)

    # Where the circle borders are darker for higher wind speed occurrences
    def get_outline_colour(hws_count):
        if hws_count == 2:
            return "gray"
        elif hws_count >= 3:
            return "black"
        else:
            return "white"
        
    # Where the inside circle fills are deeper blue for higher wind speeds   
    def get_fill_colour(wind_speed):
        if wind_speed >= 64:
            return "navy"
        elif wind_speed >= 61:
            return "blue"
        else:
            return "teal"

    for _, row in df.iterrows():
        outline_colour = get_outline_colour(row['high_wind_speed_count'])
        fill_colour = get_fill_colour(row['highest_wind_speed'])
        
        popup_text = f"""
        <strong>{row['location_name']}</strong><br>
        {row['highest_wind_speed']} km/h
        """

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5 + (row['highest_wind_speed'] * 1.5/ 5),
            color=outline_colour,
            fill=True,
            fill_color=fill_colour,
            fill_opacity=0.7,
            popup=popup_text,
            tooltip=folium.Tooltip(popup_text) # Location and wind speed on hover
        ).add_to(m)

    st_folium(m, width=675, height=600)

# --- Create the folium map key ---
with col2:
    st.markdown("""
    ** **            
    **Key**
    ** **

    **Fill Colour**  
    *Teal -> Navy*             
    (60+ km/h)

    **Border Colour**  
    *Grey -> Black*  
    (2+ high wind speed occurences)
    ** **
    """)

# Displaying the relevant columns of the table in streamlit
st.dataframe(df[['location_name', 'highest_wind_speed', 'high_wind_speed_count']])