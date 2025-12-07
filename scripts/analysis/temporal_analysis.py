"""
Temporal Analysis
=================

Time-based analysis functions.
"""

import matplotlib.pyplot as plt
from . import config
from .utils import plotting, reporting


def analyze_hourly_patterns(routes):
    """
    Analyze hourly usage patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (hourly_data, peak_hour, visualizations, report_lines)
    """
    hourly_trips = routes.groupby('unlock_hour').size()

    # Create visualizations
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart
    hourly_trips.plot(kind='bar', ax=axes[0], color=config.COLORS['primary'], edgecolor='black')
    axes[0].set_title('Trips by Hour of Day', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Hour of Day', fontsize=12)
    axes[0].set_ylabel('Number of Trips', fontsize=12)
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
    axes[0].grid(axis='y', alpha=0.3)

    # Line chart
    hourly_trips.plot(kind='line', ax=axes[1], marker='o', linewidth=2,
                      markersize=6, color=config.COLORS['primary'])
    axes[1].set_title('Hourly Trip Trend', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Hour of Day', fontsize=12)
    axes[1].set_ylabel('Number of Trips', fontsize=12)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'hourly_pattern.png', 'time_series')

    # Statistics
    peak_hour = hourly_trips.idxmax()
    peak_trips = hourly_trips.max()
    quietest_hour = hourly_trips.idxmin()
    avg_trips = hourly_trips.mean()

    # Report
    report_lines = []
    report_lines.append(f"- **Peak hour**: {peak_hour}:00 ({peak_trips} trips)")
    report_lines.append(f"- **Quietest hour**: {quietest_hour}:00 ({hourly_trips.min()} trips)")
    report_lines.append(f"- **Average trips/hour**: {avg_trips:.1f}")

    return hourly_trips, peak_hour, [filepath], report_lines


def analyze_daily_patterns(routes):
    """
    Analyze day-of-week patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (daily_data, visualizations, report_lines)
    """
    daily_trips = routes.groupby('unlock_dayofweek').size()
    daily_trips.index = [config.DAY_NAMES[i] for i in daily_trips.index]

    # Create visualization
    fig = plotting.create_bar_chart(
        daily_trips,
        'Trips by Day of Week',
        'Day of Week',
        'Number of Trips',
        color=config.COLORS['secondary']
    )
    plt.xticks(rotation=45)
    filepath = plotting.save_figure(fig, 'daily_pattern.png', 'time_series')

    # Report
    report_lines = []
    report_lines.append(f"- **Busiest day**: {daily_trips.idxmax()} ({daily_trips.max()} trips)")
    report_lines.append(f"- **Quietest day**: {daily_trips.idxmin()} ({daily_trips.min()} trips)")

    return daily_trips, [filepath], report_lines


def analyze_weekend_comparison(routes):
    """
    Compare weekday vs weekend patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (visualizations, report_lines)
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Trip count
    weekend_counts = routes.groupby('is_weekend').size()
    labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_counts.index]
    axes[0].bar(labels, weekend_counts.values,
                color=[config.COLORS['weekday'], config.COLORS['weekend']],
                edgecolor='black')
    axes[0].set_title('Trips: Weekday vs Weekend', fontweight='bold')
    axes[0].set_ylabel('Number of Trips')
    axes[0].grid(axis='y', alpha=0.3)

    # Duration
    weekend_duration = routes.groupby('is_weekend')['duration_minutes_calculated'].mean()
    duration_labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_duration.index]
    axes[1].bar(duration_labels, weekend_duration.values,
                color=[config.COLORS['weekday'], config.COLORS['weekend']],
                edgecolor='black')
    axes[1].set_title('Avg Duration: Weekday vs Weekend', fontweight='bold')
    axes[1].set_ylabel('Average Duration (minutes)')
    axes[1].grid(axis='y', alpha=0.3)

    # Distance
    weekend_distance = routes.groupby('is_weekend')['length'].mean()
    distance_labels = ['Weekday' if idx == 0 else 'Weekend' for idx in weekend_distance.index]
    axes[2].bar(distance_labels, weekend_distance.values,
                color=[config.COLORS['weekday'], config.COLORS['weekend']],
                edgecolor='black')
    axes[2].set_title('Avg Distance: Weekday vs Weekend', fontweight='bold')
    axes[2].set_ylabel('Average Distance (km)')
    axes[2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'weekend_comparison.png', 'time_series')

    # Report
    weekday_count = weekend_counts.iloc[0] if 0 in weekend_counts.index else 0
    weekend_count = weekend_counts.iloc[1] if 1 in weekend_counts.index and len(weekend_counts) > 1 else 0
    weekday_dur = weekend_duration.iloc[0] if 0 in weekend_duration.index else 0
    weekend_dur = weekend_duration.iloc[1] if 1 in weekend_duration.index and len(weekend_duration) > 1 else 0

    report_lines = []
    report_lines.append(f"- **Weekday trips**: {weekday_count:,}")
    report_lines.append(f"- **Weekend trips**: {weekend_count:,}")
    report_lines.append(f"- **Weekday avg duration**: {weekday_dur:.2f} minutes")
    report_lines.append(f"- **Weekend avg duration**: {weekend_dur:.2f} minutes")

    return [filepath], report_lines


def analyze_time_periods(routes):
    """
    Analyze different time periods (Morning/Afternoon/Evening/Night).

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (period_stats, report_lines)
    """
    period_stats = routes.groupby('time_period').agg({
        'route_code': 'count',
        'duration_minutes_calculated': 'mean',
        'length': 'mean'
    }).round(2)
    period_stats.columns = ['Trip Count', 'Avg Duration (min)', 'Avg Distance (km)']

    report_lines = []
    report_lines.append("```")
    report_lines.append(period_stats.to_string())
    report_lines.append("```")

    return period_stats, report_lines


def run_temporal_analysis(routes, report):
    """
    Run all temporal analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Analysis results
    """
    print("\n[Temporal Analysis]")
    print("-" * 80)

    results = {}

    # Hourly patterns
    print("  • Analyzing hourly patterns...")
    hourly_data, peak_hour, viz_files, report_lines = analyze_hourly_patterns(routes)
    results['hourly'] = {'data': hourly_data, 'peak_hour': peak_hour, 'visualizations': viz_files}

    report.add_section("Temporal Analysis")
    report.add_subsection("Hourly Patterns")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Daily patterns
    print("  • Analyzing daily patterns...")
    daily_data, viz_files, report_lines = analyze_daily_patterns(routes)
    results['daily'] = {'data': daily_data, 'visualizations': viz_files}

    report.add_subsection("Day of Week Patterns")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Weekend comparison
    print("  • Comparing weekday vs weekend...")
    viz_files, report_lines = analyze_weekend_comparison(routes)
    results['weekend'] = {'visualizations': viz_files}

    report.add_subsection("Weekend vs Weekday")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Time periods
    print("  • Analyzing time periods...")
    period_stats, report_lines = analyze_time_periods(routes)
    results['periods'] = {'stats': period_stats}

    report.add_subsection("Time Period Analysis")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    print(f"  ✓ Temporal analysis complete")

    return results
