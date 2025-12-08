# Tartu Smart Bike Mobility Analysis

Comprehensive data analysis of Tartu bike-sharing system using real-world GPS and trip data from July 2019.

---

## 🎯 Project Overview

Analysis of Tartu Smart Bike system (Estonia) to understand mobility patterns, user behavior, and system usage through data science and visualization techniques.

### Research Questions

- What are the peak usage hours and days?
- Which stations and routes are most popular?
- How do weekday and weekend patterns differ?
- What factors influence trip duration and distance?
- Are there distinct user segments?

---

## 📊 Dataset

**Source**: Tartu Smart Bike system, July 2019

**Raw Data**:
- 4 route files: 19,523 bike trips
- 4 location files: 1,566,457 GPS points
- 1 data dictionary: Column descriptions

**System Characteristics**:
- 515 unique bikes
- 73 bike stations
- 11 membership types
- 2 bike types (Regular & Pedelec)

---

## ✅ Completed Work

### Phase 1: Data Preprocessing ✓

**What We Did**:
- Merged 8 separate CSV files into unified datasets
- Cleaned invalid data (timestamps, GPS coordinates, duplicates)
- Created 14 new features (time-based, flags, calculated metrics)
- Generated comprehensive quality reports

**Results**:
- Routes: 19,307 clean records (1.11% data loss)
- Locations: 1,525,424 GPS points (2.62% data loss)
- Output: 2 cleaned CSV files + quality reports

**Key Statistics**:
- Average trip: 22.18 minutes, 3.01 km
- Trip range: 0.5 min to 22+ hours
- Distance range: 0 km to 38 km
- Free trips: 96.8%

---

### Phase 2: Exploratory Data Analysis (EDA) ✓

**What We Did**:
- Temporal analysis (hourly, daily, weekend patterns)
- Spatial analysis (station popularity, routes, trip types)
- Created 12 high-quality visualizations (time series, statistical charts)
- Generated comprehensive markdown report

**Key Findings**:

**Temporal Patterns**:
- Peak hour: 17:00 (1,639 trips) - evening commute
- Busiest day: Thursday (10,320 trips)
- Quietest hour: 5:00 (159 trips)
- Time periods: Afternoon most popular (7,570 trips)

**Spatial Patterns**:
- Most popular station: Uueturu (1,176 starts, 1,146 ends)
- Round trips: 11.9% (2,288 trips)
- One-way trips: 88.1% (17,019 trips)
- Top route: Specific OD pairs identified

**Correlations**:
- Duration vs Distance: 0.489 (moderate positive)
- Trip characteristics vary by time period
- Station usage highly concentrated (top 10 stations)

---

## 🏗️ Technical Architecture

### Modular Design

We implemented a **modular architecture** for maintainability and scalability:

```
scripts/
├── 01_data_preprocessing.py    # Data cleaning pipeline (415 lines)
├── 02_run_eda.py               # EDA orchestrator (96 lines)
└── analysis/                    # Modular analysis package
    ├── config.py                # Configuration & constants
    ├── data_loader.py           # Data loading utilities
    ├── temporal_analysis.py     # Time-based analysis
    ├── spatial_analysis.py      # Location-based analysis
    └── utils/
        ├── plotting.py          # Reusable plotting functions
        └── reporting.py         # Report generation
```

**Benefits**:
- Single Responsibility: Each module has one purpose
- Reusability: Common functions in utils/
- Testability: Each module independently testable
- Maintainability: Easy to locate and modify code

---

## 📁 Project Structure

```
tartu-bike-analysis/
├── data/                       # Raw data (8 CSV files + Excel)
├── processed_data/             # Cleaned data (generated)
├── scripts/
│   ├── 01_data_preprocessing.py
│   ├── 02_run_eda.py
│   └── analysis/               # Modular analysis package
├── visualizations/             # Generated charts (12 PNG files)
│   ├── time_series/
│   ├── statistical/
│   ├── distributions/
│   └── maps/
├── reports/
│   └── eda_report.md           # Comprehensive analysis report
├── requirements.txt            # Python dependencies
└── readme.md                   # This file
```

---

## 💻 Installation & Usage

### Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Libraries: pandas, numpy, matplotlib, seaborn, scikit-learn, folium, jupyter, openpyxl
```

### Run Analysis

```bash
# Step 1: Clean and prepare data
python3 scripts/01_data_preprocessing.py

# Step 2: Run exploratory analysis
python3 scripts/02_run_eda.py
```

### Output

After running scripts:
- `processed_data/`: 2 cleaned CSV files + quality reports
- `visualizations/`: 12 high-resolution charts (300 DPI)
- `reports/eda_report.md`: Complete analysis report

---

## 📈 Key Insights Summary

### Usage Patterns
- **Peak Period**: Weekday evenings (17:00) - commuter-focused
- **Consistent Weekday**: Thursday most popular
- **Short Trips**: Median 13.93 min, 2.38 km (urban commuting)
- **Free Model**: 96.8% of trips free (membership-based system)

### Station Analysis
- **Concentrated Usage**: Top station (Uueturu) handles ~6% of all trips
- **Point-to-Point**: 88% one-way trips (not round-trip focused)
- **Urban Coverage**: 73 stations across Tartu

### System Health
- **High Data Quality**: Only 1-3% data loss after cleaning
- **Complete GPS**: All trips have detailed GPS tracking (~79 points/trip)
- **Reliable System**: Consistent patterns across analysis period

---

## 🛠 Technologies

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Programming language |
| pandas | Data manipulation |
| numpy | Numerical computing |
| matplotlib | Visualization |
| seaborn | Statistical plots |
| scikit-learn | Machine learning (future) |
| folium | Interactive maps (future) |

---

## 📊 Generated Visualizations

**Time Series** (3 charts):
- Hourly trip patterns (bar + line)
- Daily trip patterns (by weekday)
- Weekend vs weekday comparison

**Statistical** (6 charts):
- Top 10 start/end stations
- Top 10 popular routes
- Membership type distribution
- Bike type comparison
- Cost distribution
- Correlation matrix

**Distributions** (2 charts):
- Trip duration/distance histograms + boxplots
- Duration vs distance scatter plot

**Maps** (1 chart):
- GPS density heatmap (Tartu area)

---

## 📄 Documentation

- **Main README**: This file
- **Analysis Package**: `scripts/analysis/README.md` (architecture details)
- **EDA Report**: `reports/eda_report.md` (complete findings)
- **Data Quality Report**: `processed_data/data_quality_report.txt`

---

## 🎓 Project Status

**Current**: Phase 2 Complete (Exploratory Data Analysis)

**Completed Phases**:
1. ✅ Data Preprocessing - Cleaning and feature engineering
2. ✅ Exploratory Data Analysis - Patterns and visualizations

**What's Next**:
- Advanced visualizations (interactive maps, animations)
- Statistical testing and correlations
- Machine learning models (demand prediction, clustering)
- User segmentation analysis

---

## 📧 Contact & Contributing

This is an academic research project. For questions or collaboration:
- Open an issue on GitHub
- Follow software engineering best practices
- Maintain modular architecture

---

**Last Updated**: December 2024
**Analysis Period**: July 2019 (4 days of data)
**Total Trips Analyzed**: 19,307
**Total GPS Points**: 1,525,424

---

*Clean code, modular design, actionable insights.*
