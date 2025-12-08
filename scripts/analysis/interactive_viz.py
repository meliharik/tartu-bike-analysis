"""
Interactive Visualizations
===========================

Interactive maps and visualizations using Folium and Plotly.
"""

import pandas as pd
import numpy as np
import folium
from folium import plugins
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from . import config


def create_station_map(routes, locations):
    """
    Create an interactive map showing all bike stations.

    Args:
        routes (pd.DataFrame): Routes dataframe
        locations (pd.DataFrame): Locations dataframe with GPS coordinates

    Returns:
        tuple: (folium.Map, filepath, report_lines)
    """
    # Get station trip counts
    start_counts = routes['startstationname'].value_counts()
    end_counts = routes['endstationname'].value_counts()

    # Merge to get total trips per station
    station_trips = pd.DataFrame({
        'start_trips': start_counts,
        'end_trips': end_counts
    }).fillna(0)
    station_trips['total_trips'] = station_trips['start_trips'] + station_trips['end_trips']
    station_trips = station_trips.reset_index()
    station_trips.columns = ['station', 'start_trips', 'end_trips', 'total_trips']

    # Get first/last GPS coordinates for each route to approximate station locations
    route_coords = locations.groupby('route_code').agg({
        'latitude': ['first', 'last'],
        'longitude': ['first', 'last']
    }).reset_index()
    route_coords.columns = ['route_code', 'start_lat', 'end_lat', 'start_lon', 'end_lon']

    # Merge with routes
    routes_with_coords = routes.merge(route_coords, on='route_code', how='left')

    # Get average coordinates for each station
    start_stations = routes_with_coords.groupby('startstationname').agg({
        'start_lat': 'mean',
        'start_lon': 'mean'
    }).reset_index()
    start_stations.columns = ['station', 'lat', 'lon']

    # Merge with trip counts
    station_stats = start_stations.merge(station_trips, on='station', how='inner')

    # Remove stations with invalid coordinates
    station_stats = station_stats[
        (station_stats['lat'] > 0) &
        (station_stats['lon'] > 0) &
        (station_stats['lat'] < 90) &
        (station_stats['lon'] < 180)
    ]

    # Create base map centered on Tartu
    center_lat = station_stats['lat'].mean()
    center_lon = station_stats['lon'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )

    # Add station markers with popup info
    for _, row in station_stats.iterrows():
        # Size marker based on trip count
        radius = np.log1p(row['total_trips']) * 2

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            popup=f"<b>{row['station']}</b><br>Total Trips: {int(row['total_trips']):,}<br>Starts: {int(row['start_trips']):,}<br>Ends: {int(row['end_trips']):,}",
            tooltip=row['station'],
            color='blue',
            fill=True,
            fillColor='lightblue',
            fillOpacity=0.6
        ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save map
    filepath = os.path.join(config.VIZ_DIR, 'interactive_station_map.html')
    m.save(filepath)

    report_lines = [
        f"**Total Stations Mapped**: {len(station_stats)}",
        f"**Map Center**: ({center_lat:.4f}, {center_lon:.4f})",
        f"**Total Trips Visualized**: {int(station_stats['total_trips'].sum()):,}",
        ""
    ]

    return m, filepath, report_lines


def create_trip_flow_map(routes, locations, top_n=20):
    """
    Create an interactive map showing trip flows between stations.

    Args:
        routes (pd.DataFrame): Routes dataframe
        locations (pd.DataFrame): Locations dataframe
        top_n (int): Number of top routes to show

    Returns:
        tuple: (folium.Map, filepath, report_lines)
    """
    # Get route coordinates
    route_coords = locations.groupby('route_code').agg({
        'latitude': ['first', 'last'],
        'longitude': ['first', 'last']
    }).reset_index()
    route_coords.columns = ['route_code', 'start_lat', 'end_lat', 'start_lon', 'end_lon']

    # Merge with routes
    routes_with_coords = routes.merge(route_coords, on='route_code', how='left')

    # Get top routes by OD pair
    route_counts = routes_with_coords.groupby([
        'startstationname', 'start_lat', 'start_lon',
        'endstationname', 'end_lat', 'end_lon'
    ]).size().reset_index(name='count')

    # Filter valid coordinates
    route_counts = route_counts[
        (route_counts['start_lat'] > 0) &
        (route_counts['start_lon'] > 0) &
        (route_counts['end_lat'] > 0) &
        (route_counts['end_lon'] > 0) &
        (route_counts['start_lat'] < 90) &
        (route_counts['end_lat'] < 90)
    ]

    # Get top routes
    top_routes = route_counts.nlargest(top_n, 'count')

    # Create base map
    center_lat = top_routes['start_lat'].mean()
    center_lon = top_routes['start_lon'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='CartoDB positron'
    )

    # Add flow lines
    for _, row in top_routes.iterrows():
        # Line thickness based on trip count
        weight = np.log1p(row['count']) * 1.5

        # Create line
        folium.PolyLine(
            locations=[
                [row['start_lat'], row['start_lon']],
                [row['end_lat'], row['end_lon']]
            ],
            color='red',
            weight=weight,
            opacity=0.6,
            popup=f"{row['startstationname']} → {row['endstationname']}<br>Trips: {row['count']:,}",
            tooltip=f"{row['count']:,} trips"
        ).add_to(m)

        # Add arrow marker at end
        folium.CircleMarker(
            location=[row['end_lat'], row['end_lon']],
            radius=3,
            color='red',
            fill=True,
            fillColor='red'
        ).add_to(m)

    # Save map
    filepath = os.path.join(config.VIZ_DIR, 'interactive_trip_flow.html')
    m.save(filepath)

    report_lines = [
        f"**Top Routes Visualized**: {top_n}",
        f"**Most Popular Route**: {top_routes.iloc[0]['startstationname']} → {top_routes.iloc[0]['endstationname']}",
        f"**Most Popular Route Trips**: {top_routes.iloc[0]['count']:,}",
        ""
    ]

    return m, filepath, report_lines


def create_heatmap_animation(locations):
    """
    Create an animated heatmap of GPS points over time.

    Args:
        locations (pd.DataFrame): Locations dataframe

    Returns:
        tuple: (folium.Map, filepath, report_lines)
    """
    # Sample data for performance (use every 100th point)
    sample_locations = locations.iloc[::100].copy()

    # Filter valid coordinates
    sample_locations = sample_locations[
        (sample_locations['latitude'] > 0) &
        (sample_locations['longitude'] > 0)
    ]

    # Create base map
    center_lat = sample_locations['latitude'].mean()
    center_lon = sample_locations['longitude'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )

    # Prepare data for heatmap
    heat_data = sample_locations[['latitude', 'longitude']].values.tolist()

    # Add heatmap layer
    plugins.HeatMap(
        heat_data,
        radius=15,
        blur=25,
        max_zoom=13
    ).add_to(m)

    # Save map
    filepath = os.path.join(config.VIZ_DIR, 'interactive_heatmap.html')
    m.save(filepath)

    report_lines = [
        f"**GPS Points Visualized**: {len(sample_locations):,}",
        f"**Sampling Rate**: 1 in 100 points",
        f"**Map Center**: ({center_lat:.4f}, {center_lon:.4f})",
        ""
    ]

    return m, filepath, report_lines


def create_interactive_hourly_chart(routes):
    """
    Create an interactive hourly trip pattern chart using Plotly.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (plotly.Figure, filepath, report_lines)
    """
    # Aggregate by hour
    hourly = routes.groupby('unlock_hour').agg({
        'route_code': 'count',
        'duration_minutes_calculated': 'mean',
        'length': 'mean'
    }).reset_index()
    hourly.columns = ['hour', 'trip_count', 'avg_duration', 'avg_distance']

    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Trip Count by Hour', 'Average Duration & Distance by Hour'),
        vertical_spacing=0.15
    )

    # Trip count
    fig.add_trace(
        go.Bar(
            x=hourly['hour'],
            y=hourly['trip_count'],
            name='Trip Count',
            marker_color='steelblue',
            hovertemplate='Hour: %{x}<br>Trips: %{y:,}<extra></extra>'
        ),
        row=1, col=1
    )

    # Duration and distance
    fig.add_trace(
        go.Scatter(
            x=hourly['hour'],
            y=hourly['avg_duration'],
            name='Avg Duration',
            mode='lines+markers',
            line=dict(color='coral', width=3),
            hovertemplate='Hour: %{x}<br>Duration: %{y:.1f} min<extra></extra>'
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=hourly['hour'],
            y=hourly['avg_distance'],
            name='Avg Distance',
            mode='lines+markers',
            line=dict(color='green', width=3),
            yaxis='y3',
            hovertemplate='Hour: %{x}<br>Distance: %{y:.2f} km<extra></extra>'
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_xaxes(title_text="Hour of Day", row=2, col=1)
    fig.update_yaxes(title_text="Number of Trips", row=1, col=1)
    fig.update_yaxes(title_text="Avg Duration (min)", row=2, col=1)

    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Interactive Hourly Trip Analysis",
        hovermode='x unified'
    )

    # Save figure
    filepath = os.path.join(config.VIZ_DIR, 'interactive_hourly_analysis.html')
    fig.write_html(filepath)

    report_lines = [
        f"**Peak Hour**: {hourly.loc[hourly['trip_count'].idxmax(), 'hour']}:00",
        f"**Peak Hour Trips**: {hourly['trip_count'].max():,}",
        f"**Quietest Hour**: {hourly.loc[hourly['trip_count'].idxmin(), 'hour']}:00",
        ""
    ]

    return fig, filepath, report_lines


def create_interactive_station_chart(routes):
    """
    Create an interactive station popularity chart using Plotly.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (plotly.Figure, filepath, report_lines)
    """
    # Top 15 stations
    top_starts = routes['startstationname'].value_counts().head(15)
    top_ends = routes['endstationname'].value_counts().head(15)

    # Combine data
    station_data = pd.DataFrame({
        'Station': top_starts.index,
        'Starts': top_starts.values,
        'Ends': [top_ends.get(s, 0) for s in top_starts.index]
    })

    # Create grouped bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=station_data['Station'],
        y=station_data['Starts'],
        name='Trip Starts',
        marker_color='steelblue',
        hovertemplate='%{x}<br>Starts: %{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=station_data['Station'],
        y=station_data['Ends'],
        name='Trip Ends',
        marker_color='coral',
        hovertemplate='%{x}<br>Ends: %{y:,}<extra></extra>'
    ))

    fig.update_layout(
        title='Top 15 Stations - Interactive Analysis',
        xaxis_title='Station',
        yaxis_title='Number of Trips',
        barmode='group',
        height=600,
        hovermode='x unified',
        xaxis_tickangle=-45
    )

    # Save figure
    filepath = os.path.join(config.VIZ_DIR, 'interactive_stations.html')
    fig.write_html(filepath)

    report_lines = [
        f"**Top Station**: {station_data.iloc[0]['Station']}",
        f"**Top Station Starts**: {station_data.iloc[0]['Starts']:,}",
        f"**Top Station Ends**: {station_data.iloc[0]['Ends']:,}",
        ""
    ]

    return fig, filepath, report_lines


def run_interactive_visualizations(routes, locations, report):
    """
    Run all interactive visualization analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        locations (pd.DataFrame): Locations dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Analysis results
    """
    print("\n[Interactive Visualizations]")
    print("-" * 80)

    results = {}

    # Station map
    print("  • Creating interactive station map...")
    station_map, filepath, report_lines = create_station_map(routes, locations)
    results['station_map'] = {'map': station_map, 'filepath': filepath}

    report.add_section("Interactive Visualizations")
    report.add_subsection("Station Map")
    for line in report_lines:
        report.add_line(line)

    # Trip flow map
    print("  • Creating trip flow visualization...")
    flow_map, filepath, report_lines = create_trip_flow_map(routes, locations, top_n=20)
    results['flow_map'] = {'map': flow_map, 'filepath': filepath}

    report.add_subsection("Trip Flow Map")
    for line in report_lines:
        report.add_line(line)

    # Heatmap
    print("  • Creating GPS density heatmap...")
    heatmap, filepath, report_lines = create_heatmap_animation(locations)
    results['heatmap'] = {'map': heatmap, 'filepath': filepath}

    report.add_subsection("GPS Density Heatmap")
    for line in report_lines:
        report.add_line(line)

    # Interactive hourly chart
    print("  • Creating interactive hourly analysis...")
    hourly_fig, filepath, report_lines = create_interactive_hourly_chart(routes)
    results['hourly_chart'] = {'figure': hourly_fig, 'filepath': filepath}

    report.add_subsection("Interactive Hourly Analysis")
    for line in report_lines:
        report.add_line(line)

    # Interactive station chart
    print("  • Creating interactive station analysis...")
    station_fig, filepath, report_lines = create_interactive_station_chart(routes)
    results['station_chart'] = {'figure': station_fig, 'filepath': filepath}

    report.add_subsection("Interactive Station Analysis")
    for line in report_lines:
        report.add_line(line)

    print(f"  ✓ Interactive visualizations complete")
    print(f"  ✓ Generated 5 interactive visualizations")

    return results
