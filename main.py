import streamlit as st
import folium
import pandas as pd
# import numpy as np - # will likely be using this soon 
from folium.plugins import HeatMap
from streamlit_folium import st_folium 

# Function to generate wind power data (cached so it's not regenerated every time)
@st.cache_data
def generate_wind_power_data():
    # Generate some example data for locations in England
    city_coords = [
        {"city": "London", "lat": 51.5074, "lon": -0.1278},
        {"city": "Manchester", "lat": 53.4808, "lon": -2.2426},
        {"city": "Bristol", "lat": 51.4545, "lon": -2.5879},
        {"city": "Sheffield", "lat": 53.3811, "lon": -1.4701},
        {"city": "Leeds", "lat": 53.8008, "lon": -1.5491},
        {"city": "Liverpool", "lat": 53.4084, "lon": -2.9916}
    ]
    
    # Wind speed data for each city
    wind_speed_data = {
        "city": [entry["city"] for entry in city_coords],
        "lat": [entry["lat"] for entry in city_coords],
        "lon": [entry["lon"] for entry in city_coords],
        "wind_speed": [11, 10, 25, 18, 15, 19]  # Real wind speed for London in one day 2024
    }

    return pd.DataFrame(wind_speed_data)

# Function to generate the folium map (cached so it's not regenerated every time)
@st.cache_data
def create_folium_map(df):
    # Create a Folium map centered around England
    m = folium.Map(location=[52.3550, -1.1743], zoom_start=6)  # Approximate center of England

    # Prepare data for HeatMap layer (lat, lon, intensity)
    heat_data = [[row['lat'], row['lon'], row['wind_speed']] for _, row in df.iterrows()]

    # Add a HeatMap layer
    HeatMap(heat_data).add_to(m)

    return m

# Streamlit app
st.title("Geospatial Heatmap of Wind Speed vs Optimal Wind Turbine Usage in England (2024)")

st.write("""
This is a geospatial heatmap showcasing the wind speed (in km/h) at various locations across England in 2024. 
The heatmap visualises the intensity of wind speed at different wind turbine locations.
""")

# Fetch or generate wind power data (using session_state to persist it)
if "wind_power_data" not in st.session_state:
    st.session_state.wind_power_data = generate_wind_power_data()

# Display the DataFrame with the generated wind power data
st.write("### Wind Speed Data (km/h):")
st.dataframe(st.session_state.wind_power_data)

# Create and cache the map, based on the current data
m = create_folium_map(st.session_state.wind_power_data)

# Use Streamlit Folium integration to display the map
st.write("### Heatmap of Wind Speed:")
st_folium(m, width=700, height=500)  # Render the Folium map

# run with streamlit run heatmap_test_final.py
