import psycopg
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

load_dotenv()
DB_URL = os.getenv("DB_URL")

# File paths
LOCATIONS_CSV = PROJECT_ROOT / "data" / "processed" / "seed_data" / "uk_town_lat_lons.csv" 
MANUAL_LOCATIONS_CSV = PROJECT_ROOT / "data" / "raw" / "manual_remaining_uk_geocodes.csv" 
WIND_DATA_CSV = PROJECT_ROOT / "data" / "processed" / "seed_data" / "location_date_winds_only.csv" 

# Combine all API fetched geodata with the manual fetch
ALL_UK_LOCATIONS = pd.concat([LOCATIONS_CSV, MANUAL_LOCATIONS_CSV], ignore_index=True)

# Connection details
conn_info = DB_URL

# Load data
locations_df = pd.read_csv(ALL_UK_LOCATIONS)
wind_df = pd.read_csv(WIND_DATA_CSV)

# Clean string fields for consistent matching
locations_df['location_name'] = locations_df['location_name'].astype(str).str.strip()
wind_df['location_name'] = wind_df['location_name'].astype(str).str.strip()

with psycopg.connect(conn_info) as conn:
    with conn.cursor() as cur:
        
        # Insert locations
        for _, row in locations_df.iterrows():
            cur.execute("""
                INSERT INTO locations (location_name, latitude, longitude)
                VALUES (%s, %s, %s)
                ON CONFLICT (location_name) DO NOTHING
            """, (row['location_name'], row['latitude'], row['longitude']))
        conn.commit()  # Commit locations before wind data

        # Insert wind data in batches
        for i, row in wind_df.iterrows():
            cur.execute("""
                SELECT location_id FROM locations WHERE location_name = %s
            """, (row['location_name'],))
            location_result = cur.fetchone()

            if location_result:
                location_id = location_result[0]
                try:
                    cur.execute("""
                        INSERT INTO wind_data (location_id, date, wind_speed)
                        VALUES (%s, %s, %s)
                    """, (location_id, row['date'], row['wind_speed']))
                except Exception as e:
                    print(f"⚠️ Failed to insert row {i}: {e}")
            else:
                print(f"⚠️ Skipped row {i}: Location '{row['location_name']}' not found.")

            # Commit every 1000 rows
            if i % 1000 == 0:
                conn.commit()

        conn.commit()  # Final commit to catch any remaining rows

print("✅ Seeding db complete.")