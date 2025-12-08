"""
Statistical Analysis
====================

Advanced statistical testing and analysis functions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from . import config
from .utils import plotting


def test_weekend_vs_weekday(routes):
    """
    Test if there are significant differences between weekend and weekday trips.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        dict: Test results and statistics
    """
    weekday_trips = routes[routes['is_weekend'] == 0]
    weekend_trips = routes[routes['is_weekend'] == 1]

    results = {}

    # Duration comparison
    if len(weekend_trips) > 0:
        duration_ttest = stats.ttest_ind(
            weekday_trips['duration_minutes_calculated'],
            weekend_trips['duration_minutes_calculated']
        )
        results['duration'] = {
            'statistic': duration_ttest.statistic,
            'pvalue': duration_ttest.pvalue,
            'weekday_mean': weekday_trips['duration_minutes_calculated'].mean(),
            'weekend_mean': weekend_trips['duration_minutes_calculated'].mean(),
            'significant': duration_ttest.pvalue < 0.05
        }

        # Distance comparison
        distance_ttest = stats.ttest_ind(
            weekday_trips['length'],
            weekend_trips['length']
        )
        results['distance'] = {
            'statistic': distance_ttest.statistic,
            'pvalue': distance_ttest.pvalue,
            'weekday_mean': weekday_trips['length'].mean(),
            'weekend_mean': weekend_trips['length'].mean(),
            'significant': distance_ttest.pvalue < 0.05
        }
    else:
        results['note'] = 'No weekend data available for comparison'

    return results


def test_bike_type_differences(routes):
    """
    Test if there are significant differences between bike types.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        dict: Test results
    """
    bike_types = routes['CycleType'].unique()

    if len(bike_types) < 2:
        return {'note': 'Only one bike type available'}

    type1 = routes[routes['CycleType'] == bike_types[0]]
    type2 = routes[routes['CycleType'] == bike_types[1]]

    # Duration comparison
    duration_ttest = stats.ttest_ind(
        type1['duration_minutes_calculated'],
        type2['duration_minutes_calculated']
    )

    # Distance comparison
    distance_ttest = stats.ttest_ind(
        type1['length'],
        type2['length']
    )

    results = {
        'bike_types': list(bike_types),
        'duration': {
            'statistic': duration_ttest.statistic,
            'pvalue': duration_ttest.pvalue,
            'type1_mean': type1['duration_minutes_calculated'].mean(),
            'type2_mean': type2['duration_minutes_calculated'].mean(),
            'significant': duration_ttest.pvalue < 0.05
        },
        'distance': {
            'statistic': distance_ttest.statistic,
            'pvalue': distance_ttest.pvalue,
            'type1_mean': type1['length'].mean(),
            'type2_mean': type2['length'].mean(),
            'significant': distance_ttest.pvalue < 0.05
        }
    }

    return results


def test_time_period_differences(routes):
    """
    Test if there are significant differences across time periods using ANOVA.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        dict: ANOVA results
    """
    time_periods = routes['time_period'].unique()
    period_groups = [routes[routes['time_period'] == period]['duration_minutes_calculated']
                     for period in time_periods]

    # ANOVA for duration
    duration_anova = stats.f_oneway(*period_groups)

    # ANOVA for distance
    distance_groups = [routes[routes['time_period'] == period]['length']
                       for period in time_periods]
    distance_anova = stats.f_oneway(*distance_groups)

    results = {
        'time_periods': list(time_periods),
        'duration_anova': {
            'statistic': duration_anova.statistic,
            'pvalue': duration_anova.pvalue,
            'significant': duration_anova.pvalue < 0.05
        },
        'distance_anova': {
            'statistic': distance_anova.statistic,
            'pvalue': distance_anova.pvalue,
            'significant': distance_anova.pvalue < 0.05
        }
    }

    return results


def analyze_user_segments(routes):
    """
    Segment users based on behavior patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (segments_df, visualization_paths, report_lines)
    """
    # Aggregate by user (using cyclenumber as proxy)
    user_stats = routes.groupby('cyclenumber').agg({
        'route_code': 'count',  # Frequency
        'duration_minutes_calculated': 'mean',
        'length': ['mean', 'sum'],
        'costs': 'sum'
    }).round(2)

    user_stats.columns = ['trip_count', 'avg_duration', 'avg_distance', 'total_distance', 'total_cost']

    # Segment by trip frequency
    user_stats['segment'] = pd.cut(
        user_stats['trip_count'],
        bins=[0, 5, 15, float('inf')],
        labels=['Occasional', 'Regular', 'Heavy']
    )

    # Segment statistics
    segment_summary = user_stats.groupby('segment').agg({
        'trip_count': ['count', 'mean'],
        'avg_duration': 'mean',
        'avg_distance': 'mean',
        'total_distance': 'mean'
    }).round(2)

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Trip count distribution by segment
    user_stats['segment'].value_counts().plot(
        kind='bar', ax=axes[0, 0], color=config.COLORS['primary'], edgecolor='black'
    )
    axes[0, 0].set_title('User Distribution by Segment', fontweight='bold')
    axes[0, 0].set_ylabel('Number of Users')
    axes[0, 0].set_xlabel('Segment')
    axes[0, 0].grid(axis='y', alpha=0.3)

    # Average trips per segment
    segment_trips = user_stats.groupby('segment')['trip_count'].mean()
    segment_trips.plot(
        kind='bar', ax=axes[0, 1], color=config.COLORS['secondary'], edgecolor='black'
    )
    axes[0, 1].set_title('Average Trips per User by Segment', fontweight='bold')
    axes[0, 1].set_ylabel('Average Number of Trips')
    axes[0, 1].set_xlabel('Segment')
    axes[0, 1].grid(axis='y', alpha=0.3)

    # Box plot: Duration by segment
    user_stats.boxplot(column='avg_duration', by='segment', ax=axes[1, 0])
    axes[1, 0].set_title('Trip Duration by User Segment', fontweight='bold')
    axes[1, 0].set_ylabel('Average Duration (minutes)')
    axes[1, 0].set_xlabel('Segment')
    plt.sca(axes[1, 0])
    plt.xticks(rotation=0)

    # Box plot: Distance by segment
    user_stats.boxplot(column='avg_distance', by='segment', ax=axes[1, 1])
    axes[1, 1].set_title('Trip Distance by User Segment', fontweight='bold')
    axes[1, 1].set_ylabel('Average Distance (km)')
    axes[1, 1].set_xlabel('Segment')
    plt.sca(axes[1, 1])
    plt.xticks(rotation=0)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'user_segmentation.png', 'statistical')

    # Report
    report_lines = []
    report_lines.append(f"**Total Users Analyzed**: {len(user_stats):,}")
    report_lines.append("")
    report_lines.append("**Segment Distribution**:")
    for segment, count in user_stats['segment'].value_counts().items():
        pct = (count / len(user_stats)) * 100
        report_lines.append(f"- {segment}: {count:,} users ({pct:.1f}%)")

    return user_stats, [filepath], report_lines


def create_distribution_comparison(routes):
    """
    Create violin plots comparing distributions across categories.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        list: Visualization file paths
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Duration by time period
    sns.violinplot(data=routes, x='time_period', y='duration_minutes_calculated',
                   ax=axes[0, 0], palette='Set2')
    axes[0, 0].set_title('Trip Duration Distribution by Time Period', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylabel('Duration (minutes)')
    axes[0, 0].set_xlabel('Time Period')
    axes[0, 0].set_ylim(0, routes['duration_minutes_calculated'].quantile(0.95))

    # Distance by time period
    sns.violinplot(data=routes, x='time_period', y='length',
                   ax=axes[0, 1], palette='Set2')
    axes[0, 1].set_title('Trip Distance Distribution by Time Period', fontweight='bold', fontsize=12)
    axes[0, 1].set_ylabel('Distance (km)')
    axes[0, 1].set_xlabel('Time Period')
    axes[0, 1].set_ylim(0, routes['length'].quantile(0.95))

    # Duration by bike type
    sns.violinplot(data=routes, x='CycleType', y='duration_minutes_calculated',
                   ax=axes[1, 0], palette='Set1')
    axes[1, 0].set_title('Trip Duration Distribution by Bike Type', fontweight='bold', fontsize=12)
    axes[1, 0].set_ylabel('Duration (minutes)')
    axes[1, 0].set_xlabel('Bike Type')
    axes[1, 0].set_ylim(0, routes['duration_minutes_calculated'].quantile(0.95))

    # Distance by bike type
    sns.violinplot(data=routes, x='CycleType', y='length',
                   ax=axes[1, 1], palette='Set1')
    axes[1, 1].set_title('Trip Distance Distribution by Bike Type', fontweight='bold', fontsize=12)
    axes[1, 1].set_ylabel('Distance (km)')
    axes[1, 1].set_xlabel('Bike Type')
    axes[1, 1].set_ylim(0, routes['length'].quantile(0.95))

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'distribution_comparisons.png', 'statistical')

    return [filepath]


def run_statistical_analysis(routes, report):
    """
    Run all statistical analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Analysis results
    """
    print("\n[Statistical Analysis]")
    print("-" * 80)

    results = {}

    # Hypothesis tests
    print("  • Testing weekend vs weekday differences...")
    weekend_results = test_weekend_vs_weekday(routes)
    results['weekend_test'] = weekend_results

    report.add_section("Statistical Analysis")
    report.add_subsection("Weekend vs Weekday Comparison")

    if 'note' in weekend_results:
        report.add_line(f"Note: {weekend_results['note']}")
    else:
        report.add_line("**Duration:**")
        report.add_line(f"- Weekday mean: {weekend_results['duration']['weekday_mean']:.2f} minutes")
        report.add_line(f"- Weekend mean: {weekend_results['duration']['weekend_mean']:.2f} minutes")
        report.add_line(f"- p-value: {weekend_results['duration']['pvalue']:.4f}")
        report.add_line(f"- Significant difference: {'Yes' if weekend_results['duration']['significant'] else 'No'}")
        report.add_line("")

        report.add_line("**Distance:**")
        report.add_line(f"- Weekday mean: {weekend_results['distance']['weekday_mean']:.2f} km")
        report.add_line(f"- Weekend mean: {weekend_results['distance']['weekend_mean']:.2f} km")
        report.add_line(f"- p-value: {weekend_results['distance']['pvalue']:.4f}")
        report.add_line(f"- Significant difference: {'Yes' if weekend_results['distance']['significant'] else 'No'}")
    report.add_line("")

    print("  • Testing bike type differences...")
    bike_results = test_bike_type_differences(routes)
    results['bike_type_test'] = bike_results

    report.add_subsection("Bike Type Comparison")
    if 'note' in bike_results:
        report.add_line(f"Note: {bike_results['note']}")
    else:
        report.add_line(f"**Comparing**: {bike_results['bike_types'][0]} vs {bike_results['bike_types'][1]}")
        report.add_line("")
        report.add_line("**Duration:**")
        report.add_line(f"- {bike_results['bike_types'][0]} mean: {bike_results['duration']['type1_mean']:.2f} minutes")
        report.add_line(f"- {bike_results['bike_types'][1]} mean: {bike_results['duration']['type2_mean']:.2f} minutes")
        report.add_line(f"- p-value: {bike_results['duration']['pvalue']:.4f}")
        report.add_line(f"- Significant difference: {'Yes' if bike_results['duration']['significant'] else 'No'}")
        report.add_line("")

        report.add_line("**Distance:**")
        report.add_line(f"- {bike_results['bike_types'][0]} mean: {bike_results['distance']['type1_mean']:.2f} km")
        report.add_line(f"- {bike_results['bike_types'][1]} mean: {bike_results['distance']['type2_mean']:.2f} km")
        report.add_line(f"- p-value: {bike_results['distance']['pvalue']:.4f}")
        report.add_line(f"- Significant difference: {'Yes' if bike_results['distance']['significant'] else 'No'}")
    report.add_line("")

    print("  • Testing time period differences...")
    time_results = test_time_period_differences(routes)
    results['time_period_test'] = time_results

    report.add_subsection("Time Period Comparison (ANOVA)")
    report.add_line(f"**Time Periods Tested**: {', '.join(time_results['time_periods'])}")
    report.add_line("")
    report.add_line("**Duration ANOVA:**")
    report.add_line(f"- F-statistic: {time_results['duration_anova']['statistic']:.2f}")
    report.add_line(f"- p-value: {time_results['duration_anova']['pvalue']:.4f}")
    report.add_line(f"- Significant difference: {'Yes' if time_results['duration_anova']['significant'] else 'No'}")
    report.add_line("")

    report.add_line("**Distance ANOVA:**")
    report.add_line(f"- F-statistic: {time_results['distance_anova']['statistic']:.2f}")
    report.add_line(f"- p-value: {time_results['distance_anova']['pvalue']:.4f}")
    report.add_line(f"- Significant difference: {'Yes' if time_results['distance_anova']['significant'] else 'No'}")
    report.add_line("")

    # User segmentation
    print("  • Analyzing user segments...")
    segments, viz_files, report_lines = analyze_user_segments(routes)
    results['user_segments'] = {'data': segments, 'visualizations': viz_files}

    report.add_subsection("User Segmentation Analysis")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # Distribution comparisons
    print("  • Creating distribution comparisons...")
    viz_files = create_distribution_comparison(routes)
    results['distributions'] = {'visualizations': viz_files}

    print(f"  ✓ Statistical analysis complete")

    return results
