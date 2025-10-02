import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import logging
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("DB_URL")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))
LOCATIONS_CSV = PROJECT_ROOT / "data" / "processed" / "seed_data" / "uk_town_lat_lons.csv" 

# Load the updated UK town geodata
df = pd.read_csv(LOCATIONS_CSV)
df = df.rename(columns={
    'Town': 'town',
    'Latitude': 'latitude',
    'Longitude': 'longitude'
})

engine = create_engine(DB_URL)

# Writing the df to a temporary table in the database
df.to_sql('temp_latlongs', con=engine, if_exists='replace', index=False)

# Setup for Logging ---

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logs_dir = PROJECT_ROOT / "scripts" / "local_db" / "logs" 
logs_dir.mkdir(parents=True, exist_ok=True) 
log_file = logs_dir / f"lat_long_cleanup_{timestamp}.log"

logging.basicConfig(
    filename=str(log_file),           
    level=logging.INFO,                       
    format='%(asctime)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'             
)
# ---------------------

with engine.begin() as conn: 

    # Update locations table joining temp_latlongs
    update_sql = text("""
        UPDATE locations AS l
        SET latitude = t.Latitude,
            longitude = t.Longitude
        FROM temp_latlongs AS t
        WHERE TRIM(LOWER(l.location_name)) = TRIM(LOWER(t.town))
        AND (l.latitude IS DISTINCT FROM t.Latitude OR l.longitude IS DISTINCT FROM t.Longitude)     
        RETURNING l.location_name
    """)

    result = conn.execute(update_sql)
    updated_locations = result.fetchall()
    print(f"Updated {len(updated_locations)} rows:")
    logging.info(f"Updated {len(updated_locations)} rows:")
    for row in updated_locations:
        print(f"- {row.location_name}")
        logging.info(f"{row.location_name}")