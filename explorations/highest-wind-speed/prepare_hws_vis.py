import psycopg
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "queries" / "highest_wind_speed.csv"

# Getting the db query ready
load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

# The final query from the first exploration
QUERY = """
SELECT *
FROM (
    SELECT DISTINCT ON (location_name)
        location_name,
        wind_speed AS highest_wind_speed,
        latitude,
        longitude,
        COUNT(*) OVER (PARTITION BY location_name) AS high_wind_speed_count
    FROM wind_data
    INNER JOIN locations ON locations.location_id = wind_data.location_id
    WHERE wind_speed >= 60
    ORDER BY location_name, wind_speed DESC
) AS top_wind_speed_per_location
WHERE high_wind_speed_count > 1
ORDER BY highest_wind_speed DESC, high_wind_speed_count DESC;
"""


def extract_to_csv():
    df = pd.read_sql(QUERY, engine)
    df.to_csv(CSV_PATH, index=False)
    print(f"Query CSV saved to {CSV_PATH}")

extract_to_csv()