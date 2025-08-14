<h1 align = "center">Highest Wind Speed</h1>

<p align = "center"><b>Exploration 1</b>: What are the highest wind speeds available from this dataset? </p>

Starting with the initial query, by viewing everything in the wind data table:

```sql
SELECT * 
FROM wind_data
ORDER BY wind_speed DESC
LIMIT 10;
```
<i>Query execution time</i> <b>0.1</b> <i>sec </i>

---

This shows only `location_id`, so let's bring in the locations table:

```sql
SELECT * 
FROM wind_data
INNER JOIN locations ON locations.location_id = wind_data.location_id
ORDER BY wind_speed DESC
LIMIT 10;
```
<i>Query execution time</i> <b>0.3</b> <i>sec </i>

---

We have multiple id fields, which is not very read friendly, so we’ll now select specific columns:

```sql
SELECT date, wind_speed, location_name, latitude, longitude 
FROM wind_data
INNER JOIN locations ON locations.location_id = wind_data.location_id
ORDER BY wind_speed DESC
LIMIT 10;
```
<i>Query execution time</i> <b>0.3</b> <i>sec </i>

---

Now it’s clear we have multiple entries for the same location, Lintmill. It appears 3 times, which is encouraging as it could potentially be windy on a regular basis. However, as we are limiting to 10 queries, with the last 3 entries being the same figure, we are potentially cutting off other towns that could be equally likely to contain that highest wind speed.

So let’s state unique location names in our top 10:

```sql
SELECT DISTINCT(location_name) date, wind_speed, latitude, longitude 
FROM wind_data
INNER JOIN locations ON locations.location_id = wind_data.location_id
ORDER BY wind_speed DESC
LIMIT 10;
```
<i>Query execution time</i> <b>0.5</b> <i>sec </i>

---

An issue here. There are multiple entries for the same location, despite using that bespoke query. So that query did not work. Let’s try adding a subquery:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
ORDER BY wind_speed DESC
LIMIT 10;
```
<i>Query execution time</i> <b>7.5</b> <i>secs </i>

---

The last 3 entries wind speed are all matching (with 62km/h). So lets see whether there are other towns with this max speed too:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
WHERE wind_speed BETWEEN 62 AND 66
ORDER BY wind_speed DESC;
```
<i>Query execution time</i> <b>7.5</b> <i>secs </i>

---

Surprisingly, by chance the query generated no additional results, as we still had the same 10 records.

So let’s check by adding 61km/h:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
WHERE wind_speed BETWEEN 61 AND 66
ORDER BY wind_speed DESC;
```
<i>Query execution time</i> <b>7.5</b> <i>secs </i>

---

Thankfully, that did generate more results (12), so 23 total records that match that query’s criteria. As the result pool is still within reasonable filtered records, let’s query to say for any wind_speed 60 and above:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
WHERE wind_speed >= 60
ORDER BY wind_speed DESC;
```
<i>Query execution time</i> <b>7.5</b> <i>secs </i>

---

This added another two unique towns to the list, Hopeman and Lossiemouth. Let’s add back in some of that information we obstructed, by counting how many times each town could have had an entry within this range of wind speed, and creating a new column for it:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude,
        COUNT(*) OVER (PARTITION BY location_name) AS high_wind_speed_count
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    WHERE wind_speed >= 60
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
ORDER BY wind_speed DESC, high_wind_speed_count DESC;
```
<i>Query execution time</i> <b>0.1</b> <i>sec </i>

---

I realised here that the query I had entered was much faster even considering the added window function, so I decided to record all execution times. This made me realise that execution time differences depended on where I had placed the wind speed filter; inside the subquery.

I executed `EXPLAIN(ANALYZE, VERBOSE)` and it showed that my subquery from the previous execution only filtered 474 rows before the majority of the rest of the query…compared to 936k from this most recent query!

Anyway, final query for this question, lets say we only want to look at ones that actually had more than one instance of very high wind speed:

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        date,
        wind_speed,
        latitude,
        longitude,
        COUNT(*) OVER (PARTITION BY location_name) AS high_wind_speed_count
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    WHERE wind_speed >= 60
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
WHERE high_wind_speed_count > 1
ORDER BY wind_speed DESC, high_wind_speed_count DESC;
```

---

In summary, utilising these particular filters we have 12 towns that could be our main focus.

However, I did notice that during this entire process we only ever got results from 2023.
Also, just because these towns reached high speeds, does not mean they have a better wind speed average throughout the year.

Thoughts for the next investigation.

</div>
