import psycopg
import pandas as pd
from config import PG_PW, PG_USER 

# 📁 File paths
LOCATIONS_CSV = "seed_data/town_lat_lons.csv"
WIND_DATA_CSV = "seed_data/location_date_winds_only.csv"

# 🔌 Connection details
conn_info = f"dbname=winds-of-change user={PG_USER} password={PG_PW} host=localhost port=5432"

# 📄 Load data
locations_df = pd.read_csv(LOCATIONS_CSV)
wind_df = pd.read_csv(WIND_DATA_CSV)

# 🧼 Clean string fields for consistent matching
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

print("✅ Seeding complete.")