import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('../data/raw/all_weather_data.csv')

# Select only the desired columns
filtered_df = df[['location', 'date', 'wind_speed km/h']]

# Save the filtered DataFrame to a new CSV file within the seed_data folder
filtered_df.to_csv('../data/processed/seed_data/location_date_winds_only.csv', index=False)

print("CSV for wind data file saved successfully!")
