"""
Tartu Bike Data - Interactive Dashboard
========================================

Streamlit dashboard for interactive data exploration.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page config
st.set_page_config(
    page_title="Tartu Bike Analysis Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load cleaned data"""
    routes = pd.read_csv('processed_data/routes_cleaned.csv')
    routes['unlock_datetime'] = pd.to_datetime(routes['unlock_datetime'])
    routes['lock_datetime'] = pd.to_datetime(routes['lock_datetime'])
    return routes

# Header
st.markdown('<h1 class="main-header">🚲 Tartu Smart Bike Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Load data
try:
    routes = load_data()

    # Sidebar filters
    st.sidebar.header("📊 Filters")

    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(routes['unlock_datetime'].min(), routes['unlock_datetime'].max()),
        min_value=routes['unlock_datetime'].min(),
        max_value=routes['unlock_datetime'].max()
    )

    # Bike type filter
    bike_types = ['All'] + list(routes['CycleType'].unique())
    selected_bike_type = st.sidebar.selectbox("Bike Type", bike_types)

    # Time period filter
    time_periods = ['All'] + list(routes['time_period'].unique())
    selected_time_period = st.sidebar.selectbox("Time Period", time_periods)

    # Apply filters
    filtered_routes = routes.copy()
    if selected_bike_type != 'All':
        filtered_routes = filtered_routes[filtered_routes['CycleType'] == selected_bike_type]
    if selected_time_period != 'All':
        filtered_routes = filtered_routes[filtered_routes['time_period'] == selected_time_period]

    # Key metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Trips", f"{len(filtered_routes):,}")
    with col2:
        st.metric("Avg Duration", f"{filtered_routes['duration_minutes_calculated'].mean():.1f} min")
    with col3:
        st.metric("Avg Distance", f"{filtered_routes['length'].mean():.2f} km")
    with col4:
        st.metric("Unique Bikes", f"{filtered_routes['cyclenumber'].nunique():,}")
    with col5:
        st.metric("Unique Stations", f"{filtered_routes['startstationname'].nunique():,}")

    st.markdown("---")

    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Temporal Analysis", "🗺️ Spatial Analysis", "📈 Statistical Analysis", "🤖 ML Insights"])

    with tab1:
        st.header("Temporal Patterns")

        col1, col2 = st.columns(2)

        with col1:
            # Hourly pattern
            hourly = filtered_routes.groupby('unlock_hour').size().reset_index(name='count')
            fig = px.bar(
                hourly,
                x='unlock_hour',
                y='count',
                title='Trips by Hour of Day',
                labels={'unlock_hour': 'Hour', 'count': 'Number of Trips'},
                color='count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Daily pattern
            daily = filtered_routes.groupby('unlock_dayofweek').size().reset_index(name='count')
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily['day_name'] = daily['unlock_dayofweek'].map(dict(enumerate(day_names)))
            fig = px.bar(
                daily,
                x='day_name',
                y='count',
                title='Trips by Day of Week',
                labels={'day_name': 'Day', 'count': 'Number of Trips'},
                color='count',
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Time period comparison
        time_period_stats = filtered_routes.groupby('time_period').agg({
            'route_code': 'count',
            'duration_minutes_calculated': 'mean',
            'length': 'mean'
        }).reset_index()
        time_period_stats.columns = ['Time Period', 'Trip Count', 'Avg Duration (min)', 'Avg Distance (km)']

        st.subheader("Time Period Statistics")
        st.dataframe(time_period_stats, use_container_width=True)

    with tab2:
        st.header("Spatial Patterns")

        col1, col2 = st.columns(2)

        with col1:
            # Top start stations
            top_starts = filtered_routes['startstationname'].value_counts().head(10)
            fig = px.bar(
                x=top_starts.values,
                y=top_starts.index,
                orientation='h',
                title='Top 10 Start Stations',
                labels={'x': 'Number of Trips', 'y': 'Station'},
                color=top_starts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Top end stations
            top_ends = filtered_routes['endstationname'].value_counts().head(10)
            fig = px.bar(
                x=top_ends.values,
                y=top_ends.index,
                orientation='h',
                title='Top 10 End Stations',
                labels={'x': 'Number of Trips', 'y': 'Station'},
                color=top_ends.values,
                color_continuous_scale='Plasma'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Top routes
        st.subheader("Top 10 Popular Routes")
        top_routes = filtered_routes.groupby(['startstationname', 'endstationname']).size().reset_index(name='count')
        top_routes = top_routes.sort_values('count', ascending=False).head(10)
        top_routes['route'] = top_routes['startstationname'] + ' → ' + top_routes['endstationname']

        fig = px.bar(
            top_routes,
            x='count',
            y='route',
            orientation='h',
            title='Most Popular Routes',
            labels={'count': 'Number of Trips', 'route': 'Route'},
            color='count',
            color_continuous_scale='Turbo'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Statistical Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Duration distribution
            fig = px.histogram(
                filtered_routes,
                x='duration_minutes_calculated',
                nbins=50,
                title='Trip Duration Distribution',
                labels={'duration_minutes_calculated': 'Duration (minutes)', 'count': 'Frequency'},
                color_discrete_sequence=['steelblue']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Distance distribution
            fig = px.histogram(
                filtered_routes,
                x='length',
                nbins=50,
                title='Trip Distance Distribution',
                labels={'length': 'Distance (km)', 'count': 'Frequency'},
                color_discrete_sequence=['coral']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Bike type comparison
        st.subheader("Bike Type Comparison")
        bike_stats = filtered_routes.groupby('CycleType').agg({
            'route_code': 'count',
            'duration_minutes_calculated': 'mean',
            'length': 'mean',
            'costs': 'mean'
        }).reset_index()
        bike_stats.columns = ['Bike Type', 'Trip Count', 'Avg Duration (min)', 'Avg Distance (km)', 'Avg Cost']
        st.dataframe(bike_stats, use_container_width=True)

        # Correlation matrix
        st.subheader("Correlation Analysis")
        corr_features = ['duration_minutes_calculated', 'length', 'costs', 'unlock_hour']
        corr_matrix = filtered_routes[corr_features].corr()

        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            title='Feature Correlation Matrix',
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Machine Learning Insights")

        st.info("💡 This section displays insights from ML models trained on the complete dataset.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("User Segmentation")
            st.markdown("""
            **Heavy Users (88.5%)**:
            - Average 37-53 trips
            - Most active segment
            - Core user base

            **Regular Users (8.2%)**:
            - Moderate usage
            - 15-30 trips average

            **Occasional Users (3.3%)**:
            - Low frequency
            - < 5 trips
            """)

        with col2:
            st.subheader("Anomaly Detection")
            st.markdown("""
            **Anomalies Detected: 5%**

            Characteristics:
            - Duration: 84.4 min (vs 18.9 normal)
            - Distance: 7.58 km (vs 2.77 normal)
            - Most during night hours (0:00-6:00)
            - Potential outliers or special use cases
            """)

        st.subheader("Interactive Maps & Visualizations")
        st.markdown("""
        The following interactive HTML visualizations are available:
        - 🗺️ **Station Map**: All bike stations with trip counts
        - 🔀 **Trip Flow Map**: Popular routes visualization
        - 🔥 **GPS Heatmap**: Density of bike usage across Tartu
        - 📊 **Interactive Charts**: Hourly and station analysis

        *Open the HTML files in `visualizations/` directory to explore these maps.*
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚲 Tartu Smart Bike Analysis Dashboard | Data Period: July 2019 | Total Trips: 19,307</p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Data files not found! Please run `python3 scripts/01_data_preprocessing.py` first.")
    st.info("📝 This will process the raw data and create the necessary files.")
