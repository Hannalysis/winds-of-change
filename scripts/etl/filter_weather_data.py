import pandas as pd
from pathlib import Path
import sys

# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

WEATHER_CSV_PATH = PROJECT_ROOT / "data" / "raw" / "all_weather_data.csv"
WINDS_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "seed_data" / "location_date_winds_only.csv" 

# Load the CSV into a DataFrame
df = pd.read_csv(WEATHER_CSV_PATH)

# Select only the desired columns
filtered_df = df[['location', 'date', 'wind_speed km/h']]

# Save the filtered DataFrame to a new CSV file within the seed_data folder
filtered_df.to_csv(WINDS_CSV_PATH, index=False)

print("CSV for wind data file saved successfully!")
