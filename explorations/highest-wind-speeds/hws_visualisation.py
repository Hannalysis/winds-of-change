import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path
# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Build path to your CSV
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "queries" / "highest_wind_speeds.csv"

# Load your wind data
df = pd.read_csv(CSV_PATH)

st.title("~~~ Highest Wind Speed Map ~~~")
st.markdown("Each point represents a town")

# Layout: two columns
col1, col2 = st.columns([4, 1]) 


# Center the map on average lat/lon
map_center = [df["latitude"].mean(), df["longitude"].mean()]

# Create folium map
with col1:
    m = folium.Map(location=map_center, zoom_start=6.25)

    def get_fill_colour(hws_count):
        if hws_count == 2:
            return "gray"
        elif hws_count >= 3:
            return "black"
        else:
            return "white"
        
    def get_outline_colour(wind_speed):
        if wind_speed >= 64:
            return "navy"
        elif wind_speed >= 61:
            return "blue"
        else:
            return "teal"

    for _, row in df.iterrows():
        fill_colour = get_fill_colour(row['high_wind_speed_count'])
        outline_colour = get_outline_colour(row['highest_wind_speed'])
        
        popup_text = f"""
        <strong>{row['location_name']}</strong><br>
        {row['highest_wind_speed']} km/h
        """

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5 + (row['highest_wind_speed'] * 1.5/ 5),
            color=fill_colour,
            fill=True,
            fill_color=outline_colour,
            fill_opacity=0.7,
            popup=popup_text,
            tooltip=folium.Tooltip(popup_text)
        ).add_to(m)

    st_folium(m, width=675, height=600)

with col2:
    st.markdown("""
    ** **            
    **Key**
    ** **

    **Fill Color**  
    *Teal -> Navy*             
    (60+ km/h)

    **Border Color**  
    *Grey -> Black*  
    (2+ high wind speed occurences)
    ** **
    """)

st.dataframe(df[['location_name', 'highest_wind_speed', 'high_wind_speed_count']])