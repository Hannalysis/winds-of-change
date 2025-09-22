from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

# Grab local .env info
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Get tables
engine = create_engine(DB_URL)
locations_df = pd.read_sql_table('locations', engine)
wind_df = pd.read_sql_table('wind_data', engine)

# --- Data Validation Functions --- #

def check_nulls(df):
    return df.isnull().sum()

def check_duplicates(df):
    return df.duplicated().sum()

# -----------------------------------

# Execute each validation for locations

print("-" * 15)
print("Locations table")
print("-" * 15)
print("🧪 Null Counts:")
print(check_nulls(locations_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(locations_df)}")

# Execute each validation for wind_data

print("-" * 15)
print("Wind_Data table")
print("-" * 15)
print("🧪 Null Counts:")
print(check_nulls(wind_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(wind_df)}")