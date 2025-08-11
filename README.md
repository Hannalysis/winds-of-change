<h1 align = "center">Visualising Wind Power Potential in the UK</h1>

<p align = "center"><b>Overview</b>: This is a geospatial heatmap showcasing the wind speed (in km/h) at various locations across England in 2024. 
The heatmap aims to visualise the intensity of wind speed vs current wind turbine locations.</p>

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
  - [ETL Pipeline](#etl-pipeline)
- [Progress](#mvp---completed-20250316)
  - [Current Milestone](#ms15---in-progress)
  - [Future Milestones](#future-milestones)
- [Author](#author)

------------

## Installation

To run the demo MVP via the repo - Inside your VSCode terminal, enter the following:

```bash windows 
    py -m venv venv
    venv\Scripts\Activate.ps1
```

Then, install the required dependencies...

```bash
    pip install -r requirements.txt
```

...run with:

```bash
    streamlit run demo.py
```
... and open the local http link provided.

------------

## My Brief  

<i>The goal of this project is to explore advanced Python-based data visualisation libraries while addressing a subject I am passionate about: renewable energy. Specifically, I aim to analyse the effectiveness of current wind farm locations in the UK, assessing whether these sites are optimally utilised. Additionally, I will investigate potential areas for new wind farm development, using data-driven insights to inform future decisions on sustainable energy deployment.</i>

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
  <h4><u>Python Helper Script modules:</u><br/><span style = "font-weight:lighter">Psycopg, Requests, CSV, Time</span></h4>
</p>

# <h3><u>ETL Pipeline</u></h3>  

1. Raw dataset (obtained from Kaggle), save and reside in: `data/raw/all_weather_data.csv`
2. Filter only useful columns (<i>filter_weather_data.py</i>) → `data/processed/seed_data/location_date_winds_only.csv`
3. Enrich town data with lat/long with an external API (<i>uk_lat_long_fetch.py</i>) → `data/processed/seed_data/town_lat_lons.csv`
4. Seed processed data files into a local postgres database (<i>seed.py</i>)

# <h3><u>MVP</u> - Completed: 2025/03/16</h3>

- Basic small data sample of wind speed (last recorded end of 2024) for major cities in the UK 
- Functional basic dataframe visualisation of the sample dataset
- Functional geospatial map of the UK renders appropriately
- Basic Style Formatting and rendered with Streamlit

<h3><u>MS1</u> - Completed: 2025/04/13</h3>

- Increased the Dataset size; included every major town/city within the UK and all wind speed information
- Transformed the raw data: Dropped all unrelated weather columns, and checked for any missing values
- Utilised all town names to create a script to fetch geo data from an API to enrich the data and store in a local CSV; checked for any unsuccessful entries, and re-fetched or manually obtained entries as necessary
- Ensured consistency between the two csv files whether information is related
- Seeded the winds and geo csv files and load them into a local SQL database instance 

<h4>Data successfully seeded</h4>

<p align = "center">
  <img align = "center" src="/readme-images/wind-data-seeded-sql-scaled.PNG" alt="pgadmin-wind-data-select-all-2807998-entries">
</p>

<p align = "center">
  <img align = "center" src="/readme-images/locations-seeded-sql-scaled.PNG" alt="pgadmin-location-data-select-all-501-entries">
</p>

⚠️ <i>Note: Due to the file size of the wind-data, that csv (and the raw files) are not available inside the repo at present</i>

# <h3><u>MS1.5</u> - Completed: 2025/07/22</h3>

- Refactored the project hierarchy
- Adjusted the script outputs to match the new structure [- See Data Pipeline](#etl-pipeline)

## Future Milestones

<h3><u>MS2</u></h3>

- Sanity check the transformed data within the database; add data validation
- CLI implementation 
- Create relevant aggregated queries that can be visualised with dfs and folium to display on the front-end

<h3><u>MS3</u></h3>

- An additional layer (toggle) to show the current wind farm locations 
- Increase the Dataset scope: Locating data for villages, and offshore locations around the UK

<h3><u>MS4</u></h3>

- Implement a machine learning library (ie scikit) to aid future wind speed predictions 

## Author

Created by Hannahry
<i></br><b>aka: </b>@Hannalysis</i>

