"""
Machine Learning Models
=======================

Machine learning models for prediction, clustering, and anomaly detection.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, davies_bouldin_score
from . import config
from .utils import plotting


def predict_hourly_demand(routes):
    """
    Predict hourly bike demand using historical patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (predictions_df, visualization_paths, report_lines)
    """
    # Aggregate hourly demand
    hourly_demand = routes.groupby('unlock_hour').size()

    # Calculate statistics for prediction
    predictions = pd.DataFrame({
        'hour': range(24),
        'historical_mean': [hourly_demand.get(h, 0) for h in range(24)]
    })

    # Simple moving average prediction (3-hour window)
    predictions['predicted_demand'] = predictions['historical_mean'].rolling(
        window=3, center=True, min_periods=1
    ).mean()

    # Calculate confidence intervals (based on std)
    hourly_std = routes.groupby('unlock_hour')['route_code'].count().std()
    predictions['lower_bound'] = predictions['predicted_demand'] - hourly_std
    predictions['upper_bound'] = predictions['predicted_demand'] + hourly_std
    predictions['lower_bound'] = predictions['lower_bound'].clip(lower=0)

    # Visualization
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(predictions['hour'], predictions['historical_mean'],
            marker='o', label='Historical', linewidth=2, markersize=6)
    ax.plot(predictions['hour'], predictions['predicted_demand'],
            marker='s', label='Predicted', linewidth=2, markersize=6, linestyle='--')
    ax.fill_between(predictions['hour'], predictions['lower_bound'],
                     predictions['upper_bound'], alpha=0.2, label='Confidence Interval')

    ax.set_title('Hourly Demand Prediction', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Number of Trips', fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    filepath = plotting.save_figure(fig, 'demand_prediction.png', 'ml')

    # Report
    peak_hour = predictions.loc[predictions['predicted_demand'].idxmax()]
    report_lines = []
    report_lines.append(f"**Predicted Peak Hour**: {int(peak_hour['hour'])}:00")
    report_lines.append(f"**Predicted Peak Demand**: {peak_hour['predicted_demand']:.0f} trips")
    report_lines.append(f"**Average Hourly Demand**: {predictions['predicted_demand'].mean():.0f} trips")

    return predictions, [filepath], report_lines


def cluster_user_behavior(routes, n_clusters=3):
    """
    Cluster users based on behavior patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe
        n_clusters (int): Number of clusters

    Returns:
        tuple: (clustered_users, visualization_paths, report_lines)
    """
    # Aggregate user features
    user_features = routes.groupby('cyclenumber').agg({
        'route_code': 'count',  # Trip frequency
        'duration_minutes_calculated': 'mean',  # Avg duration
        'length': ['mean', 'sum'],  # Avg and total distance
        'unlock_hour': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.mean(),  # Preferred hour
        'is_weekend': 'mean',  # Weekend preference
        'costs': 'sum'  # Total cost
    })

    user_features.columns = ['trip_count', 'avg_duration', 'avg_distance',
                             'total_distance', 'preferred_hour', 'weekend_ratio', 'total_cost']

    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(user_features)

    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    user_features['cluster'] = kmeans.fit_predict(features_scaled)

    # Calculate cluster statistics
    cluster_stats = user_features.groupby('cluster').agg({
        'trip_count': ['count', 'mean'],
        'avg_duration': 'mean',
        'avg_distance': 'mean',
        'preferred_hour': 'mean',
        'weekend_ratio': 'mean'
    }).round(2)

    # Evaluation metrics
    silhouette = silhouette_score(features_scaled, user_features['cluster'])
    davies_bouldin = davies_bouldin_score(features_scaled, user_features['cluster'])

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Cluster sizes
    cluster_counts = user_features['cluster'].value_counts().sort_index()
    axes[0, 0].bar(cluster_counts.index, cluster_counts.values,
                   color=[config.COLORS['primary'], config.COLORS['secondary'], config.COLORS['tertiary']][:n_clusters],
                   edgecolor='black')
    axes[0, 0].set_title('Cluster Sizes', fontweight='bold')
    axes[0, 0].set_xlabel('Cluster')
    axes[0, 0].set_ylabel('Number of Users')
    axes[0, 0].grid(axis='y', alpha=0.3)

    # Trip count vs Duration (colored by cluster)
    for cluster in range(n_clusters):
        cluster_data = user_features[user_features['cluster'] == cluster]
        axes[0, 1].scatter(cluster_data['trip_count'], cluster_data['avg_duration'],
                          label=f'Cluster {cluster}', alpha=0.6, s=50)
    axes[0, 1].set_title('Trip Count vs Avg Duration', fontweight='bold')
    axes[0, 1].set_xlabel('Number of Trips')
    axes[0, 1].set_ylabel('Average Duration (minutes)')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # Distance vs Hour (colored by cluster)
    for cluster in range(n_clusters):
        cluster_data = user_features[user_features['cluster'] == cluster]
        axes[1, 0].scatter(cluster_data['preferred_hour'], cluster_data['avg_distance'],
                          label=f'Cluster {cluster}', alpha=0.6, s=50)
    axes[1, 0].set_title('Preferred Hour vs Avg Distance', fontweight='bold')
    axes[1, 0].set_xlabel('Preferred Hour')
    axes[1, 0].set_ylabel('Average Distance (km)')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)

    # Cluster characteristics heatmap
    cluster_means = user_features.groupby('cluster')[['trip_count', 'avg_duration',
                                                       'avg_distance']].mean()
    cluster_means_norm = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min())

    sns.heatmap(cluster_means_norm.T, annot=True, fmt='.2f', cmap='YlOrRd',
                ax=axes[1, 1], cbar_kws={'label': 'Normalized Value'})
    axes[1, 1].set_title('Cluster Characteristics (Normalized)', fontweight='bold')
    axes[1, 1].set_xlabel('Cluster')
    axes[1, 1].set_ylabel('Feature')

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'user_behavior_clustering.png', 'ml')

    # Report
    report_lines = []
    report_lines.append(f"**Number of Clusters**: {n_clusters}")
    report_lines.append(f"**Silhouette Score**: {silhouette:.3f} (higher is better)")
    report_lines.append(f"**Davies-Bouldin Index**: {davies_bouldin:.3f} (lower is better)")
    report_lines.append("")

    for cluster in range(n_clusters):
        cluster_data = user_features[user_features['cluster'] == cluster]
        report_lines.append(f"**Cluster {cluster}**:")
        report_lines.append(f"- Users: {len(cluster_data)}")
        report_lines.append(f"- Avg trips: {cluster_data['trip_count'].mean():.1f}")
        report_lines.append(f"- Avg duration: {cluster_data['avg_duration'].mean():.1f} min")
        report_lines.append(f"- Avg distance: {cluster_data['avg_distance'].mean():.2f} km")
        report_lines.append("")

    return user_features, [filepath], report_lines


def detect_anomalies(routes, contamination=0.05):
    """
    Detect anomalous trips using Isolation Forest.

    Args:
        routes (pd.DataFrame): Routes dataframe
        contamination (float): Expected proportion of outliers

    Returns:
        tuple: (routes_with_anomalies, visualization_paths, report_lines)
    """
    # Select features for anomaly detection
    features = routes[['duration_minutes_calculated', 'length', 'unlock_hour']].copy()

    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Isolation Forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    routes['anomaly'] = iso_forest.fit_predict(features_scaled)
    routes['anomaly_score'] = iso_forest.score_samples(features_scaled)

    # -1 for anomalies, 1 for normal
    anomalies = routes[routes['anomaly'] == -1]
    normal = routes[routes['anomaly'] == 1]

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Duration vs Distance
    axes[0, 0].scatter(normal['length'], normal['duration_minutes_calculated'],
                      alpha=0.3, s=20, c='blue', label='Normal', edgecolors='none')
    axes[0, 0].scatter(anomalies['length'], anomalies['duration_minutes_calculated'],
                      alpha=0.8, s=50, c='red', label='Anomaly', marker='x')
    axes[0, 0].set_title('Anomaly Detection: Duration vs Distance', fontweight='bold')
    axes[0, 0].set_xlabel('Distance (km)')
    axes[0, 0].set_ylabel('Duration (minutes)')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)

    # Anomaly scores distribution
    axes[0, 1].hist(routes['anomaly_score'], bins=50, edgecolor='black', alpha=0.7)
    axes[0, 1].axvline(routes[routes['anomaly'] == -1]['anomaly_score'].max(),
                      color='red', linestyle='--', linewidth=2, label='Anomaly Threshold')
    axes[0, 1].set_title('Anomaly Score Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Anomaly Score')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # Anomalies by hour
    anomaly_by_hour = routes.groupby('unlock_hour')['anomaly'].apply(lambda x: (x == -1).sum())
    axes[1, 0].bar(anomaly_by_hour.index, anomaly_by_hour.values,
                  color='red', edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Anomalies by Hour', fontweight='bold')
    axes[1, 0].set_xlabel('Hour of Day')
    axes[1, 0].set_ylabel('Number of Anomalies')
    axes[1, 0].grid(axis='y', alpha=0.3)

    # Feature comparison: Normal vs Anomaly
    comparison = pd.DataFrame({
        'Normal Duration': [normal['duration_minutes_calculated'].mean()],
        'Anomaly Duration': [anomalies['duration_minutes_calculated'].mean()],
        'Normal Distance': [normal['length'].mean()],
        'Anomaly Distance': [anomalies['length'].mean()]
    })
    comparison.T.plot(kind='barh', ax=axes[1, 1], legend=False, color=['blue', 'red'])
    axes[1, 1].set_title('Normal vs Anomaly Characteristics', fontweight='bold')
    axes[1, 1].set_xlabel('Average Value')
    axes[1, 1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'anomaly_detection.png', 'ml')

    # Report
    report_lines = []
    report_lines.append(f"**Total Trips**: {len(routes):,}")
    report_lines.append(f"**Anomalies Detected**: {len(anomalies):,} ({len(anomalies)/len(routes)*100:.2f}%)")
    report_lines.append(f"**Normal Trips**: {len(normal):,} ({len(normal)/len(routes)*100:.2f}%)")
    report_lines.append("")
    report_lines.append("**Anomaly Characteristics**:")
    report_lines.append(f"- Avg duration: {anomalies['duration_minutes_calculated'].mean():.1f} min (vs {normal['duration_minutes_calculated'].mean():.1f} normal)")
    report_lines.append(f"- Avg distance: {anomalies['length'].mean():.2f} km (vs {normal['length'].mean():.2f} normal)")
    report_lines.append(f"- Most anomalies at hour: {anomaly_by_hour.idxmax()}:00")

    return routes, [filepath], report_lines


def cluster_routes_spatial(routes, n_clusters=5):
    """
    Cluster routes based on origin-destination patterns.

    Args:
        routes (pd.DataFrame): Routes dataframe
        n_clusters (int): Number of clusters

    Returns:
        tuple: (route_clusters, visualization_paths, report_lines)
    """
    # Create OD pair features
    od_pairs = routes.groupby(['startstationname', 'endstationname']).agg({
        'route_code': 'count',
        'duration_minutes_calculated': 'mean',
        'length': 'mean'
    }).reset_index()
    od_pairs.columns = ['origin', 'destination', 'trip_count', 'avg_duration', 'avg_distance']

    # Filter to significant routes (at least 5 trips)
    od_pairs = od_pairs[od_pairs['trip_count'] >= 5]

    # Prepare features for clustering
    features = od_pairs[['trip_count', 'avg_duration', 'avg_distance']].copy()
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    od_pairs['cluster'] = kmeans.fit_predict(features_scaled)

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Cluster sizes
    cluster_counts = od_pairs['cluster'].value_counts().sort_index()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:n_clusters]
    axes[0, 0].bar(cluster_counts.index, cluster_counts.values,
                   color=colors, edgecolor='black')
    axes[0, 0].set_title('Route Cluster Sizes', fontweight='bold')
    axes[0, 0].set_xlabel('Cluster')
    axes[0, 0].set_ylabel('Number of OD Pairs')
    axes[0, 0].grid(axis='y', alpha=0.3)

    # Trip count vs Distance by cluster
    for cluster in range(n_clusters):
        cluster_data = od_pairs[od_pairs['cluster'] == cluster]
        axes[0, 1].scatter(cluster_data['trip_count'], cluster_data['avg_distance'],
                          label=f'Cluster {cluster}', alpha=0.6, s=50, color=colors[cluster])
    axes[0, 1].set_title('Trip Count vs Distance by Cluster', fontweight='bold')
    axes[0, 1].set_xlabel('Number of Trips')
    axes[0, 1].set_ylabel('Average Distance (km)')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    # Duration vs Distance by cluster
    for cluster in range(n_clusters):
        cluster_data = od_pairs[od_pairs['cluster'] == cluster]
        axes[1, 0].scatter(cluster_data['avg_distance'], cluster_data['avg_duration'],
                          label=f'Cluster {cluster}', alpha=0.6, s=50, color=colors[cluster])
    axes[1, 0].set_title('Distance vs Duration by Cluster', fontweight='bold')
    axes[1, 0].set_xlabel('Average Distance (km)')
    axes[1, 0].set_ylabel('Average Duration (minutes)')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)

    # Top routes per cluster
    top_routes = []
    for cluster in range(min(3, n_clusters)):
        cluster_routes = od_pairs[od_pairs['cluster'] == cluster].nlargest(3, 'trip_count')
        top_routes.extend([f"C{cluster}: {row['origin'][:10]}→{row['destination'][:10]}"
                          for _, row in cluster_routes.iterrows()])

    axes[1, 1].axis('off')
    axes[1, 1].text(0.1, 0.9, 'Top Routes by Cluster', fontsize=12, fontweight='bold',
                   transform=axes[1, 1].transAxes)
    for i, route in enumerate(top_routes[:9]):
        axes[1, 1].text(0.1, 0.8 - i*0.08, route, fontsize=9,
                       transform=axes[1, 1].transAxes)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'route_clustering.png', 'ml')

    # Report
    report_lines = []
    report_lines.append(f"**Number of Clusters**: {n_clusters}")
    report_lines.append(f"**Total OD Pairs Analyzed**: {len(od_pairs)}")
    report_lines.append("")

    for cluster in range(n_clusters):
        cluster_data = od_pairs[od_pairs['cluster'] == cluster]
        report_lines.append(f"**Cluster {cluster}**:")
        report_lines.append(f"- Routes: {len(cluster_data)}")
        report_lines.append(f"- Avg trips/route: {cluster_data['trip_count'].mean():.1f}")
        report_lines.append(f"- Avg distance: {cluster_data['avg_distance'].mean():.2f} km")
        report_lines.append("")

    return od_pairs, [filepath], report_lines


def run_ml_analysis(routes, report):
    """
    Run all machine learning analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: ML results
    """
    print("\n[Machine Learning Analysis]")
    print("-" * 80)

    results = {}

    # Demand prediction
    print("  • Predicting hourly demand...")
    predictions, viz_files, report_lines = predict_hourly_demand(routes)
    results['demand_prediction'] = {'predictions': predictions, 'visualizations': viz_files}

    report.add_section("Machine Learning Analysis")
    report.add_subsection("Demand Prediction")
    for line in report_lines:
        report.add_line(line)
    report.add_line("")

    # User clustering
    print("  • Clustering user behavior...")
    user_clusters, viz_files, report_lines = cluster_user_behavior(routes, n_clusters=3)
    results['user_clustering'] = {'clusters': user_clusters, 'visualizations': viz_files}

    report.add_subsection("User Behavior Clustering")
    for line in report_lines:
        report.add_line(line)

    # Route clustering
    print("  • Clustering routes...")
    route_clusters, viz_files, report_lines = cluster_routes_spatial(routes, n_clusters=5)
    results['route_clustering'] = {'clusters': route_clusters, 'visualizations': viz_files}

    report.add_subsection("Route Clustering")
    for line in report_lines:
        report.add_line(line)

    # Anomaly detection
    print("  • Detecting anomalies...")
    routes_with_anomalies, viz_files, report_lines = detect_anomalies(routes, contamination=0.05)
    results['anomaly_detection'] = {'data': routes_with_anomalies, 'visualizations': viz_files}

    report.add_subsection("Anomaly Detection")
    for line in report_lines:
        report.add_line(line)

    print(f"  ✓ Machine learning analysis complete")

    return results
