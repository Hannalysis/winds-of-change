from sqlalchemy import create_engine
import pandas as pd
import os
import logging
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
    return None if not invalid_format else list(invalid_format)

def check_date_format(df, column, date_format='%Y-%m-%d'):
    try:
        pd.to_datetime(df[column], format=date_format, errors='raise')
        return None 
    except Exception as e:
        invalid_dates = pd.to_datetime(df[column], format=date_format, errors='coerce')
        return df[invalid_dates.isna()]

def check_uk_lat (df, column):
    not_uk_lat = df[(df[column] < 49) | (df[column] > 61)]
    return not_uk_lat if not not_uk_lat.empty else None

def check_uk_long (df, column):
    not_uk_long = df[(df[column] < -8) | (df[column] > 2)]
    return not_uk_long if not not_uk_long.empty else None

def check_wind_speed(df, column):
    unreal_winds = df[(df[column] < 0) | (df[column] > 99)]
    return unreal_winds if not unreal_winds.empty else None

# -----------------------------------

# Setup for logging

logging.basicConfig(
    filename='data_validation.log',           
    level=logging.INFO,                       
    format='%(asctime)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'             
)

# --- Log specific functions --- #

def log_if_invalid(result, label):
    if result is not None:
        logging.warning(
            "\n=== Invalid data: %s ===\n%s\n===========================",
            label,
            result.to_string(index=False)
        )

# Log each validation for locations

logging.info("-" * 15)
logging.info("Locations table")
logging.info("-" * 15)

logging.info("\n Null Counts:")
logging.info(check_nulls(locations_df))

logging.info("\n Duplicate Rows:")
logging.info(f"Total duplicates: {check_duplicates(locations_df)}")

logging.info("\n Format Checks:")
logging.info(f"Location_names not title cased: {check_location_format(locations_df, 'location_name')}")

logging.info("\n Range Checks:")
lat_result = check_uk_lat(locations_df, 'latitude')
log_if_invalid(lat_result, "Latitudes outside of UK ranges")
long_result = check_uk_long(locations_df, 'longitude')
log_if_invalid(long_result, "Longitudes outside of UK ranges")

logging.info("\n")

# Log each validation for wind_data

logging.info("-" * 15)
logging.info("Wind_Data table")
logging.info("-" * 15)

logging.info("\n Null Counts:")
logging.info(check_nulls(wind_df))

logging.info("\n Duplicate Rows:")
logging.info(f"Total duplicates: {check_duplicates(wind_df)}")

logging.info("\n Format Checks:")
logging.info(f"Date formatting issues: {check_date_format(wind_df, 'date')}")

logging.info("\n Range Checks:")
logging.info(f"Wind speed outside of reasonable ranges: {check_wind_speed(wind_df, 'wind_speed')}")

# Print each validation for locations

print("-" * 15)
print("Locations table")
print("-" * 15)

print("\n🧪 Null Counts:")
print(check_nulls(locations_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(locations_df)}")

print("\n🧪 Format Checks:")
print(f"Location_names not title cased: {check_location_format(locations_df, 'location_name')}")

print("\n🧪 Range Checks:")
print(f"Latitudes outside of UK ranges: {check_uk_lat(locations_df, 'latitude')}")
print(f"Longitudes outside of UK ranges: {check_uk_long(locations_df, 'longitude')}")

print("\n")

# Print each validation for wind_data

print("-" * 15)
print("Wind_Data table")
print("-" * 15)

print("\n🧪 Null Counts:")
print(check_nulls(wind_df))

print("\n🧪 Duplicate Rows:")
print(f"Total duplicates: {check_duplicates(wind_df)}")

print("\n🧪 Format Checks:")
print(f"Date formatting issues: {check_date_format(wind_df, 'date')}")

print("\n🧪 Range Checks:")
print(f"Wind speed outside of reasonable ranges: {check_wind_speed(wind_df, 'wind_speed')}")
