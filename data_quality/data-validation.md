<h1 align = "center">Data Validation Results</h1>

## Sweep 1 | Start: 2025-09-25
### Issues encountered:
- Latitude: 61 values outside of expected UK range (49 to 61)
- Longitude: 73 values outside of expected UK range (-8 to 2)

### Actions taken:
- Logged for review
- Updated UK geodata to be more accurate (in progress)
    - Mainland: 49.863 to 59.391, 1.761 to -8.649 | Northern Island 54.053 to 55.311, -5.453 to -7.920
    - Re-ran log with updated lat long ranges within the Data Validation process
- ETL Updated: Nominatom API fetch query now only lifts UK geolocations

### Log files:
- <a href=".\logs\data_validation_2025-09-25_13-13-39.log">📂 data_validation_2025-09-25_13-13-39.log</a>
- <a href=".\logs\data_validation_2025-10-01_12-12-45.log">📂 data_validation_2025-10-01_12-12-45.log</a>