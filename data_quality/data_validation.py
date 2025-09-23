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

def check_location_format(df, column):
    known_uk_exceptions = {
        "Knight's Hill", 
        "Neal's Green", 
        "No Man's Heath", 
        "Page's Green", 
        "Regent's Park", 
        "St John's Wood", 
        "St Luke's", 
        "Ty'n-Y-Garn"
    }

    non_title_case = df[~df[column].astype(str).str.istitle()][column].unique()

    # Remove known UK exceptions from the title case checker
    invalid_format = [name for name in non_title_case if name not in known_uk_exceptions]
    return list(invalid_format) if not list(invalid_format).empty else None

def check_uk_lat (df, column):
    not_uk_lat = df[(df[column] < 49) | (df[column] > 61)]
    print(not_uk_lat[[column]])
    return not_uk_lat if not not_uk_lat.empty else None

def check_uk_long (df, column):
    not_uk_long = df[(df[column] < -8) | (df[column] > 2)]
    print(not_uk_long[[column]])
    return not_uk_long if not not_uk_long.empty else None

# -----------------------------------

# Execute each validation for locations

print("-" * 15)
print("Locations table")
print("-" * 15)
print("🧪 Null Counts:")
print(check_nulls(locations_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(locations_df)}")

print("\n🧪 Format Checks:")
print(f"Location_names not title cased: {check_location_format(locations_df, 'location_name')}")

print("\n🧪 Range Checks:")
print(f"Latitudes outside of UK ranges: {check_uk_lat(locations_df, 'latitude')}")
print(f"Longitudes outside of UK ranges: {check_uk_long(locations_df, 'longitude')}")

print("\n")
# Execute each validation for wind_data

print("-" * 15)
print("Wind_Data table")
print("-" * 15)
print("🧪 Null Counts:")
print(check_nulls(wind_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(wind_df)}")
