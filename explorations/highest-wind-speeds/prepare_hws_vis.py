from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path
# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.append(str(PROJECT_ROOT))
from utils import extract_to_csv

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "queries" / "highest_wind_speeds.csv"

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

# Saving to a local file for visualisation
extract_to_csv(QUERY, engine, CSV_PATH)