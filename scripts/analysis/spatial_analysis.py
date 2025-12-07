"""
Spatial Analysis
================

Location-based analysis functions.
"""

import matplotlib.pyplot as plt
from . import config
from .utils import plotting


def analyze_popular_stations(routes):
    """
    Analyze most popular stations.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (top_start, top_end, visualizations, report_lines)
    """
    top_start = routes['startstationname'].value_counts().head(10)
    top_end = routes['endstationname'].value_counts().head(10)

    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    top_start.plot(kind='barh', ax=axes[0], color=config.COLORS['primary'], edgecolor='black')
    axes[0].set_title('Top 10 Start Stations', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Number of Trips')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)

    top_end.plot(kind='barh', ax=axes[1], color=config.COLORS['secondary'], edgecolor='black')
    axes[1].set_title('Top 10 End Stations', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Number of Trips')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'top_stations.png', 'statistical')

    # Report
    report_lines = []
    report_lines.append("**Top 5 Start Stations:**")
    for i, (station, count) in enumerate(top_start.head(5).items(), 1):
        report_lines.append(f"{i}. {station}: {count:,} trips")
    report_lines.append("")
    report_lines.append("**Top 5 End Stations:**")
    for i, (station, count) in enumerate(top_end.head(5).items(), 1):
        report_lines.append(f"{i}. {station}: {count:,} trips")

    return top_start, top_end, [filepath], report_lines


def analyze_trip_types(routes):
    """
    Analyze round trips vs one-way trips.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (round_trip_pct, report_lines)
    """
    routes_copy = routes.copy()
    routes_copy['is_round_trip'] = routes_copy['startstationname'] == routes_copy['endstationname']
    round_trip_pct = (routes_copy['is_round_trip'].sum() / len(routes_copy)) * 100

    report_lines = []
    report_lines.append(f"- **Round trips**: {routes_copy['is_round_trip'].sum():,} ({round_trip_pct:.1f}%)")
    report_lines.append(f"- **One-way trips**: {(~routes_copy['is_round_trip']).sum():,} ({100-round_trip_pct:.1f}%)")

    return round_trip_pct, report_lines


def analyze_popular_routes(routes):
    """
    Analyze most popular routes (OD pairs).

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (top_routes, visualizations, report_lines)
    """
    routes_copy = routes.copy()
    routes_copy['is_round_trip'] = routes_copy['startstationname'] == routes_copy['endstationname']
    routes_copy['od_pair'] = routes_copy['startstationname'] + ' → ' + routes_copy['endstationname']

    top_routes = routes_copy[~routes_copy['is_round_trip']]['od_pair'].value_counts().head(10)

    # Create visualization
    fig = plotting.create_horizontal_bar_chart(
        top_routes,
        'Top 10 Most Popular Routes (One-Way)',
        'Number of Trips'
    )
    filepath = plotting.save_figure(fig, 'top_routes.png', 'statistical')

    # Report
    report_lines = []
    for i, (route, count) in enumerate(top_routes.head(5).items(), 1):
        report_lines.append(f"{i}. {route}: {count} trips")

    return top_routes, [filepath], report_lines


def run_spatial_analysis(routes, report):
    """
    Run all spatial analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Analysis results
    """
    print("\n[Spatial Analysis]")
    print("-" * 80)

    results = {}

    # Popular stations
    print("  • Analyzing popular stations...")
    top_start, top_end, viz_files, report_lines = analyze_popular_stations(routes)
    results['stations'] = {
        'top_start': top_start,
        'top_end': top_end,
        'visualizations': viz_files
    }

    report.add_section("Spatial Analysis")
    report.add_subsection("Most Popular Stations")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Trip types
    print("  • Analyzing trip types...")
    round_trip_pct, report_lines = analyze_trip_types(routes)
    results['trip_types'] = {'round_trip_pct': round_trip_pct}

    report.add_subsection("Trip Types")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Popular routes
    print("  • Analyzing popular routes...")
    top_routes, viz_files, report_lines = analyze_popular_routes(routes)
    results['routes'] = {'top_routes': top_routes, 'visualizations': viz_files}

    report.add_subsection("Most Popular Routes")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    print(f"  ✓ Spatial analysis complete")

    return results
