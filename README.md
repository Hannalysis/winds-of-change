<h1 align = "center">Visualising Wind Power Potential in the UK</h1>

<p align = "center"><b>Overview</b>: This is a geospatial heatmap showcasing the wind speed (in km/h) at various locations across England in 2024. 
The heatmap visualises the intensity of wind speed at different wind turbine locations.</p>

<p align = "center">
  <img align = "center" src="/readme-images/winds-of-change.PNG" alt="df-city-loc-wind-speed-and-geospatial-heatmap-of-uk">
</p>

------------

<h2>Table of Contents</h2>


- [Installation](#installation)
- [Brief](#my-brief)
- [Documentation](#documentation)
  - [Supplements](#project-supplements)
  - [Tech Stack](#tech-stack-including)
- [Progress](#mvp---completed-20250316)
  - [Future Milestones](#future-milestones)
- [Author](#author)

------------

## Installation

To run the demo MVP via the repo - Inside your VScode terminal, enter the following:

```bash
    pip install pandas streamlit folium streamlit-folium  
    streamlit run main.py
```
... and open the local http link provided.

------------

## My Brief  

<i>The goal of this project is to explore advanced Python-based data visualisation libraries while addressing a subject I am deeply passionate about: renewable energy. Specifically, I aim to analyse the effectiveness of current wind farm locations in the UK, assessing whether these sites are optimally utilised. Additionally, I will investigate potential areas for new wind farm development, using data-driven insights to inform future decisions on sustainable energy deployment.</i>

------------

## Documentation 

# <h3><u>Project Supplements</u></h3>  


- UK weather data: Kaggle.com/datasets, under the <i>"2M+ Daily Weather History UK"</i>.
- UK geo location data: Nominatom.openstreetmap.org
- UK wind turbine locations: TheWindPower.net


# <h3><u>Tech Stack including:</u></h3>  

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,vscode,postgresql&perline=8" />
  </a>
  <h4><u>Python Main modules:</u><br/><span style = "font-weight:lighter">Pandas, Streamlit, Folium</span></h4>
  <h4><u>Python Helper Script modules:</u><br/><span style = "font-weight:lighter">Requests, CSV, Time</span></h4>
</p>

# <h3><u>MVP</u> - Completed: 2025/03/16</h3>

- Basic small data sample of wind speed (last recorded end of 2024) for major cities in the UK 
- Functional basic dataframe visualisation of the sample dataset
- Functional geospatial map of the UK renders appropriately
- Basic Style Formatting and rendered with Streamlit

<h3><u>MS1</u> - Currently working on</h3>

- Increasing the Dataset size; every major town/city within the UK and all wind speed information from a recent time period (ie 2024) therefore...
- Analysing the raw data: Drop all unrelated weather columns, and check for any missing values
- Utilise all town names to create a script to fetch geo data from an API and store in a local CSV; check for any unsuccessful entries, and re-fetch or manually obtain/delete entries as necessary
- Seed the winds and geo csv files into a local SQL database instance 

## Future Milestones

<h3><u>MS2</u></h3>

- Increasing the Dataset size; every major town/city within the UK and all wind speed information
- Utilising the data effectively; avg vs highest (visual toggle)
- An additional layer (toggle) to show the current wind farm locations 

<h3><u>MS3</u></h3>

- Increasing the Dataset scope: Locating data for villages, and offshore locations around the UK
- Increasing the Dataset size to account for more years for a more accurate prediction for the future wind conditions
- Implement a machine learning library (ie scikit) to aid future wind speed predictions 

## Author

Created by Hannahry
<i></br><b>aka: </b>@Hannalysis</i>

