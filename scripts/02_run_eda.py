"""
Tartu Bike Data - Exploratory Data Analysis Runner
==================================================

Main script to run all EDA analyses.

This is the orchestrator that calls modular analysis functions.
"""

import sys
import warnings
warnings.filterwarnings('ignore')

# Add analysis package to path
from analysis import config
from analysis.data_loader import load_routes_data, load_locations_data, get_data_summary
from analysis.temporal_analysis import run_temporal_analysis
from analysis.spatial_analysis import run_spatial_analysis
from analysis.statistical_analysis import run_statistical_analysis
from analysis.ml_models import run_ml_analysis
from analysis.utils.plotting import setup_plot_style
from analysis.utils.reporting import MarkdownReport

print("=" * 80)
print("TARTU BIKE DATA - EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Setup
print("\n[Setup]")
print("-" * 80)
config.ensure_directories()
setup_plot_style()
print("  ✓ Directories created")
print("  ✓ Plot style configured")

# Load data
print("\n[Data Loading]")
print("-" * 80)

try:
    routes = load_routes_data()
    locations = load_locations_data()
    print(f"  ✓ Routes loaded: {len(routes):,} records")
    print(f"  ✓ Locations loaded: {len(locations):,} GPS points")
except FileNotFoundError as e:
    print(f"  ✗ Error: {e}")
    print("\n  Please run 01_data_preprocessing.py first!")
    sys.exit(1)

# Get summary
summary = get_data_summary(routes, locations)

# Initialize report
report = MarkdownReport("Tartu Bike Data - Exploratory Data Analysis Report")

report.add_section("Dataset Overview")
report.add_stat("Total trips", summary['total_trips'])
report.add_stat("Total GPS points", summary['total_gps_points'])
report.add_line(f"- **Date range**: {summary['date_range'][0]} to {summary['date_range'][1]}")
report.add_stat("Unique bikes", summary['unique_bikes'])
report.add_stat("Unique stations", summary['unique_stations'])
report.add_line("")

# Run analyses
all_results = {}

# Temporal Analysis
temporal_results = run_temporal_analysis(routes, report)
all_results['temporal'] = temporal_results

# Spatial Analysis
spatial_results = run_spatial_analysis(routes, report)
all_results['spatial'] = spatial_results

# Statistical Analysis
statistical_results = run_statistical_analysis(routes, report)
all_results['statistical'] = statistical_results

# Machine Learning Analysis
ml_results = run_ml_analysis(routes, report)
all_results['ml'] = ml_results

# Save report
print("\n[Saving Report]")
print("-" * 80)

import os
report_path = os.path.join(config.REPORTS_DIR, 'eda_report.md')
report.save(report_path)
print(f"  ✓ Report saved: {report_path}")

# Summary
print("\n" + "=" * 80)
print("EXPLORATORY DATA ANALYSIS COMPLETED!")
print("=" * 80)

print("\nKey Findings:")
print(f"  • Peak hour: {temporal_results['hourly']['peak_hour']}:00")
print(f"  • Most popular station: {spatial_results['stations']['top_start'].index[0]}")
print(f"  • Round trip percentage: {spatial_results['trip_types']['round_trip_pct']:.1f}%")
print(f"  • ML models trained: {len(ml_results)} analyses")

print("\nGenerated Files:")
print(f"  • Report: {report_path}")
print(f"  • Visualizations: {config.VIZ_DIR}/")

print("\n" + "=" * 80)
