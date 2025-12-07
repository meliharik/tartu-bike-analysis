"""
Configuration and Constants
============================

Central configuration file for all analysis scripts.
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed_data')
VIZ_DIR = os.path.join(BASE_DIR, 'visualizations')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Visualization subdirectories
VIZ_TIME_SERIES = os.path.join(VIZ_DIR, 'time_series')
VIZ_STATISTICAL = os.path.join(VIZ_DIR, 'statistical')
VIZ_DISTRIBUTIONS = os.path.join(VIZ_DIR, 'distributions')
VIZ_MAPS = os.path.join(VIZ_DIR, 'maps')

# Plot settings
PLOT_DPI = 300
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
PLOT_PALETTE = 'husl'

# Color schemes
COLORS = {
    'primary': 'steelblue',
    'secondary': 'coral',
    'tertiary': 'green',
    'quaternary': 'purple',
    'weekday': 'steelblue',
    'weekend': 'coral',
    'bike_colors': ['skyblue', 'lightcoral']
}

# Analysis parameters
PEAK_THRESHOLD = 0.8  # For identifying peak hours
MIN_TRIPS_THRESHOLD = 10  # Minimum trips for station analysis

# Day names
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Time periods
TIME_PERIODS = {
    'Morning': (6, 12),
    'Afternoon': (12, 18),
    'Evening': (18, 22),
    'Night': (22, 6)
}

def ensure_directories():
    """Create all necessary output directories."""
    directories = [
        PROCESSED_DIR,
        VIZ_DIR,
        VIZ_TIME_SERIES,
        VIZ_STATISTICAL,
        VIZ_DISTRIBUTIONS,
        VIZ_MAPS,
        REPORTS_DIR
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
