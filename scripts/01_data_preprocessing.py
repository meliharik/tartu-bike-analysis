"""
Tartu Bike Data - Data Merging and Cleaning (Data Preprocessing)
=================================================================

This script loads, merges, cleans, and prepares raw Tartu bike-sharing data
for analysis.

Data Sets:
- routes_*.csv: General information about each bike trip
- locations_*.csv: GPS coordinates for each trip (time series)
- Smart Bike Tartu_july 2019.xlsx: Data dictionary

Outputs:
- processed_data/routes_cleaned.csv: Cleaned trip data
- processed_data/locations_cleaned.csv: Cleaned location data
- processed_data/data_quality_report.txt: Data quality report
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed_data')

# Create processed data folder
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("=" * 80)
print("TARTU BIKE DATA - DATA PREPROCESSING AND CLEANING")
print("=" * 80)

# ============================================================================
# 1. DATA LOADING
# ============================================================================

print("\n[1/5] Loading Data...")
print("-" * 80)

# Find and load all routes files
routes_files = [f for f in os.listdir(DATA_DIR) if f.startswith('routes_') and f.endswith('.csv')]
routes_files.sort()

print(f"Found routes files: {len(routes_files)}")
for f in routes_files:
    print(f"  - {f}")

# Merge routes data
routes_list = []
for file in routes_files:
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path)
    # Extract date from filename
    date_str = file.replace('routes_', '').replace('.csv', '')
    df['data_source_date'] = date_str
    routes_list.append(df)
    print(f"  ✓ {file}: {len(df)} records loaded")

routes_df = pd.concat(routes_list, ignore_index=True)
print(f"\nTotal routes records: {len(routes_df):,}")

# Find and load all locations files
locations_files = [f for f in os.listdir(DATA_DIR) if f.startswith('locations_') and f.endswith('.csv')]
locations_files.sort()

print(f"\nFound locations files: {len(locations_files)}")
for f in locations_files:
    print(f"  - {f}")

# Merge locations data
locations_list = []
for file in locations_files:
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path)
    # Extract date from filename
    date_str = file.replace('locations_', '').replace('.csv', '')
    df['data_source_date'] = date_str
    locations_list.append(df)
    print(f"  ✓ {file}: {len(df):,} records loaded")

locations_df = pd.concat(locations_list, ignore_index=True)
print(f"\nTotal locations records: {len(locations_df):,}")

# ============================================================================
# 2. DATA QUALITY ANALYSIS (INITIAL STATE)
# ============================================================================

print("\n[2/5] Analyzing Data Quality (Initial State)...")
print("-" * 80)

# Collect information for report
quality_report = []
quality_report.append("=" * 80)
quality_report.append("TARTU BIKE DATA - DATA QUALITY REPORT")
quality_report.append("=" * 80)
quality_report.append(f"\nReport Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Routes data quality
quality_report.append("\n" + "=" * 80)
quality_report.append("ROUTES DATA - INITIAL STATE")
quality_report.append("=" * 80)
quality_report.append(f"\nTotal Records: {len(routes_df):,}")
quality_report.append(f"Total Columns: {len(routes_df.columns)}")

quality_report.append("\n\nColumn Information:")
quality_report.append("-" * 80)
for col in routes_df.columns:
    null_count = routes_df[col].isnull().sum()
    null_pct = (null_count / len(routes_df)) * 100
    dtype = routes_df[col].dtype
    quality_report.append(f"{col:20s} | Type: {str(dtype):10s} | Null: {null_count:6,} ({null_pct:5.2f}%)")

# Locations data quality
quality_report.append("\n\n" + "=" * 80)
quality_report.append("LOCATIONS DATA - INITIAL STATE")
quality_report.append("=" * 80)
quality_report.append(f"\nTotal Records: {len(locations_df):,}")
quality_report.append(f"Total Columns: {len(locations_df.columns)}")

quality_report.append("\n\nColumn Information:")
quality_report.append("-" * 80)
for col in locations_df.columns:
    null_count = locations_df[col].isnull().sum()
    null_pct = (null_count / len(locations_df)) * 100
    dtype = locations_df[col].dtype
    quality_report.append(f"{col:20s} | Type: {str(dtype):10s} | Null: {null_count:6,} ({null_pct:5.2f}%)")

# Print summary to screen
print("\nRoutes Data Summary:")
print(f"  - Total Records: {len(routes_df):,}")
print(f"  - Total Columns: {len(routes_df.columns)}")
print(f"  - Columns with Null Values: {routes_df.isnull().any().sum()}")
print(f"  - Duplicate route_code: {routes_df['route_code'].duplicated().sum():,}")

print("\nLocations Data Summary:")
print(f"  - Total Records: {len(locations_df):,}")
print(f"  - Total Columns: {len(locations_df.columns)}")
print(f"  - Columns with Null Values: {locations_df.isnull().any().sum()}")

# ============================================================================
# 3. DATA CLEANING
# ============================================================================

print("\n[3/5] Cleaning Data...")
print("-" * 80)

initial_routes_count = len(routes_df)
initial_locations_count = len(locations_df)

# --- ROUTES CLEANING ---
print("\nCleaning routes data...")

# 3.1. Combine and fix date/time columns
print("  • Combining date and time columns...")
routes_df['unlock_datetime'] = pd.to_datetime(
    routes_df['unlockedat'] + ' ' + routes_df['unlockedattime'],
    errors='coerce'
)
routes_df['lock_datetime'] = pd.to_datetime(
    routes_df['lockedat'] + ' ' + routes_df['lockedattime'],
    errors='coerce'
)

# 3.2. Check and remove null datetime values
null_unlock = routes_df['unlock_datetime'].isnull().sum()
null_lock = routes_df['lock_datetime'].isnull().sum()
print(f"  • Invalid unlock_datetime: {null_unlock}")
print(f"  • Invalid lock_datetime: {null_lock}")

routes_df = routes_df.dropna(subset=['unlock_datetime', 'lock_datetime'])
print(f"  ✓ Removed {initial_routes_count - len(routes_df)} records with invalid dates")

# 3.3. Calculate and validate trip duration
routes_df['duration_minutes_calculated'] = (
    routes_df['lock_datetime'] - routes_df['unlock_datetime']
).dt.total_seconds() / 60

# Filter negative or extremely long trips (0-1440 minutes = 24 hours)
before_duration_filter = len(routes_df)
routes_df = routes_df[
    (routes_df['duration_minutes_calculated'] > 0) &
    (routes_df['duration_minutes_calculated'] <= 1440)
]
print(f"  ✓ Removed {before_duration_filter - len(routes_df)} records with invalid duration")

# 3.4. Distance validation (0-100 km)
before_distance_filter = len(routes_df)
routes_df = routes_df[
    (routes_df['length'] >= 0) &
    (routes_df['length'] <= 100)
]
print(f"  ✓ Removed {before_distance_filter - len(routes_df)} records with invalid distance")

# 3.5. Duplicate route_code check
before_dup = len(routes_df)
routes_df = routes_df.drop_duplicates(subset=['route_code'], keep='first')
print(f"  ✓ Removed {before_dup - len(routes_df)} duplicate route_code records")

# 3.6. Add time features
routes_df['unlock_hour'] = routes_df['unlock_datetime'].dt.hour
routes_df['unlock_dayofweek'] = routes_df['unlock_datetime'].dt.dayofweek
routes_df['unlock_date'] = routes_df['unlock_datetime'].dt.date
routes_df['unlock_month'] = routes_df['unlock_datetime'].dt.month
routes_df['unlock_day'] = routes_df['unlock_datetime'].dt.day

# Weekday/Weekend flag
routes_df['is_weekend'] = routes_df['unlock_dayofweek'].isin([5, 6]).astype(int)

# Time period (morning, afternoon, evening, night)
def get_time_period(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour < 22:
        return 'Evening'
    else:
        return 'Night'

routes_df['time_period'] = routes_df['unlock_hour'].apply(get_time_period)

print(f"  ✓ Added time features")

# 3.7. Clean string columns
text_columns = ['startstationname', 'endstationname', 'rfidnumber', 'CycleType', 'Membership']
for col in text_columns:
    if col in routes_df.columns:
        routes_df[col] = routes_df[col].astype(str).str.strip()

print(f"  ✓ Cleaned text columns")

# --- LOCATIONS CLEANING ---
print("\nCleaning locations data...")

# 3.8. Combine date/time columns
print("  • Combining date and time columns...")
locations_df['coord_datetime'] = pd.to_datetime(
    locations_df['coord_date'] + ' ' + locations_df['coord_time'],
    errors='coerce'
)

# Remove null datetime values
null_coord = locations_df['coord_datetime'].isnull().sum()
print(f"  • Invalid coord_datetime: {null_coord}")
locations_df = locations_df.dropna(subset=['coord_datetime'])

# 3.9. GPS coordinates validation (near Tartu, Estonia)
# Tartu approximately: lat ~58.38, lon ~26.72
before_gps_filter = len(locations_df)
locations_df = locations_df[
    (locations_df['latitude'].between(58.0, 59.0)) &
    (locations_df['longitude'].between(26.0, 27.5))
]
print(f"  ✓ Removed {before_gps_filter - len(locations_df)} records with invalid GPS coordinates")

# 3.10. Null latitude/longitude check
locations_df = locations_df.dropna(subset=['latitude', 'longitude'])

# 3.11. Add time features
locations_df['coord_hour'] = locations_df['coord_datetime'].dt.hour
locations_df['coord_minute'] = locations_df['coord_datetime'].dt.minute
locations_df['coord_second'] = locations_df['coord_datetime'].dt.second

print(f"  ✓ Added time features")

# 3.12. Keep only route_codes that exist in routes
valid_route_codes = set(routes_df['route_code'].unique())
before_route_filter = len(locations_df)
locations_df = locations_df[locations_df['route_code'].isin(valid_route_codes)]
print(f"  ✓ Removed {before_route_filter - len(locations_df):,} locations records not found in routes")

# ============================================================================
# 4. CLEANED DATA STATISTICS
# ============================================================================

print("\n[4/5] Cleaned Data Statistics...")
print("-" * 80)

quality_report.append("\n\n" + "=" * 80)
quality_report.append("CLEANING STATISTICS")
quality_report.append("=" * 80)

quality_report.append("\n\nROUTES DATA:")
quality_report.append(f"  Initial Records:          {initial_routes_count:,}")
quality_report.append(f"  Cleaned Records:          {len(routes_df):,}")
quality_report.append(f"  Removed Records:          {initial_routes_count - len(routes_df):,}")
quality_report.append(f"  Data Loss:                {((initial_routes_count - len(routes_df)) / initial_routes_count * 100):.2f}%")

quality_report.append("\n\nLOCATIONS DATA:")
quality_report.append(f"  Initial Records:          {initial_locations_count:,}")
quality_report.append(f"  Cleaned Records:          {len(locations_df):,}")
quality_report.append(f"  Removed Records:          {initial_locations_count - len(locations_df):,}")
quality_report.append(f"  Data Loss:                {((initial_locations_count - len(locations_df)) / initial_locations_count * 100):.2f}%")

# Basic statistics
quality_report.append("\n\n" + "=" * 80)
quality_report.append("ROUTES DATA - CLEANED STATISTICS")
quality_report.append("=" * 80)

quality_report.append(f"\n\nUnique Values:")
quality_report.append(f"  - Unique route_code:        {routes_df['route_code'].nunique():,}")
quality_report.append(f"  - Unique bikes:             {routes_df['cyclenumber'].nunique():,}")
quality_report.append(f"  - Unique start stations:    {routes_df['startstationname'].nunique():,}")
quality_report.append(f"  - Unique end stations:      {routes_df['endstationname'].nunique():,}")
quality_report.append(f"  - Unique membership types:  {routes_df['Membership'].nunique():,}")
quality_report.append(f"  - Unique bike types:        {routes_df['CycleType'].nunique():,}")

quality_report.append(f"\n\nNumerical Values (Summary):")
stats_cols = ['length', 'duration_minutes_calculated', 'DurationMinutes', 'costs']
for col in stats_cols:
    if col in routes_df.columns:
        quality_report.append(f"\n  {col}:")
        quality_report.append(f"    - Mean:     {routes_df[col].mean():.2f}")
        quality_report.append(f"    - Median:   {routes_df[col].median():.2f}")
        quality_report.append(f"    - Min:      {routes_df[col].min():.2f}")
        quality_report.append(f"    - Max:      {routes_df[col].max():.2f}")
        quality_report.append(f"    - Std:      {routes_df[col].std():.2f}")

quality_report.append("\n\n" + "=" * 80)
quality_report.append("LOCATIONS DATA - CLEANED STATISTICS")
quality_report.append("=" * 80)

quality_report.append(f"\n\nUnique Values:")
quality_report.append(f"  - Unique route_code:  {locations_df['route_code'].nunique():,}")
quality_report.append(f"  - Unique bikes:       {locations_df['cyclenumber'].nunique():,}")

quality_report.append(f"\n\nGPS Coordinates (Summary):")
quality_report.append(f"  Latitude:")
quality_report.append(f"    - Mean:     {locations_df['latitude'].mean():.6f}")
quality_report.append(f"    - Min:      {locations_df['latitude'].min():.6f}")
quality_report.append(f"    - Max:      {locations_df['latitude'].max():.6f}")
quality_report.append(f"  Longitude:")
quality_report.append(f"    - Mean:     {locations_df['longitude'].mean():.6f}")
quality_report.append(f"    - Min:      {locations_df['longitude'].min():.6f}")
quality_report.append(f"    - Max:      {locations_df['longitude'].max():.6f}")

# Print to screen
print(f"\nRoutes:")
print(f"  - Initial:  {initial_routes_count:,}")
print(f"  - Cleaned:  {len(routes_df):,}")
print(f"  - Removed:  {initial_routes_count - len(routes_df):,} ({((initial_routes_count - len(routes_df)) / initial_routes_count * 100):.2f}%)")

print(f"\nLocations:")
print(f"  - Initial:  {initial_locations_count:,}")
print(f"  - Cleaned:  {len(locations_df):,}")
print(f"  - Removed:  {initial_locations_count - len(locations_df):,} ({((initial_locations_count - len(locations_df)) / initial_locations_count * 100):.2f}%)")

# ============================================================================
# 5. SAVE DATA
# ============================================================================

print("\n[5/5] Saving Cleaned Data...")
print("-" * 80)

# Save routes
routes_output_path = os.path.join(PROCESSED_DIR, 'routes_cleaned.csv')
routes_df.to_csv(routes_output_path, index=False)
print(f"  ✓ Routes saved: {routes_output_path}")
print(f"    ({len(routes_df):,} records, {len(routes_df.columns)} columns)")

# Save locations
locations_output_path = os.path.join(PROCESSED_DIR, 'locations_cleaned.csv')
locations_df.to_csv(locations_output_path, index=False)
print(f"  ✓ Locations saved: {locations_output_path}")
print(f"    ({len(locations_df):,} records, {len(locations_df.columns)} columns)")

# Save report
report_path = os.path.join(PROCESSED_DIR, 'data_quality_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(quality_report))
print(f"  ✓ Data quality report saved: {report_path}")

# Save column lists
routes_columns_path = os.path.join(PROCESSED_DIR, 'routes_columns.txt')
with open(routes_columns_path, 'w', encoding='utf-8') as f:
    f.write("ROUTES DATA - COLUMN LIST\n")
    f.write("=" * 80 + "\n\n")
    for i, col in enumerate(routes_df.columns, 1):
        f.write(f"{i:2d}. {col:30s} ({routes_df[col].dtype})\n")
print(f"  ✓ Routes column list saved: {routes_columns_path}")

locations_columns_path = os.path.join(PROCESSED_DIR, 'locations_columns.txt')
with open(locations_columns_path, 'w', encoding='utf-8') as f:
    f.write("LOCATIONS DATA - COLUMN LIST\n")
    f.write("=" * 80 + "\n\n")
    for i, col in enumerate(locations_df.columns, 1):
        f.write(f"{i:2d}. {col:30s} ({locations_df[col].dtype})\n")
print(f"  ✓ Locations column list saved: {locations_columns_path}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("DATA PREPROCESSING COMPLETED!")
print("=" * 80)
print("\nOutput Files:")
print(f"  1. {routes_output_path}")
print(f"  2. {locations_output_path}")
print(f"  3. {report_path}")
print(f"  4. {routes_columns_path}")
print(f"  5. {locations_columns_path}")

print("\nNext Steps:")
print("  - Review the data quality report")
print("  - Perform exploratory data analysis (EDA)")
print("  - Create visualizations")
print("  - Conduct statistical analyses")

print("\n" + "=" * 80)
