<h1 align = "center">Data Validation Results</h1>

## Sweep 1 | Start: 2025-09-25
### Issues encountered:
- Latitude: 61 values outside of expected UK range (49 to 61)
- Longitude: 73 values outside of expected UK range (-8 to 2)

### Actions taken:
- Logged for review
- Updated UK geodata to be more accurate:
    - Mainland: 49.863 to 59.391, 1.761 to -8.649 | Northern Island 54.053 to 55.311, -5.453 to -7.920
    - Re-ran log with updated lat long ranges within the Data Validation process
- ETL Updated: Nominatom API fetch query now only lifts UK geolocations
- Local DB Updated:
    - Ran script to replace locations with more accurate geodata | <a href="../scripts/local_db/lat_long_cleanup.py">lat_long_cleanup.py</a> 
    - Ran a couple of [SQL](#sql-query) queries in pgAdmin to remove the 2 remaining irrelevant locations and their respective wind data records; Hamberg and Abengourou (these would no longer be added during the ETL process due to the API UK geo fetch, so a manual removal is apt for my local db instance.)

### Log files:
- <a href=".\logs\data_validation_2025-09-25_13-13-39.log">📂 data_validation_2025-09-25_13-13-39.log</a>
- <a href=".\logs\data_validation_2025-10-01_12-12-45.log">📂 data_validation_2025-10-01_12-12-45.log</a>
- <a href="../scripts/local_db/logs/lat_long_cleanup_2025-10-02_14-55-02.log">📂 lat_long_cleanup_2025-10-02_14-55-02.log</a>

### SQL Queries:

```sql-query1-2025-10-02
DELETE FROM wind_data
USING locations
WHERE wind_data.location_id = locations.location_id
  AND locations.location_name IN ('Hamberg', 'Abengourou');
```
```sql-query2-2025-10-02
DELETE
FROM locations
WHERE location_name IN ('Abengourou', 'Hamberg');
```
## Sweep 1 | End: 2025-10-02