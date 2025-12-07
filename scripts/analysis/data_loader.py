"""
Data Loading Utilities
=======================

Functions for loading and preprocessing data.
"""

import pandas as pd
import os
from . import config


def load_routes_data():
    """
    Load cleaned routes data.

    Returns:
        pd.DataFrame: Routes dataframe with datetime columns parsed
    """
    file_path = os.path.join(config.PROCESSED_DIR, 'routes_cleaned.csv')

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Routes data not found at {file_path}. "
            "Please run 01_data_preprocessing.py first."
        )

    routes = pd.read_csv(file_path)

    # Parse datetime columns
    routes['unlock_datetime'] = pd.to_datetime(routes['unlock_datetime'])
    routes['lock_datetime'] = pd.to_datetime(routes['lock_datetime'])

    return routes


def load_locations_data():
    """
    Load cleaned locations data.

    Returns:
        pd.DataFrame: Locations dataframe with datetime columns parsed
    """
    file_path = os.path.join(config.PROCESSED_DIR, 'locations_cleaned.csv')

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Locations data not found at {file_path}. "
            "Please run 01_data_preprocessing.py first."
        )

    locations = pd.read_csv(file_path)

    # Parse datetime columns
    locations['coord_datetime'] = pd.to_datetime(locations['coord_datetime'])

    return locations


def get_data_summary(routes, locations):
    """
    Get summary statistics for the datasets.

    Args:
        routes (pd.DataFrame): Routes dataframe
        locations (pd.DataFrame): Locations dataframe

    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_trips': len(routes),
        'total_gps_points': len(locations),
        'date_range': (
            routes['unlock_datetime'].min().date(),
            routes['unlock_datetime'].max().date()
        ),
        'unique_bikes': routes['cyclenumber'].nunique(),
        'unique_stations': routes['startstationname'].nunique(),
        'unique_memberships': routes['Membership'].nunique(),
        'avg_trip_duration': routes['duration_minutes_calculated'].mean(),
        'avg_trip_distance': routes['length'].mean()
    }

    return summary
