# Analysis Package

Modular analysis package for Tartu bike-sharing data.

## Architecture

This package follows **modular design principles** for better maintainability, reusability, and testability.

### Package Structure

```
analysis/
├── __init__.py                # Package initialization
├── config.py                  # Configuration and constants (66 lines)
├── data_loader.py             # Data loading utilities (85 lines)
├── temporal_analysis.py       # Time-based analysis (238 lines)
├── spatial_analysis.py        # Location-based analysis (163 lines)
└── utils/
    ├── __init__.py
    ├── plotting.py            # Plotting utilities (215 lines)
    └── reporting.py           # Report generation (151 lines)
```

**Total**: ~920 lines across 8 focused modules (vs 550+ lines in one file)

## Design Principles

### 1. **Single Responsibility Principle**
Each module has one clear purpose:
- `config.py` → All configuration in one place
- `data_loader.py` → Data loading only
- `temporal_analysis.py` → Time-based analysis only
- `spatial_analysis.py` → Location-based analysis only
- `utils/plotting.py` → Reusable plotting functions
- `utils/reporting.py` → Report generation utilities

### 2. **Separation of Concerns**
- **Analysis logic** separated from **visualization**
- **Visualization** separated from **file saving**
- **Configuration** separated from **implementation**

### 3. **Reusability**
Common functions in `utils/` can be used across all analysis modules:
```python
from analysis.utils import plotting

# Reusable plotting function
fig = plotting.create_bar_chart(data, title, xlabel, ylabel)
```

### 4. **Testability**
Each module can be tested independently:
```python
# Test temporal analysis without running entire pipeline
from analysis.temporal_analysis import analyze_hourly_patterns
result = analyze_hourly_patterns(routes)
```

## Usage

### Running Full Analysis

```bash
python3 scripts/02_run_eda.py
```

### Using Individual Modules

```python
# Load data
from analysis.data_loader import load_routes_data
routes = load_routes_data()

# Run specific analysis
from analysis.temporal_analysis import analyze_hourly_patterns
hourly_data, peak_hour, viz, report = analyze_hourly_patterns(routes)

# Use plotting utilities
from analysis.utils import plotting
fig = plotting.create_bar_chart(data, "Title", "X", "Y")
```

## Benefits

### Before (Monolithic)
```
02_exploratory_analysis.py (550+ lines)
├── Load data
├── Temporal analysis
├── Spatial analysis
├── User behavior
├── Statistical analysis
├── GPS analysis
├── Plotting code
└── Report generation
```

**Problems**:
- ❌ Hard to find specific functionality
- ❌ Can't reuse functions easily
- ❌ Difficult to test individual parts
- ❌ Large file, slow to load in editor
- ❌ Git diffs are messy

### After (Modular)
```
analysis/
├── config.py (66 lines)
├── data_loader.py (85 lines)
├── temporal_analysis.py (238 lines)
├── spatial_analysis.py (163 lines)
└── utils/
    ├── plotting.py (215 lines)
    └── reporting.py (151 lines)
```

**Advantages**:
- ✅ Easy to find and modify
- ✅ Functions can be imported anywhere
- ✅ Each module testable independently
- ✅ Smaller, focused files
- ✅ Clear git history

## Adding New Analyses

To add a new analysis module:

1. **Create new module** in `analysis/`:
```python
# analysis/bike_analysis.py

def analyze_bike_usage(routes):
    """Analyze individual bike usage patterns."""
    # Analysis code here
    return results

def run_bike_analysis(routes, report):
    """Run all bike analyses."""
    print("\\n[Bike Analysis]")
    results = analyze_bike_usage(routes)
    # Add to report
    return results
```

2. **Add to orchestrator**:
```python
# scripts/02_run_eda.py

from analysis.bike_analysis import run_bike_analysis

# In main script
bike_results = run_bike_analysis(routes, report)
all_results['bike'] = bike_results
```

3. **Use utilities**:
```python
from analysis.utils import plotting, reporting

# Create visualizations
fig = plotting.create_bar_chart(data, title, xlabel, ylabel)
filepath = plotting.save_figure(fig, 'bike_usage.png', 'statistical')

# Add to report
report.add_section("Bike Analysis")
report.add_stat("Total bikes", total)
```

## Configuration

All configuration in one place (`config.py`):

```python
# Modify paths
VIZ_DIR = os.path.join(BASE_DIR, 'my_visualizations')

# Change plot settings
PLOT_DPI = 600  # Higher resolution
PLOT_STYLE = 'ggplot'  # Different style

# Adjust colors
COLORS = {
    'primary': 'blue',
    'secondary': 'red',
    # ...
}
```

## Best Practices

1. **Keep modules focused** - Each should do one thing well
2. **Use descriptive names** - Function and variable names should be clear
3. **Document functions** - Docstrings for all public functions
4. **Return structured data** - Tuples or dicts, not mixed
5. **Separate data from visualization** - Analysis returns data, plotting creates visuals
6. **Use configuration** - Don't hardcode paths or settings

## Future Extensions

Easy to add:
- `user_behavior.py` - User behavior analysis
- `statistical_analysis.py` - Advanced statistics
- `gps_analysis.py` - GPS trajectory analysis
- `machine_learning.py` - ML models

Each as a separate, focused module!

---

**Architecture**: Modular, maintainable, scalable
**Total Code**: ~920 lines across 8 modules
**Avg Module Size**: ~115 lines (highly focused)
