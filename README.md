<h1 align = "center">Winds of Change</h1>

<h2 align = "center">A Data-Driven Pipeline to Explore UK Wind Power Potential</h2>

<p align = "center"><b>Overview</b>: This project is a data pipeline that analyses UK wind speed data, and visualises the outputs using Folium. </p>

<p align = "center">
  <img src= "/readme-images/init-vis-top-half.jpg" alt="init-exploration-visualisation-hws" width="45%" style="margin-right:12px;"  />
  <img src="/readme-images/init-vis-zoomed-in-map-markers-ex.jpg"
  alt="init-exploration-zoomed-in-example-hws" width="45%" />
</p>

The overall intent will include additional layers such as current wind farm locations, and wind predictions to suggest where future farms could potentially be built. 

------------

<h2>Table of Contents</h2>


- [Installation](#installation)
- [Brief](#my-brief)
- [Documentation](#documentation)
  - [Supplements](#documentation) <!-- re-using doc link to avoid double line formatting -->
  - [Tech Stack](#tech-stack-including)
  - [ETL Pipeline](#etl-pipeline)
  - [Data Validation](#data-validation---tables)
    - [Validation Sweeps](#data-validation---sweeps)
  - [Unit Testing](#unit-testing)
- [Progress](#progress)
  - [Current Milestone](#ms2---in-progress)
  - [Future Milestones](#future-milestones)
- [Author](#author)

------------

## Installation

To follow through with the overall data process, please navigate to [ETL Pipeline](#etl-pipeline)

Else if you'd like to run the initial visualisation locally via the repo, feel free to follow the steps below. </br>
Inside your VSCode terminal, enter the following:

```bash windows 
    py -m venv venv
    venv\Scripts\Activate.ps1
```

Then, install the required dependencies:

```bash
    pip install -r requirements.txt
```

Change the directory with this command:

```bash
    cd .\explorations\highest-wind-speeds\
```

And run with:

```bash
    streamlit run .hws_visualisation.py
```
... and open the local http link provided.

------------

## My Brief  

<i>The goal of this project is to explore advanced Python-based data visualisation libraries while addressing a subject I am passionate about: renewable energy. Specifically, I aim to analyse the effectiveness of current wind farm locations in the UK, assessing whether these sites are optimally utilised. Additionally, I will investigate potential areas for new wind farm development, using data-driven insights to inform future decisions on sustainable energy deployment.</i>

------------

## Documentation 

<h3><u>Project Supplements</u></h3>  

- UK weather data: Kaggle.com/datasets, under the <i>"2M+ Daily Weather History UK"</i>.
- UK geo location data: Nominatom.openstreetmap.org
- UK wind turbine locations: TheWindPower.net

# <h3><u>Tech Stack including:</u></h3>  

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,postgresql,vscode&perline=8" />
  </a>
  <h4><u>Main modules:</u><br/><span style = "font-weight:lighter">pandas, sqlalchemy, folium, streamlit, dotenv, os</span></h4>
  <h4><u>Script modules:</u><br/><span style = "font-weight:lighter">psycopg, requests, pathlib, sys, csv, time, logging</span></h4>
</p>

# <h3><u>ETL Pipeline</u></h3>  

1. Raw dataset (obtained from Kaggle), save and reside in: `data/raw/all_weather_data.csv`
2. Filter only useful columns (<i>filter_weather_data.py</i>) → `data/processed/seed_data/location_date_winds_only.csv`
3. Enrich town data with lat/long with an external API (<i>uk_lat_long_fetch.py</i>) → `data/processed/seed_data/town_lat_lons.csv`
4. Seed processed data files into a local postgres database (<i>seed.py</i>)

# <h3><u>Data Validation - Tables</u></h3>  

<h4><b> Wind Data </b>(wind_data)</h4>

| Field       | Type       | Rule                                         |
|-------------|------------|----------------------------------------------|
| id          | int64      | Must be unique                               |
| location_id | int64      | One for each bespoke location                |
| date        | datetime64 | In YYYY-MM-DD format                         |
| wind_speed  | float64    | Within expected ranges (> 0 and < 100 km/h)  |

<h4><b> Locations </b>(locations)</h4>

| Field             |  Type               | Rule                              |
|-------------------|---------------------|-----------------------------------|
| location_id       |  int64              | Must be unique                    |
| location_name     |  object (string)    | Title cased                       |
| latitude          |  float64            | Within UK ranges (49.86 to 59.39) |
| longitude         |  float64            | Within UK ranges (-8.64 to 1.76)  |

<h4><b> Global Rules </b></h4>

- All rows must have non-null values in
- No duplicate rows should exist in the table

# <h3><u>Data Validation - Sweeps</u></h3> 

Sweep 1 | Opened: 2025-09-25 | Resolved: 2025-10-03 |  <a href="./data_quality/data-validation.md">data-validation.md</a>

# <h3><u>Unit Testing</u></h3> 

A `pytest` suite that validates the following:

| Subfolder       | Function/s                              |
|-----------------|-----------------------------------------|
| `scripts/`      | Geocode enrichment API fetch            |
| `utils/`        | CSV data extraction utility functions   |
| `data_quality/` | Data validation and integrity functions |

<p>Located in 📂 <a href="./tests">tests</a></p>

------------

## Progress

<h3><b>MVP</b> - Completed: 2025/03/16</h3>

- Basic small data sample of wind speed (last recorded end of 2024) for major cities in the UK 
- Functional basic dataframe visualisation of the sample dataset
- Functional geospatial map of the UK renders appropriately
- Basic Style Formatting and rendered with Streamlit

<h3><b>MS1</b> - Completed: 2025/04/13</h3>

- Increased the Dataset size; included every major town/city within the UK and all wind speed information
- Transformed the raw data: Dropped all unrelated weather columns, and checked for any missing values
- Utilised all town names to create a script to fetch geo data from an API to enrich the data and store in a local CSV; checked for any unsuccessful entries, and re-fetched or manually obtained entries as necessary
- Ensured consistency between the two csv files whether information is related
- Seeded the winds and geo csv files and load them into a local SQL database instance 

<h4>Local postgres database dataset successfully seeded</h4>

<p align = "center">
  <img align = "center" src="/readme-images/wind-data-seeded-sql-scaled.PNG" alt="pgadmin-wind-data-select-all-2807998-entries">
</p>

<p align = "center">
  <img align = "center" src="/readme-images/locations-seeded-sql-scaled.PNG" alt="pgadmin-location-data-select-all-501-entries">
</p>

⚠️ <i>Note: Due to the file size of the wind-data, that particular csv (and the raw files) are not available inside the repo</i>

<h3><b>MS1.5</b> - Completed: 2025/07/22</h3>

- Refactored the project hierarchy
- Adjusted the script outputs to match the new structure | [See Data Pipeline](#etl-pipeline)


# <h3><b>MS2</b> - In progress</h3>

- 🚧 Explorations & visualisations  
  - ✔️ Highest Wind Speed | <i><a href="./explorations/highest-wind-speeds/hws-query-process.md">Query Process</a></i> | 🗺️ Visualisation Result (to run, refer to [Installation](#installation))
  - 🚧 Highest Avg Wind Speed (per region - tbc) | ⏳ <i>Query Process</i>  | ⏳ Visualisation Result 
- ✔️ Add data validation
  - ✔️ Add data validation script & appropriate logging | <a href="./data_quality/data_validation.py">data_validation</a>
  - ✔️ Implement a script to update the local database with the necessary record removals, courtesy of the findings from the first data validation run |  <a href="./data_quality/data-validation.md">Sweep 1</a>
  - ✔️ Update the ETL pipeline to include omitting the irrelevant locations
- Add a data integrity assessment
- ✔️ Implement unit testing for helper scripts, utils & data validation functions
- CLI implementation

<h4>Local postgres database record removals successful</h4>

<p align = "center">
  <img src= "/readme-images/local-db-update-deleting-non-uk-records-wind-data-and-locations-table.jpg" alt="pgadmin-ss-wind-data-and-locations-records-updated" width="90%"/>
</p>

## Future Milestones

<h3><b>MS3</b></h3>

- An additional layer (toggle) to show the current wind farm locations 
- Increase the Dataset scope: Locating data for villages, and offshore locations around the UK

<h3><b>MS4</b></h3>

- Implement a machine learning library (ie scikit) to aid future wind speed predictions 

## Author

Created by Hannahry
<i></br><b>aka: </b>@Hannalysis</i>

