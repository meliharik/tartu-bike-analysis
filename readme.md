# Tartu Smart Bike Mobility Analysis

A comprehensive data analysis project examining bike-sharing patterns in Tartu, Estonia using real-world GPS and trip data from July 2019.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset Description](#dataset-description)
- [Project Status](#project-status)
- [What Has Been Completed](#what-has-been-completed)
- [Future Work](#future-work)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Key Findings (So Far)](#key-findings-so-far)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project analyzes the Tartu Smart Bike system, a bike-sharing service in Tartu, Estonia. The goal is to extract meaningful insights about mobility patterns, user behavior, and system usage through comprehensive data analysis and machine learning techniques.

### Objectives

1. **Understand usage patterns**: When, where, and how people use the bike-sharing system
2. **Identify popular routes**: Discover the most frequently used stations and routes
3. **Analyze user behavior**: Different usage patterns across membership types
4. **Predict demand**: Build models to forecast bike demand by time and location
5. **Optimize operations**: Provide insights for better resource allocation

### Research Questions

- What are the peak usage hours and days?
- Which stations are most popular?
- How do weekday and weekend patterns differ?
- What is the average trip duration and distance?
- Can we predict bike demand for different times and locations?
- Are there distinct user segments based on behavior?

---

## 📊 Dataset Description

### Data Source

Real-world data from Tartu Smart Bike system collected in July 2019.

### Raw Data Files

**Routes Data** (4 files):
- `routes_20190718.csv` - 5,261 trips
- `routes_20190719.csv` - 4,176 trips
- `routes_20190725.csv` - 5,127 trips
- `routes_20190726.csv` - 4,959 trips
- **Total**: 19,523 bike trips

**Locations Data** (4 files):
- `locations_20190718.csv` - 474,264 GPS points
- `locations_20190719.csv` - 322,633 GPS points
- `locations_20190725.csv` - 407,683 GPS points
- `locations_20190726.csv` - 361,877 GPS points
- **Total**: 1,566,457 GPS coordinates

**Data Dictionary**:
- `Smart Bike Tartu_july 2019.xlsx` - Column descriptions and metadata

### Data Characteristics

**Routes Dataset** contains:
- Trip identifiers (`route_code`)
- Bike information (`cyclenumber`)
- Timestamps (unlock/lock dates and times)
- Station information (start/end stations)
- Trip metrics (duration, distance)
- User information (membership type, costs)
- Payment method (`rfidnumber`)
- Bike type (`CycleType`)

**Locations Dataset** contains:
- Trip identifier (`route_code`)
- Bike identifier (`cyclenumber`)
- GPS coordinates (latitude, longitude)
- Timestamps (date, time)
- ~5-second intervals between GPS points

### System Overview

- **515 unique bikes** in the fleet
- **73 bike stations** across Tartu
- **11 membership types** available
- **2 bike types**: Regular and Pedelec (electric-assist)

---

## ✅ Project Status

**Current Phase**: Exploratory Data Analysis ✓ Complete
**Next Phase**: Advanced Visualizations & Statistical Analysis

### Timeline

- ✅ **Phase 1** (Completed): Data Collection & Preprocessing
- ✅ **Phase 2** (Completed): Exploratory Data Analysis
- 🔄 **Phase 3** (In Progress): Advanced Visualizations & Statistical Analysis
- 📅 **Phase 4** (Planned): Machine Learning & Predictive Modeling

---

## 🎉 What Has Been Completed

### 1. Project Setup ✓

**Environment Configuration**:
- Created project directory structure
- Initialized Git repository
- Set up `.gitignore` for Python projects
- Created virtual environment configuration

**Dependencies Management**:
- Created `requirements.txt` with 8 essential libraries:
  - `pandas==2.1.4` - Data manipulation and analysis
  - `numpy==1.26.2` - Numerical computing
  - `openpyxl==3.1.2` - Excel file handling
  - `matplotlib==3.8.2` - Data visualization
  - `seaborn==0.13.0` - Statistical visualizations
  - `jupyter==1.0.0` - Interactive notebooks
  - `scikit-learn==1.3.2` - Machine learning algorithms
  - `folium==0.15.1` - Interactive maps

**Installation Success**: All libraries installed without errors

---

### 2. Data Loading and Merging ✓

**Routes Data Processing**:
```
Input:  4 separate CSV files (19,523 records)
Process: - Loaded each file into pandas DataFrame
         - Extracted source date from filename
         - Concatenated all files
Output: Single unified routes dataset
```

**Locations Data Processing**:
```
Input:  4 separate CSV files (1,566,457 GPS points)
Process: - Loaded each file into pandas DataFrame
         - Extracted source date from filename
         - Concatenated all files
Output: Single unified locations dataset
```

**Result**: Successfully merged 8 separate files into 2 consolidated datasets

---

### 3. Data Quality Analysis ✓

**Initial Data Assessment**:

**Routes Data Quality**:
- ✓ No null values in any column
- ✓ 1 duplicate `route_code` detected
- ✓ All data types appropriate
- ✓ Date/time stored as text (requires conversion)

**Locations Data Quality**:
- ⚠️ 115 null values in date columns (0.01%)
- ✓ No null GPS coordinates
- ✓ All data types appropriate
- ✓ Date/time stored as text (requires conversion)

**Issues Identified**:
1. Date/time columns stored as separate text fields
2. One duplicate trip record
3. Some trips with invalid timestamps
4. Potential GPS outliers
5. Location records without matching routes

---

### 4. Data Cleaning and Transformation ✓

**Implemented Cleaning Operations**:

#### Routes Data Cleaning:

1. **DateTime Conversion**:
   - Combined `unlockedat` + `unlockedattime` → `unlock_datetime`
   - Combined `lockedat` + `lockedattime` → `lock_datetime`
   - Converted to proper datetime format

2. **Invalid Data Removal**:
   - Removed 23 records with invalid unlock times
   - Removed 189 records with invalid lock times
   - Removed 3 records with negative/zero duration
   - Removed 1 duplicate record
   - **Total removed**: 216 records (1.11%)

3. **Data Validation**:
   - Duration: Must be between 0-1440 minutes (24 hours)
   - Distance: Must be between 0-100 km
   - All validations passed successfully

4. **Feature Engineering** (11 new features created):
   - `duration_minutes_calculated` - Computed from unlock/lock times
   - `unlock_hour` - Hour of day (0-23)
   - `unlock_dayofweek` - Day of week (0=Monday, 6=Sunday)
   - `unlock_date` - Date only
   - `unlock_month` - Month number
   - `unlock_day` - Day of month
   - `is_weekend` - Binary flag (1=weekend, 0=weekday)
   - `time_period` - Categorical (Morning/Afternoon/Evening/Night)

5. **Text Cleaning**:
   - Stripped whitespace from station names
   - Standardized membership type text
   - Cleaned RFID number format

#### Locations Data Cleaning:

1. **DateTime Conversion**:
   - Combined `coord_date` + `coord_time` → `coord_datetime`
   - Converted to proper datetime format
   - Removed 4,668 records with invalid timestamps

2. **GPS Validation**:
   - Validated coordinates within Tartu area
   - Latitude range: 58.0°N to 59.0°N
   - Longitude range: 26.0°E to 27.5°E
   - All GPS points passed validation (0 removed)

3. **Data Integrity**:
   - Removed 36,365 location records without matching routes
   - Ensures referential integrity between datasets
   - **Total removed**: 41,033 records (2.62%)

4. **Feature Engineering** (3 new features created):
   - `coord_hour` - Hour of GPS recording
   - `coord_minute` - Minute of GPS recording
   - `coord_second` - Second of GPS recording

---

### 5. Cleaned Dataset Creation ✓

**Final Datasets**:

**routes_cleaned.csv**:
- **Records**: 19,307 (99% of original)
- **Columns**: 25 (14 original + 11 engineered)
- **Size**: ~2.5 MB
- **Quality**: No null values, no duplicates, validated ranges

**locations_cleaned.csv**:
- **Records**: 1,525,424 (97% of original)
- **Columns**: 11 (7 original + 4 engineered)
- **Size**: ~65 MB
- **Quality**: No null values, validated GPS coordinates

**Data Loss Summary**:
- Routes: 1.11% removed (excellent quality)
- Locations: 2.62% removed (excellent quality)
- Overall data integrity maintained

---

### 6. Data Quality Reporting ✓

**Generated Reports**:

1. **data_quality_report.txt**:
   - Initial data state statistics
   - Cleaning operations summary
   - Final data statistics
   - Unique value counts
   - Numerical summaries (mean, median, min, max, std)
   - GPS coordinate ranges

2. **routes_columns.txt**:
   - Complete list of 25 columns
   - Data type for each column
   - Column descriptions

3. **locations_columns.txt**:
   - Complete list of 11 columns
   - Data type for each column
   - Column descriptions

---

### 7. Automated Pipeline Creation ✓

**Created Script**: `scripts/01_data_preprocessing.py`

**Script Capabilities**:
- ✅ Automatically finds and loads all data files
- ✅ Performs comprehensive data quality checks
- ✅ Executes all cleaning operations
- ✅ Generates detailed quality reports
- ✅ Saves cleaned data in structured format
- ✅ Fully documented with comments
- ✅ Progress tracking with console output
- ✅ Error handling and validation
- ✅ Reproducible and reusable

**Execution Time**: ~30-60 seconds for complete pipeline

**Script Features**:
- Modular design (5 distinct phases)
- Clear progress indicators
- Comprehensive logging
- Automatic directory creation
- Cross-platform compatibility
- Configurable file paths

---

### 8. Documentation ✓

**Created Documentation**:

1. **GUIDE.md** (Comprehensive learning resource):
   - Python fundamentals explained
   - How Python works (execution flow)
   - Library concepts and explanations
   - Detailed breakdown of all 8 libraries used
   - How to run Python scripts (3 methods)
   - Code structure walkthrough
   - Common issues and solutions
   - Key programming concepts
   - Additional learning resources

2. **HOW_TO_RUN.md** (Quick-start guide):
   - Step-by-step setup instructions
   - Command-line reference
   - Troubleshooting guide
   - File structure overview
   - Data flow explanation
   - Quick command reference

3. **This README.md**:
   - Project overview and objectives
   - Complete progress documentation
   - Detailed methodology
   - Results and findings

**Documentation Features**:
- Beginner-friendly language
- Code examples with explanations
- Visual diagrams (ASCII art)
- Practical troubleshooting
- Learning resources
- Quick reference sections

---

### 9. Key Statistics Discovered ✓

**Trip Statistics**:
```
Average trip duration:  22.18 minutes
Median trip duration:   13.93 minutes
Longest trip:           1,366 minutes (22.7 hours)
Shortest trip:          0.50 minutes

Average trip distance:  3.01 km
Median trip distance:   2.38 km
Longest trip:           37.95 km
Shortest trip:          0.00 km (station returns)
```

**System Usage**:
```
Unique bikes:           515
Unique stations:        73
Membership types:       11
Bike types:             2
```

**Cost Distribution**:
```
Average cost:           €0.05
Median cost:            €0.00 (most rides free)
Maximum cost:           €4.00
```

**GPS Coverage**:
```
Latitude range:         58.293°N - 58.437°N
Longitude range:        26.607°E - 26.896°E
Average GPS points/trip: ~79 points
Recording interval:     ~5 seconds
```

---

### 10. Exploratory Data Analysis (EDA) ✓

**Modular Analysis Architecture**:
- Created `analysis/` package with modular design
- Separated concerns: temporal, spatial, utilities
- Reusable plotting and reporting functions
- Centralized configuration management

**Temporal Analysis**:
- ✅ Hourly usage patterns (peak: 17:00 with 1,639 trips)
- ✅ Day-of-week patterns (Thursday busiest: 10,320 trips)
- ✅ Weekend vs weekday comparison
- ✅ Time period analysis (Morning/Afternoon/Evening/Night)
- ✅ Generated visualizations: `hourly_pattern.png`, `daily_pattern.png`, `weekend_comparison.png`

**Spatial Analysis**:
- ✅ Popular stations ranking (Uueturu: 1,176 start trips)
- ✅ Trip type analysis (11.9% round trips, 88.1% one-way)
- ✅ Popular routes identification (top OD pairs)
- ✅ Generated visualizations: `top_stations.png`, `top_routes.png`

**Created Scripts**:
- `scripts/02_run_eda.py` - Main EDA orchestrator
- `scripts/analysis/temporal_analysis.py` - Time-based analyses
- `scripts/analysis/spatial_analysis.py` - Location-based analyses
- `scripts/analysis/data_loader.py` - Data loading utilities
- `scripts/analysis/utils/plotting.py` - Visualization helpers
- `scripts/analysis/utils/reporting.py` - Report generation

**Generated Outputs**:
- ✅ EDA Report: `reports/eda_report.md`
- ✅ 9+ visualizations in `visualizations/` subdirectories
- ✅ Time series charts (hourly, daily, weekend patterns)
- ✅ Statistical charts (stations, routes, distributions)
- ✅ Distribution plots (duration, distance, correlations)

**Key Insights Discovered**:
- Peak usage at 17:00 (evening commute)
- Uueturu is the most popular station (hub location)
- 88% of trips are one-way (commuter pattern)
- Afternoon period has highest trip count (7,570 trips)
- Evening trips are longest on average (24.51 minutes)

---

## 🚀 Future Work

### Phase 3: Advanced Visualizations & Statistical Analysis

**Planned Enhancements**:

1. **Enhanced Visualizations**:
   - Interactive maps with folium (station heatmaps, route flows)
   - GPS trajectory visualization
   - Origin-Destination flow maps
   - Service area coverage maps
   - Real-time style interactive dashboards

2. **Statistical Analysis**:
   - Correlation analysis (duration vs distance, time vs usage)
   - Hypothesis testing (usage pattern differences)
   - Distribution fitting (trip duration, distance)
   - Outlier detection and analysis
   - Statistical significance tests

3. **User Behavior Deep Dive**:
   - Membership type comparison (detailed analysis)
   - User segmentation analysis
   - Trip duration/distance distributions by user type
   - Bike type performance comparison (Regular vs Pedelec)
   - Cost analysis and pricing patterns

4. **Bike Utilization Analysis**:
   - Individual bike usage frequency
   - Fleet efficiency metrics
   - Maintenance indicators
   - Bike turnover rates
   - Station capacity analysis

**Deliverables**:
- Enhanced visualization scripts
- Interactive HTML maps
- Statistical analysis report
- User behavior insights document

---


### Phase 4: Machine Learning and Predictive Modeling

**Planned ML Projects**:

1. **Demand Prediction**:
   - **Objective**: Forecast bike demand by hour/station
   - **Approach**: Time series forecasting (ARIMA, LSTM)
   - **Features**: Hour, day, weather, station, historical data
   - **Metric**: RMSE, MAE

2. **Route Clustering**:
   - **Objective**: Identify common route patterns
   - **Approach**: K-means, DBSCAN on GPS trajectories
   - **Features**: Start/end points, path similarity
   - **Output**: Route clusters, typical patterns

3. **User Segmentation**:
   - **Objective**: Classify users into behavior groups
   - **Approach**: Clustering (K-means, hierarchical)
   - **Features**: Trip frequency, duration, distance, time
   - **Output**: User personas, characteristics

4. **Anomaly Detection**:
   - **Objective**: Identify unusual trips or system issues
   - **Approach**: Isolation Forest, Autoencoder
   - **Features**: Duration, distance, speed, route
   - **Output**: Anomaly scores, flagged trips

5. **Station Recommendation**:
   - **Objective**: Suggest optimal station placements
   - **Approach**: Optimization, clustering analysis
   - **Features**: Usage density, coverage gaps
   - **Output**: Recommended new station locations

**Deliverables**:
- Python scripts: `04_machine_learning.py`
- Trained models (saved in `models/`)
- Model evaluation reports
- Prediction visualizations
- Recommendation dashboard

---

## 💻 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (for version control)
- 200+ MB free disk space

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd tartu-bike-analysis
```

### Step 2: Install Dependencies

```bash
pip3 install -r requirements.txt
```

This installs all required libraries:
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- scikit-learn (machine learning)
- folium (interactive maps)
- jupyter (notebooks)
- openpyxl (Excel support)

**Installation time**: ~2-5 minutes

### Step 3: Verify Installation

```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, sklearn, folium; print('All libraries installed successfully!')"
```

---

## 🔧 Usage

### Running the Data Preprocessing Pipeline

```bash
# Navigate to project directory
cd tartu-bike-analysis

# Run the preprocessing script
python3 scripts/01_data_preprocessing.py
```

**Expected output**:
```
================================================================================
TARTU BIKE DATA - DATA PREPROCESSING AND CLEANING
================================================================================

[1/5] Loading Data...
[2/5] Analyzing Data Quality (Initial State)...
[3/5] Cleaning Data...
[4/5] Cleaned Data Statistics...
[5/5] Saving Cleaned Data...

DATA PREPROCESSING COMPLETED!
```

### Output Files

After running, check `processed_data/` folder:
- ✓ `routes_cleaned.csv` (19,307 trips)
- ✓ `locations_cleaned.csv` (1,525,424 GPS points)
- ✓ `data_quality_report.txt`
- ✓ `routes_columns.txt`
- ✓ `locations_columns.txt`

### Running the Exploratory Data Analysis

```bash
# Run the EDA script
python3 scripts/02_run_eda.py
```

**Expected output**:
```
================================================================================
TARTU BIKE DATA - EXPLORATORY DATA ANALYSIS
================================================================================

[Setup]
[Data Loading]
  ✓ Routes loaded: 19,307 records
  ✓ Locations loaded: 1,525,424 GPS points
[Temporal Analysis]
  • Analyzing hourly patterns...
  • Analyzing daily patterns...
  • Comparing weekday vs weekend...
  • Analyzing time periods...
  ✓ Temporal analysis complete
[Spatial Analysis]
  • Analyzing popular stations...
  • Analyzing trip types...
  • Analyzing popular routes...
  ✓ Spatial analysis complete
[Saving Report]
  ✓ Report saved: reports/eda_report.md

EXPLORATORY DATA ANALYSIS COMPLETED!
```

**Generated Outputs**:
- ✓ EDA Report: `reports/eda_report.md`
- ✓ Visualizations in `visualizations/` subdirectories
- ✓ Time series charts, statistical charts, distribution plots

### Using Cleaned Data in Python

```python
import pandas as pd

# Load cleaned routes data
routes = pd.read_csv('processed_data/routes_cleaned.csv')
print(routes.head())

# Load cleaned locations data
locations = pd.read_csv('processed_data/locations_cleaned.csv')
print(locations.head())

# Example analysis: Average trip duration by hour
hourly_avg = routes.groupby('unlock_hour')['duration_minutes_calculated'].mean()
print(hourly_avg)
```

### Using the Analysis Package

```python
from analysis.data_loader import load_routes_data, load_locations_data
from analysis.temporal_analysis import analyze_hourly_patterns
from analysis.spatial_analysis import analyze_popular_stations

# Load data using the package
routes = load_routes_data()
locations = load_locations_data()

# Run specific analyses
hourly_data, peak_hour, viz_files, report_lines = analyze_hourly_patterns(routes)
top_start, top_end, viz_files, report_lines = analyze_popular_stations(routes)
```

### Using Jupyter Notebooks (Interactive Analysis)

```bash
# Start Jupyter
jupyter notebook

# Browser opens automatically
# Create new notebook or open existing
# Run analysis interactively
```

---

## 📁 Project Structure

```
tartu-bike-analysis/
│
├── data/                              # Raw data (DO NOT MODIFY)
│   ├── routes_20190718.csv            # Trip data - July 18
│   ├── routes_20190719.csv            # Trip data - July 19
│   ├── routes_20190725.csv            # Trip data - July 25
│   ├── routes_20190726.csv            # Trip data - July 26
│   ├── locations_20190718.csv         # GPS data - July 18
│   ├── locations_20190719.csv         # GPS data - July 19
│   ├── locations_20190725.csv         # GPS data - July 25
│   ├── locations_20190726.csv         # GPS data - July 26
│   └── Smart Bike Tartu_july 2019.xlsx # Data dictionary
│
├── processed_data/                    # Cleaned data (GENERATED)
│   ├── routes_cleaned.csv             # Cleaned trip data
│   ├── locations_cleaned.csv          # Cleaned GPS data
│   ├── data_quality_report.txt        # Quality metrics
│   ├── routes_columns.txt             # Routes schema
│   └── locations_columns.txt          # Locations schema
│
├── scripts/                           # Python scripts
│   ├── 01_data_preprocessing.py       # Data cleaning pipeline
│   ├── 02_run_eda.py                  # EDA orchestrator
│   ├── 03_visualization.py            # Advanced visualizations (planned)
│   ├── 04_machine_learning.py         # ML models (planned)
│   └── analysis/                      # Modular analysis package
│       ├── __init__.py                # Package initialization
│       ├── config.py                  # Configuration & constants
│       ├── data_loader.py             # Data loading utilities
│       ├── temporal_analysis.py      # Time-based analyses
│       ├── spatial_analysis.py        # Location-based analyses
│       └── utils/                      # Utility modules
│           ├── plotting.py            # Visualization helpers
│           └── reporting.py           # Report generation
│
├── notebooks/                         # Jupyter notebooks (planned)
│   ├── EDA.ipynb                      # Exploratory analysis
│   ├── Visualizations.ipynb           # Chart creation
│   └── ML_Models.ipynb                # Model building
│
├── visualizations/                    # Generated charts
│   ├── time_series/                   # Time-based plots
│   │   ├── hourly_pattern.png         # Hourly usage patterns
│   │   ├── daily_pattern.png          # Day-of-week patterns
│   │   └── weekend_comparison.png     # Weekday vs weekend
│   ├── maps/                          # Geographic visualizations
│   │   └── gps_density_heatmap.png   # GPS density map
│   ├── statistical/                   # Statistical charts
│   │   ├── top_stations.png          # Popular stations
│   │   ├── top_routes.png            # Popular routes
│   │   ├── bike_type_comparison.png  # Bike type analysis
│   │   ├── membership_types.png      # Membership analysis
│   │   ├── correlation_matrix.png    # Feature correlations
│   │   └── cost_distribution.png     # Cost analysis
│   └── distributions/                 # Distribution plots
│       ├── trip_distributions.png     # Trip metrics
│       └── duration_vs_distance.png  # Scatter analysis
│
├── models/                            # Trained ML models (planned)
│   ├── demand_prediction/
│   ├── clustering/
│   └── anomaly_detection/
│
├── reports/                           # Analysis reports
│   ├── eda_report.md                  # EDA findings (✓ Complete)
│   ├── statistical_analysis.md       # Statistical analysis (planned)
│   └── ml_results.md                  # ML results (planned)
│
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── readme.md                          # This file
├── GUIDE.md                           # Python learning guide
└── HOW_TO_RUN.md                      # Quick start guide
```

---

## 🔄 Data Pipeline

### Current Pipeline (Completed)

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAW DATA (8 files)                         │
│  • 4 routes CSV files (19,523 trips)                            │
│  • 4 locations CSV files (1,566,457 GPS points)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LOADING & MERGING                             │
│  • Read CSV files with pandas                                   │
│  • Add source date column                                       │
│  • Concatenate into unified datasets                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   QUALITY ANALYSIS                              │
│  • Check data types                                             │
│  • Identify null values                                         │
│  • Detect duplicates                                            │
│  • Validate ranges                                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA CLEANING                                 │
│  Routes:                    Locations:                          │
│  • DateTime conversion      • DateTime conversion               │
│  • Remove invalid dates     • Remove invalid dates              │
│  • Validate duration        • Validate GPS coords               │
│  • Validate distance        • Filter orphan records             │
│  • Remove duplicates        • Add time features                 │
│  • Add 11 new features                                          │
│  • Clean text fields                                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLEANED DATA                                  │
│  • routes_cleaned.csv (19,307 records, 25 columns)              │
│  • locations_cleaned.csv (1,525,424 records, 11 columns)        │
│  • Quality reports generated                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Current Pipeline (Including EDA)

```
┌─────────────────────────────────────────────────────────────────┐
│                   CLEANED DATA                                  │
│  • routes_cleaned.csv (19,307 records, 25 columns)              │
│  • locations_cleaned.csv (1,525,424 records, 11 columns)        │
│  • Quality reports generated                                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXPLORATORY DATA ANALYSIS (EDA)                    │
│  Temporal Analysis:          Spatial Analysis:                   │
│  • Hourly patterns          • Station popularity                │
│  • Daily patterns           • Route analysis                    │
│  • Weekend comparison       • Trip type classification          │
│  • Time period analysis     • OD matrix                         │
│  Output: Visualizations + EDA Report                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              VISUALIZATIONS & STATISTICAL ANALYSIS              │
│  • Interactive maps (folium)                                    │
│  • Advanced statistical charts                                  │
│  • Correlation analysis                                         │
│  • Distribution fitting                                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              MACHINE LEARNING & PREDICTIVE MODELING             │
│  • Demand prediction                                           │
│  • Route clustering                                            │
│  • User segmentation                                           │
│  • Anomaly detection                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Key Findings (So Far)

### 1. Data Quality
- ✅ **Excellent quality**: Only 1-3% data loss after cleaning
- ✅ **Complete GPS coverage**: All coordinates within Tartu area
- ✅ **Reliable timestamps**: 99% valid datetime records
- ✅ **Consistent structure**: No schema issues

### 2. Usage Patterns (Preliminary)

**Trip Duration**:
- Most trips are short (median: 13.93 minutes)
- Average pulled up by longer trips (mean: 22.18 minutes)
- Some very long trips detected (max: 22+ hours)

**Trip Distance**:
- Compact city usage (median: 2.38 km)
- Average: 3.01 km
- Some outlier long trips (max: 37.95 km)

**Cost Structure**:
- Most rides are free (median cost: €0.00)
- Suggests many users have free memberships
- Maximum charge: €4.00

### 3. System Characteristics

**Fleet Size**: 515 bikes serving 73 stations
- Good coverage ratio: ~7 bikes per station
- Mix of regular and electric bikes (Pedelec)

**GPS Tracking**: ~79 GPS points per trip
- High-resolution tracking (~5 second intervals)
- Enables detailed route reconstruction

### 4. Data Availability

**Temporal Coverage**: 4 days in July 2019
- 2 days from mid-July (18-19)
- 2 days from late July (25-26)
- Limited but sufficient for pattern analysis

**Completeness**:
- All trips have GPS trajectories
- All required fields present
- Membership and payment info available

### 5. Exploratory Data Analysis Findings

**Temporal Patterns**:
- **Peak hour**: 17:00 (1,639 trips) - Evening commute
- **Quietest hour**: 5:00 (159 trips) - Early morning
- **Busiest day**: Thursday (10,320 trips)
- **Average trips/hour**: 965.4 trips
- **Time period distribution**: Afternoon (7,570), Evening (5,679), Morning (3,225), Night (2,833)

**Spatial Patterns**:
- **Most popular station**: Uueturu (1,176 start trips, 1,146 end trips)
- **Top 5 stations**: Uueturu, Soola, Eeden, Pirogovi plats, Vabadussild
- **Trip types**: 88.1% one-way trips, 11.9% round trips
- **Most popular route**: Veeriku → Kannikese (60 trips)

**Usage Characteristics**:
- Evening trips are longest (avg 24.51 minutes)
- Morning trips are shortest (avg 15.80 minutes)
- Afternoon has highest trip volume
- Night trips have longest average distance (3.33 km)

---

## 🛠 Technologies Used

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Primary programming language |
| pandas | 2.1.4 | Data manipulation and analysis |
| numpy | 1.26.2 | Numerical computing |
| matplotlib | 3.8.2 | Data visualization |
| seaborn | 0.13.0 | Statistical visualizations |
| scikit-learn | 1.3.2 | Machine learning |
| folium | 0.15.1 | Interactive maps |
| jupyter | 1.0.0 | Interactive notebooks |
| openpyxl | 3.1.2 | Excel file handling |

### Development Tools

- **Git**: Version control
- **GitHub**: Code repository
- **VS Code**: Code editor
- **Terminal**: Script execution

### Data Format Standards

- **CSV**: Primary data format
- **UTF-8**: Text encoding
- **ISO 8601**: Datetime format
- **WGS84**: GPS coordinate system

---

## 🤝 Contributing

This is an academic/research project. Contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Areas

- **Code improvements**: Optimize existing scripts
- **New analyses**: Add additional analytical techniques
- **Visualizations**: Create new charts and maps
- **Documentation**: Improve guides and comments
- **Bug fixes**: Report and fix issues

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- **Tartu Smart Bike**: For providing the dataset
- **City of Tartu**: For operating the bike-sharing system
- **Open Source Community**: For the amazing Python libraries

---

## 📚 Additional Resources

### Learning Materials

- **Python Basics**: See `GUIDE.md` for comprehensive Python tutorial
- **Quick Start**: See `HOW_TO_RUN.md` for step-by-step instructions
- **Data Reports**: Check `processed_data/data_quality_report.txt`

### External Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/index.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Folium Examples](https://python-visualization.github.io/folium/)

---

**Last Updated**: December 7, 2024
**Project Status**: Phase 1 & 2 Complete, Phase 3 In Progress
**Next Milestone**: Advanced Visualizations & Statistical Analysis

---

*This project demonstrates the complete data science workflow: from raw data to actionable insights.*
