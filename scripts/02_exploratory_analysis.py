"""
Tartu Bike Data - Exploratory Data Analysis (EDA)
==================================================

This script performs comprehensive exploratory data analysis on the cleaned
Tartu bike-sharing data, including:
- Temporal analysis (hourly, daily, weekly patterns)
- Spatial analysis (station popularity, route patterns)
- User behavior analysis (membership types, trip characteristics)
- Statistical analysis and correlations
- Data visualizations

Input:
- processed_data/routes_cleaned.csv
- processed_data/locations_cleaned.csv

Output:
- visualizations/ (charts and plots)
- reports/eda_report.md
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for all plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed_data')
VIZ_DIR = os.path.join(BASE_DIR, 'visualizations')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Create output directories
os.makedirs(os.path.join(VIZ_DIR, 'time_series'), exist_ok=True)
os.makedirs(os.path.join(VIZ_DIR, 'statistical'), exist_ok=True)
os.makedirs(os.path.join(VIZ_DIR, 'distributions'), exist_ok=True)
os.makedirs(os.path.join(VIZ_DIR, 'maps'), exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

print("=" * 80)
print("TARTU BIKE DATA - EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Initialize report
report = []
report.append("# Tartu Bike Data - Exploratory Data Analysis Report\n")
report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
report.append("---\n")

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n[1/7] Loading Data...")
print("-" * 80)

routes = pd.read_csv(os.path.join(PROCESSED_DIR, 'routes_cleaned.csv'))
locations = pd.read_csv(os.path.join(PROCESSED_DIR, 'locations_cleaned.csv'))

# Convert datetime columns
routes['unlock_datetime'] = pd.to_datetime(routes['unlock_datetime'])
routes['lock_datetime'] = pd.to_datetime(routes['lock_datetime'])
locations['coord_datetime'] = pd.to_datetime(locations['coord_datetime'])

print(f"✓ Routes loaded: {len(routes):,} records")
print(f"✓ Locations loaded: {len(locations):,} GPS points")

report.append("## 1. Dataset Overview\n")
report.append(f"- **Total trips**: {len(routes):,}\n")
report.append(f"- **Total GPS points**: {len(locations):,}\n")
report.append(f"- **Date range**: {routes['unlock_datetime'].min().date()} to {routes['unlock_datetime'].max().date()}\n")
report.append(f"- **Unique bikes**: {routes['cyclenumber'].nunique()}\n")
report.append(f"- **Unique stations**: {routes['startstationname'].nunique()}\n\n")

# ============================================================================
# 2. TEMPORAL ANALYSIS
# ============================================================================

print("\n[2/7] Temporal Analysis...")
print("-" * 80)

report.append("## 2. Temporal Analysis\n")

# 2.1 Hourly Pattern
hourly_trips = routes.groupby('unlock_hour').size()
print(f"  • Analyzing hourly patterns...")

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
hourly_trips.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title('Trips by Hour of Day', fontsize=14, fontweight='bold')
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)

# Add line plot overlay
plt.subplot(1, 2, 2)
hourly_trips.plot(kind='line', marker='o', linewidth=2, markersize=6, color='steelblue')
plt.title('Hourly Trip Trend', fontsize=14, fontweight='bold')
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'time_series', 'hourly_pattern.png'), dpi=300, bbox_inches='tight')
plt.close()

peak_hour = hourly_trips.idxmax()
peak_trips = hourly_trips.max()
print(f"  ✓ Peak hour: {peak_hour}:00 with {peak_trips} trips")

report.append("### 2.1 Hourly Patterns\n")
report.append(f"- **Peak hour**: {peak_hour}:00 ({peak_trips} trips)\n")
report.append(f"- **Quietest hour**: {hourly_trips.idxmin()}:00 ({hourly_trips.min()} trips)\n")
report.append(f"- **Average trips/hour**: {hourly_trips.mean():.1f}\n\n")

# 2.2 Day of Week Pattern
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_trips = routes.groupby('unlock_dayofweek').size()
daily_trips.index = [day_names[i] for i in daily_trips.index]

print(f"  • Analyzing day-of-week patterns...")

plt.figure(figsize=(12, 6))
daily_trips.plot(kind='bar', color='coral', edgecolor='black')
plt.title('Trips by Day of Week', fontsize=14, fontweight='bold')
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'time_series', 'daily_pattern.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 2.2 Day of Week Patterns\n")
report.append(f"- **Busiest day**: {daily_trips.idxmax()} ({daily_trips.max()} trips)\n")
report.append(f"- **Quietest day**: {daily_trips.idxmin()} ({daily_trips.min()} trips)\n\n")

# 2.3 Weekend vs Weekday
weekend_comparison = routes.groupby('is_weekend').agg({
    'duration_minutes_calculated': ['mean', 'median'],
    'length': ['mean', 'median'],
    'route_code': 'count'
}).round(2)

print(f"  • Comparing weekday vs weekend patterns...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Trip count
weekend_counts = routes.groupby('is_weekend').size()
labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_counts.index]
axes[0].bar(labels, weekend_counts.values, color=['steelblue', 'coral'], edgecolor='black')
axes[0].set_title('Trips: Weekday vs Weekend', fontweight='bold')
axes[0].set_ylabel('Number of Trips')
axes[0].grid(axis='y', alpha=0.3)

# Duration comparison
weekend_duration = routes.groupby('is_weekend')['duration_minutes_calculated'].mean()
duration_labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_duration.index]
axes[1].bar(duration_labels, weekend_duration.values, color=['steelblue', 'coral'], edgecolor='black')
axes[1].set_title('Avg Duration: Weekday vs Weekend', fontweight='bold')
axes[1].set_ylabel('Average Duration (minutes)')
axes[1].grid(axis='y', alpha=0.3)

# Distance comparison
weekend_distance = routes.groupby('is_weekend')['length'].mean()
distance_labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_distance.index]
axes[2].bar(distance_labels, weekend_distance.values, color=['steelblue', 'coral'], edgecolor='black')
axes[2].set_title('Avg Distance: Weekday vs Weekend', fontweight='bold')
axes[2].set_ylabel('Average Distance (km)')
axes[2].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'time_series', 'weekend_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 2.3 Weekend vs Weekday\n")
weekday_count = weekend_counts.iloc[0] if 0 in weekend_counts.index else 0
weekend_count = weekend_counts.iloc[1] if 1 in weekend_counts.index and len(weekend_counts) > 1 else 0
weekday_duration = weekend_duration.iloc[0] if 0 in weekend_duration.index else 0
weekend_duration_val = weekend_duration.iloc[1] if 1 in weekend_duration.index and len(weekend_duration) > 1 else 0
report.append(f"- **Weekday trips**: {weekday_count:,}\n")
report.append(f"- **Weekend trips**: {weekend_count:,}\n")
report.append(f"- **Weekday avg duration**: {weekday_duration:.2f} minutes\n")
report.append(f"- **Weekend avg duration**: {weekend_duration_val:.2f} minutes\n\n")

# 2.4 Time Period Analysis
time_period_stats = routes.groupby('time_period').agg({
    'route_code': 'count',
    'duration_minutes_calculated': 'mean',
    'length': 'mean'
}).round(2)
time_period_stats.columns = ['Trip Count', 'Avg Duration (min)', 'Avg Distance (km)']

print(f"  • Analyzing time periods (Morning/Afternoon/Evening/Night)...")

report.append("### 2.4 Time Period Analysis\n")
report.append("```\n")
report.append(time_period_stats.to_string())
report.append("\n```\n\n")

# ============================================================================
# 3. SPATIAL ANALYSIS
# ============================================================================

print("\n[3/7] Spatial Analysis...")
print("-" * 80)

report.append("## 3. Spatial Analysis\n")

# 3.1 Top Stations
top_start_stations = routes['startstationname'].value_counts().head(10)
top_end_stations = routes['endstationname'].value_counts().head(10)

print(f"  • Identifying popular stations...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

top_start_stations.plot(kind='barh', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title('Top 10 Start Stations', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Number of Trips')
axes[0].invert_yaxis()
axes[0].grid(axis='x', alpha=0.3)

top_end_stations.plot(kind='barh', ax=axes[1], color='coral', edgecolor='black')
axes[1].set_title('Top 10 End Stations', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Number of Trips')
axes[1].invert_yaxis()
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'top_stations.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 3.1 Most Popular Stations\n")
report.append("**Top 5 Start Stations:**\n")
for i, (station, count) in enumerate(top_start_stations.head(5).items(), 1):
    report.append(f"{i}. {station}: {count:,} trips\n")
report.append("\n**Top 5 End Stations:**\n")
for i, (station, count) in enumerate(top_end_stations.head(5).items(), 1):
    report.append(f"{i}. {station}: {count:,} trips\n")
report.append("\n")

# 3.2 Round Trips vs One-Way
routes['is_round_trip'] = routes['startstationname'] == routes['endstationname']
round_trip_pct = (routes['is_round_trip'].sum() / len(routes)) * 100

print(f"  • Round trips: {routes['is_round_trip'].sum():,} ({round_trip_pct:.1f}%)")

report.append("### 3.2 Trip Types\n")
report.append(f"- **Round trips**: {routes['is_round_trip'].sum():,} ({round_trip_pct:.1f}%)\n")
report.append(f"- **One-way trips**: {(~routes['is_round_trip']).sum():,} ({100-round_trip_pct:.1f}%)\n\n")

# 3.3 Popular Routes (Top OD pairs)
routes['od_pair'] = routes['startstationname'] + ' → ' + routes['endstationname']
top_routes = routes[~routes['is_round_trip']]['od_pair'].value_counts().head(10)

print(f"  • Identifying popular routes...")

plt.figure(figsize=(12, 8))
top_routes.plot(kind='barh', color='green', edgecolor='black')
plt.title('Top 10 Most Popular Routes (One-Way)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Trips', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'top_routes.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 3.3 Most Popular Routes\n")
for i, (route, count) in enumerate(top_routes.head(5).items(), 1):
    report.append(f"{i}. {route}: {count} trips\n")
report.append("\n")

# ============================================================================
# 4. USER BEHAVIOR ANALYSIS
# ============================================================================

print("\n[4/7] User Behavior Analysis...")
print("-" * 80)

report.append("## 4. User Behavior Analysis\n")

# 4.1 Membership Types
membership_stats = routes.groupby('Membership').agg({
    'route_code': 'count',
    'duration_minutes_calculated': 'mean',
    'length': 'mean',
    'costs': 'mean'
}).round(2)
membership_stats.columns = ['Trip Count', 'Avg Duration (min)', 'Avg Distance (km)', 'Avg Cost (€)']
membership_stats = membership_stats.sort_values('Trip Count', ascending=False)

print(f"  • Analyzing {routes['Membership'].nunique()} membership types...")

# Plot top membership types
plt.figure(figsize=(14, 6))
top_memberships = routes['Membership'].value_counts().head(8)
top_memberships.plot(kind='bar', color='purple', edgecolor='black')
plt.title('Trips by Membership Type (Top 8)', fontsize=14, fontweight='bold')
plt.xlabel('Membership Type', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'membership_types.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 4.1 Membership Analysis\n")
report.append("**Top 5 Membership Types:**\n")
for i, (membership, count) in enumerate(membership_stats.head(5)['Trip Count'].items(), 1):
    report.append(f"{i}. {membership}: {int(count):,} trips\n")
report.append("\n")

# 4.2 Bike Type Comparison
bike_type_stats = routes.groupby('CycleType').agg({
    'route_code': 'count',
    'duration_minutes_calculated': 'mean',
    'length': 'mean'
}).round(2)

print(f"  • Comparing bike types...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Trip count by bike type
bike_counts = routes['CycleType'].value_counts()
axes[0].pie(bike_counts.values, labels=bike_counts.index, autopct='%1.1f%%',
            startangle=90, colors=['skyblue', 'lightcoral'])
axes[0].set_title('Trips by Bike Type', fontweight='bold')

# Duration comparison
bike_duration = routes.groupby('CycleType')['duration_minutes_calculated'].mean()
axes[1].bar(bike_duration.index, bike_duration.values, color=['skyblue', 'lightcoral'], edgecolor='black')
axes[1].set_title('Avg Duration by Bike Type', fontweight='bold')
axes[1].set_ylabel('Minutes')
axes[1].grid(axis='y', alpha=0.3)

# Distance comparison
bike_distance = routes.groupby('CycleType')['length'].mean()
axes[2].bar(bike_distance.index, bike_distance.values, color=['skyblue', 'lightcoral'], edgecolor='black')
axes[2].set_title('Avg Distance by Bike Type', fontweight='bold')
axes[2].set_ylabel('Kilometers')
axes[2].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'bike_type_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 4.2 Bike Type Analysis\n")
for bike_type, stats in bike_type_stats.iterrows():
    report.append(f"**{bike_type}:**\n")
    report.append(f"- Trips: {int(stats['route_code']):,}\n")
    report.append(f"- Avg Duration: {stats['duration_minutes_calculated']:.2f} min\n")
    report.append(f"- Avg Distance: {stats['length']:.2f} km\n\n")

# ============================================================================
# 5. TRIP CHARACTERISTICS
# ============================================================================

print("\n[5/7] Analyzing Trip Characteristics...")
print("-" * 80)

report.append("## 5. Trip Characteristics\n")

# 5.1 Duration Distribution
print(f"  • Analyzing duration distribution...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Duration histogram
axes[0, 0].hist(routes['duration_minutes_calculated'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Trip Duration Distribution', fontweight='bold')
axes[0, 0].set_xlabel('Duration (minutes)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].axvline(routes['duration_minutes_calculated'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
axes[0, 0].axvline(routes['duration_minutes_calculated'].median(), color='green', linestyle='--', linewidth=2, label='Median')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Duration boxplot
axes[0, 1].boxplot(routes['duration_minutes_calculated'], vert=True)
axes[0, 1].set_title('Duration Boxplot', fontweight='bold')
axes[0, 1].set_ylabel('Duration (minutes)')
axes[0, 1].grid(alpha=0.3)

# Distance histogram
axes[1, 0].hist(routes['length'], bins=50, color='coral', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Trip Distance Distribution', fontweight='bold')
axes[1, 0].set_xlabel('Distance (km)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].axvline(routes['length'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
axes[1, 0].axvline(routes['length'].median(), color='green', linestyle='--', linewidth=2, label='Median')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Distance boxplot
axes[1, 1].boxplot(routes['length'], vert=True)
axes[1, 1].set_title('Distance Boxplot', fontweight='bold')
axes[1, 1].set_ylabel('Distance (km)')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'distributions', 'trip_distributions.png'), dpi=300, bbox_inches='tight')
plt.close()

# Statistics
duration_stats = routes['duration_minutes_calculated'].describe()
distance_stats = routes['length'].describe()

report.append("### 5.1 Duration Statistics\n")
report.append(f"- Mean: {duration_stats['mean']:.2f} minutes\n")
report.append(f"- Median: {duration_stats['50%']:.2f} minutes\n")
report.append(f"- Std Dev: {duration_stats['std']:.2f} minutes\n")
report.append(f"- Min: {duration_stats['min']:.2f} minutes\n")
report.append(f"- Max: {duration_stats['max']:.2f} minutes\n\n")

report.append("### 5.2 Distance Statistics\n")
report.append(f"- Mean: {distance_stats['mean']:.2f} km\n")
report.append(f"- Median: {distance_stats['50%']:.2f} km\n")
report.append(f"- Std Dev: {distance_stats['std']:.2f} km\n")
report.append(f"- Min: {distance_stats['min']:.2f} km\n")
report.append(f"- Max: {distance_stats['max']:.2f} km\n\n")

# 5.2 Duration vs Distance Scatter
print(f"  • Creating duration vs distance plot...")

plt.figure(figsize=(10, 8))
plt.scatter(routes['length'], routes['duration_minutes_calculated'],
            alpha=0.3, s=20, c='steelblue', edgecolors='none')
plt.title('Trip Duration vs Distance', fontsize=14, fontweight='bold')
plt.xlabel('Distance (km)', fontsize=12)
plt.ylabel('Duration (minutes)', fontsize=12)
plt.grid(alpha=0.3)

# Add correlation
correlation = routes['length'].corr(routes['duration_minutes_calculated'])
plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}',
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'distributions', 'duration_vs_distance.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append(f"### 5.3 Duration vs Distance Correlation\n")
report.append(f"- **Correlation coefficient**: {correlation:.3f}\n\n")

# ============================================================================
# 6. STATISTICAL ANALYSIS
# ============================================================================

print("\n[6/7] Statistical Analysis...")
print("-" * 80)

report.append("## 6. Statistical Analysis\n")

# 6.1 Correlation Matrix
print(f"  • Computing correlation matrix...")

numeric_cols = ['duration_minutes_calculated', 'length', 'costs', 'unlock_hour', 'is_weekend']
correlation_matrix = routes[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'correlation_matrix.png'), dpi=300, bbox_inches='tight')
plt.close()

report.append("### 6.1 Correlation Matrix\n")
report.append("Key correlations:\n")
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_val = correlation_matrix.iloc[i, j]
        if abs(corr_val) > 0.1:  # Only report notable correlations
            report.append(f"- {correlation_matrix.columns[i]} vs {correlation_matrix.columns[j]}: {corr_val:.3f}\n")
report.append("\n")

# 6.2 Cost Analysis
cost_distribution = routes['costs'].value_counts().sort_index()

print(f"  • Analyzing cost distribution...")

plt.figure(figsize=(10, 6))
cost_distribution.plot(kind='bar', color='green', edgecolor='black')
plt.title('Trip Cost Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Cost (€)', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'statistical', 'cost_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()

free_trips_pct = (routes['costs'] == 0).sum() / len(routes) * 100
report.append("### 6.2 Cost Analysis\n")
report.append(f"- **Free trips**: {(routes['costs'] == 0).sum():,} ({free_trips_pct:.1f}%)\n")
report.append(f"- **Paid trips**: {(routes['costs'] > 0).sum():,} ({100-free_trips_pct:.1f}%)\n")
report.append(f"- **Average cost (all)**: €{routes['costs'].mean():.2f}\n")
report.append(f"- **Average cost (paid only)**: €{routes[routes['costs'] > 0]['costs'].mean():.2f}\n\n")

# ============================================================================
# 7. GPS DATA ANALYSIS
# ============================================================================

print("\n[7/7] GPS Data Analysis...")
print("-" * 80)

report.append("## 7. GPS Data Analysis\n")

# Calculate average GPS points per trip
gps_per_trip = locations.groupby('route_code').size()
avg_gps_points = gps_per_trip.mean()
median_gps_points = gps_per_trip.median()

print(f"  • GPS points per trip - Mean: {avg_gps_points:.1f}, Median: {median_gps_points:.1f}")

# Geographic boundaries
lat_range = locations['latitude'].max() - locations['latitude'].min()
lon_range = locations['longitude'].max() - locations['longitude'].min()

print(f"  • Geographic coverage - Lat: {lat_range:.4f}°, Lon: {lon_range:.4f}°")

report.append(f"- **Average GPS points per trip**: {avg_gps_points:.1f}\n")
report.append(f"- **Median GPS points per trip**: {median_gps_points:.1f}\n")
report.append(f"- **Latitude range**: {locations['latitude'].min():.6f}° to {locations['latitude'].max():.6f}°\n")
report.append(f"- **Longitude range**: {locations['longitude'].min():.6f}° to {locations['longitude'].max():.6f}°\n")
report.append(f"- **Coverage area**: ~{lat_range:.4f}° × {lon_range:.4f}°\n\n")

# GPS density heatmap
print(f"  • Creating GPS density heatmap...")

plt.figure(figsize=(12, 10))
plt.hexbin(locations['longitude'], locations['latitude'], gridsize=50, cmap='YlOrRd', mincnt=1)
plt.colorbar(label='GPS Point Density')
plt.title('GPS Point Density Heatmap - Tartu Area', fontsize=14, fontweight='bold')
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, 'maps', 'gps_density_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 8. SAVE REPORT
# ============================================================================

print("\n[8/8] Saving Analysis Report...")
print("-" * 80)

# Add summary statistics
report.append("## 8. Summary Statistics\n")
report.append("```\n")
report.append(routes[['duration_minutes_calculated', 'length', 'costs']].describe().to_string())
report.append("\n```\n\n")

# Save report
report_path = os.path.join(REPORTS_DIR, 'eda_report.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"✓ Report saved: {report_path}")

# Summary
print("\n" + "=" * 80)
print("EXPLORATORY DATA ANALYSIS COMPLETED!")
print("=" * 80)
print("\nGenerated Visualizations:")
print(f"  • Time Series: {len(os.listdir(os.path.join(VIZ_DIR, 'time_series')))} charts")
print(f"  • Statistical: {len(os.listdir(os.path.join(VIZ_DIR, 'statistical')))} charts")
print(f"  • Distributions: {len(os.listdir(os.path.join(VIZ_DIR, 'distributions')))} charts")
print(f"  • Maps: {len(os.listdir(os.path.join(VIZ_DIR, 'maps')))} charts")

print("\nKey Findings:")
print(f"  • Peak hour: {peak_hour}:00 ({peak_trips} trips)")
print(f"  • Most popular station: {top_start_stations.index[0]} ({top_start_stations.iloc[0]} trips)")
print(f"  • Round trip percentage: {round_trip_pct:.1f}%")
print(f"  • Free trips: {free_trips_pct:.1f}%")
print(f"  • Duration-Distance correlation: {correlation:.3f}")

print("\nOutput Files:")
print(f"  • Report: {report_path}")
print(f"  • Visualizations: {VIZ_DIR}/")

print("\n" + "=" * 80)
