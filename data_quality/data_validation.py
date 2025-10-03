from sqlalchemy import create_engine
import pandas as pd
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import sys

# Ensuring directory pathing is consistent
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

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
    not_uk_lat = df[(df[column] < 49.86) | (df[column] > 59.39)]
    return not_uk_lat if not not_uk_lat.empty else None

def check_uk_long (df, column):
    not_uk_long = df[(df[column] < -8.64) | (df[column] > 1.76)]
    return not_uk_long if not not_uk_long.empty else None

def check_wind_speed(df, column):
    unreal_winds = df[(df[column] < 0) | (df[column] > 99)]
    return unreal_winds if not unreal_winds.empty else None

# -----------------------------------

# Setup for logging

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logs_dir = PROJECT_ROOT / "data_quality" / "logs" 
logs_dir.mkdir(parents=True, exist_ok=True) 
log_file = logs_dir / f"data_validation_{timestamp}.log"

logging.basicConfig(
    filename=str(log_file),           
    level=logging.INFO,                       
    format='%(asctime)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'             
)

# --- Log specific functions --- #

def log_if_invalid(result, label):
    if result is not None:
        logging.warning(
            "\n=== Invalid data: %s (count: %d) ===\n%s\n===========================",
            label,
            len(result),
            result.to_string(index=False)
        )
    else:
        logging.info(f"{label}: None")

# --------------------------------

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

