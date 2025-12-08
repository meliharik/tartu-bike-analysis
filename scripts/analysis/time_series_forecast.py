"""
Time Series Forecasting
========================

Demand forecasting using Prophet and SARIMA models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("  ⚠ Prophet not available, using SARIMA only")

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
from . import config
from .utils import plotting


def prepare_time_series_data(routes):
    """
    Prepare hourly time series data for forecasting.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        pd.DataFrame: Hourly aggregated data
    """
    # Create hourly aggregation
    routes['hour_timestamp'] = routes['unlock_datetime'].dt.floor('H')

    hourly_data = routes.groupby('hour_timestamp').agg({
        'route_code': 'count',
        'duration_minutes_calculated': 'mean',
        'length': 'mean'
    }).reset_index()

    hourly_data.columns = ['ds', 'y', 'avg_duration', 'avg_distance']

    # Fill missing hours with 0
    full_range = pd.date_range(
        start=hourly_data['ds'].min(),
        end=hourly_data['ds'].max(),
        freq='H'
    )

    hourly_data = hourly_data.set_index('ds').reindex(full_range, fill_value=0).reset_index()
    hourly_data.columns = ['ds', 'y', 'avg_duration', 'avg_distance']

    return hourly_data


def forecast_with_prophet(hourly_data, periods=168):
    """
    Forecast demand using Facebook Prophet.

    Args:
        hourly_data (pd.DataFrame): Hourly time series data
        periods (int): Number of hours to forecast ahead (default 168 = 1 week)

    Returns:
        tuple: (model, forecast, metrics)
    """
    if not PROPHET_AVAILABLE:
        return None, None, None, None, None

    # Prepare data for Prophet
    df_prophet = hourly_data[['ds', 'y']].copy()

    # Train-test split (last 24 hours for testing)
    train_size = len(df_prophet) - 24
    train_data = df_prophet[:train_size]
    test_data = df_prophet[train_size:]

    # Initialize and fit model
    try:
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05
        )

        model.fit(train_data)
    except (AttributeError, Exception) as e:
        print(f"  ⚠ Prophet initialization failed: {e}")
        return None, None, None, None, None

    # Make predictions on test set
    test_forecast = model.predict(test_data[['ds']])

    # Calculate metrics
    y_true = test_data['y'].values
    y_pred = test_forecast['yhat'].values

    metrics = {
        'mae': mean_absolute_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score(y_true, y_pred),
        'mape': np.mean(np.abs((y_true - y_pred) / (y_true + 1))) * 100
    }

    # Future forecast
    future = model.make_future_dataframe(periods=periods, freq='H')
    forecast = model.predict(future)

    return model, forecast, metrics, test_data, test_forecast


def forecast_with_sarima(hourly_data, order=(1,1,1), seasonal_order=(1,1,1,24)):
    """
    Forecast demand using SARIMA model.

    Args:
        hourly_data (pd.DataFrame): Hourly time series data
        order (tuple): ARIMA order (p,d,q)
        seasonal_order (tuple): Seasonal order (P,D,Q,s)

    Returns:
        tuple: (model, forecast, metrics)
    """
    # Prepare data
    ts_data = hourly_data.set_index('ds')['y']

    # Train-test split
    train_size = len(ts_data) - 24
    train_data = ts_data[:train_size]
    test_data = ts_data[train_size:]

    # Fit SARIMA model
    try:
        model = SARIMAX(
            train_data,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fitted_model = model.fit(disp=False, maxiter=200)

        # Forecast
        forecast_steps = len(test_data) + 168  # Test period + 1 week ahead
        forecast = fitted_model.forecast(steps=forecast_steps)

        # Calculate metrics on test set
        test_forecast = forecast[:len(test_data)]

        metrics = {
            'mae': mean_absolute_error(test_data, test_forecast),
            'rmse': np.sqrt(mean_squared_error(test_data, test_forecast)),
            'r2': r2_score(test_data, test_forecast),
            'mape': np.mean(np.abs((test_data - test_forecast) / (test_data + 1))) * 100,
            'aic': fitted_model.aic,
            'bic': fitted_model.bic
        }

        return fitted_model, forecast, metrics, test_data

    except Exception as e:
        print(f"  ⚠ SARIMA model failed: {e}")
        return None, None, None, None


def perform_seasonal_decomposition(hourly_data):
    """
    Decompose time series into trend, seasonal, and residual components.

    Args:
        hourly_data (pd.DataFrame): Hourly time series data

    Returns:
        statsmodels.DecomposeResult: Decomposition result
    """
    ts_data = hourly_data.set_index('ds')['y']

    # Perform decomposition
    decomposition = seasonal_decompose(
        ts_data,
        model='additive',
        period=24,  # Daily seasonality
        extrapolate_trend='freq'
    )

    return decomposition


def visualize_forecasts(hourly_data, prophet_forecast, sarima_forecast,
                       prophet_metrics, sarima_metrics, test_data):
    """
    Create comprehensive forecast visualizations.

    Args:
        hourly_data (pd.DataFrame): Original hourly data
        prophet_forecast (pd.DataFrame): Prophet predictions
        sarima_forecast (pd.Series): SARIMA predictions
        prophet_metrics (dict): Prophet evaluation metrics
        sarima_metrics (dict): SARIMA evaluation metrics
        test_data (pd.DataFrame): Test dataset

    Returns:
        list: Visualization file paths
    """
    filepaths = []

    # Figure 1: Prophet Forecast
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot actual data
    ax.plot(hourly_data['ds'], hourly_data['y'],
            'k.', alpha=0.5, label='Actual', markersize=3)

    # Plot forecast
    ax.plot(prophet_forecast['ds'], prophet_forecast['yhat'],
            'b-', label='Prophet Forecast', linewidth=2)

    # Plot confidence interval
    ax.fill_between(prophet_forecast['ds'],
                     prophet_forecast['yhat_lower'],
                     prophet_forecast['yhat_upper'],
                     alpha=0.2, color='blue', label='95% Confidence')

    # Highlight test period
    if test_data is not None:
        ax.axvspan(test_data['ds'].iloc[0], test_data['ds'].iloc[-1],
                   alpha=0.1, color='red', label='Test Period')

    ax.set_title('Hourly Bike Demand Forecast - Prophet Model',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Timestamp', fontsize=12)
    ax.set_ylabel('Number of Trips', fontsize=12)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add metrics text
    metrics_text = f"MAE: {prophet_metrics['mae']:.2f} | RMSE: {prophet_metrics['rmse']:.2f} | R²: {prophet_metrics['r2']:.3f} | MAPE: {prophet_metrics['mape']:.2f}%"
    ax.text(0.5, 0.02, metrics_text, transform=ax.transAxes,
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'prophet_forecast.png', 'statistical')
    filepaths.append(filepath)
    plt.close()

    # Figure 2: Model Comparison (if SARIMA available)
    if sarima_forecast is not None and sarima_metrics is not None:
        fig, axes = plt.subplots(2, 1, figsize=(16, 12))

        # Prophet
        axes[0].plot(hourly_data['ds'], hourly_data['y'],
                    'k.', alpha=0.5, label='Actual', markersize=2)
        axes[0].plot(prophet_forecast['ds'], prophet_forecast['yhat'],
                    'b-', label='Prophet', linewidth=2)
        axes[0].set_title('Prophet Model Forecast', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Number of Trips', fontsize=10)
        axes[0].legend(loc='upper left')
        axes[0].grid(True, alpha=0.3)

        # Add Prophet metrics
        prophet_text = f"MAE: {prophet_metrics['mae']:.2f} | RMSE: {prophet_metrics['rmse']:.2f} | R²: {prophet_metrics['r2']:.3f}"
        axes[0].text(0.98, 0.95, prophet_text, transform=axes[0].transAxes,
                    ha='right', va='top', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        # SARIMA
        sarima_dates = pd.date_range(
            start=test_data.index[0],
            periods=len(sarima_forecast),
            freq='H'
        )

        axes[1].plot(hourly_data['ds'], hourly_data['y'],
                    'k.', alpha=0.5, label='Actual', markersize=2)
        axes[1].plot(sarima_dates, sarima_forecast,
                    'r-', label='SARIMA', linewidth=2)
        axes[1].set_title('SARIMA Model Forecast', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Timestamp', fontsize=10)
        axes[1].set_ylabel('Number of Trips', fontsize=10)
        axes[1].legend(loc='upper left')
        axes[1].grid(True, alpha=0.3)

        # Add SARIMA metrics
        sarima_text = f"MAE: {sarima_metrics['mae']:.2f} | RMSE: {sarima_metrics['rmse']:.2f} | AIC: {sarima_metrics['aic']:.0f}"
        axes[1].text(0.98, 0.95, sarima_text, transform=axes[1].transAxes,
                    ha='right', va='top', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

        plt.tight_layout()
        filepath = plotting.save_figure(fig, 'forecast_comparison.png', 'statistical')
        filepaths.append(filepath)
        plt.close()

    # Figure 3: Forecast Components (Prophet)
    fig = plt.figure(figsize=(16, 12))

    # Trend
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(prophet_forecast['ds'], prophet_forecast['trend'], 'g-', linewidth=2)
    ax1.set_title('Trend Component', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Trend', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Daily seasonality
    ax2 = plt.subplot(3, 1, 2)
    ax2.plot(prophet_forecast['ds'], prophet_forecast['daily'], 'b-', linewidth=2)
    ax2.set_title('Daily Seasonality', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Daily Effect', fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Weekly seasonality
    ax3 = plt.subplot(3, 1, 3)
    ax3.plot(prophet_forecast['ds'], prophet_forecast['weekly'], 'r-', linewidth=2)
    ax3.set_title('Weekly Seasonality', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Timestamp', fontsize=10)
    ax3.set_ylabel('Weekly Effect', fontsize=10)
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'forecast_components.png', 'statistical')
    filepaths.append(filepath)
    plt.close()

    return filepaths


def visualize_seasonal_decomposition(decomposition):
    """
    Visualize seasonal decomposition.

    Args:
        decomposition: Decomposition result

    Returns:
        str: Visualization file path
    """
    fig, axes = plt.subplots(4, 1, figsize=(16, 12))

    # Observed
    decomposition.observed.plot(ax=axes[0], color='black', linewidth=1)
    axes[0].set_title('Observed', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Trips', fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Trend
    decomposition.trend.plot(ax=axes[1], color='green', linewidth=2)
    axes[1].set_title('Trend', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Trips', fontsize=10)
    axes[1].grid(True, alpha=0.3)

    # Seasonal
    decomposition.seasonal.plot(ax=axes[2], color='blue', linewidth=1)
    axes[2].set_title('Seasonal (Daily Pattern)', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Trips', fontsize=10)
    axes[2].grid(True, alpha=0.3)

    # Residual
    decomposition.resid.plot(ax=axes[3], color='red', linewidth=1, alpha=0.7)
    axes[3].set_title('Residual', fontsize=12, fontweight='bold')
    axes[3].set_xlabel('Timestamp', fontsize=10)
    axes[3].set_ylabel('Trips', fontsize=10)
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'seasonal_decomposition.png', 'statistical')
    plt.close()

    return filepath


def run_time_series_forecasting(routes, report):
    """
    Run all time series forecasting analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Forecasting results
    """
    print("\n[Time Series Forecasting]")
    print("-" * 80)

    results = {}

    # Prepare data
    print("  • Preparing hourly time series data...")
    hourly_data = prepare_time_series_data(routes)
    results['hourly_data'] = hourly_data

    report.add_section("Time Series Forecasting")
    report.add_line(f"**Total Hours**: {len(hourly_data)}")
    report.add_line(f"**Date Range**: {hourly_data['ds'].min()} to {hourly_data['ds'].max()}")
    report.add_line(f"**Avg Trips/Hour**: {hourly_data['y'].mean():.2f}")
    report.add_line("")

    # Seasonal decomposition
    print("  • Performing seasonal decomposition...")
    decomposition = perform_seasonal_decomposition(hourly_data)
    results['decomposition'] = decomposition

    decomp_viz = visualize_seasonal_decomposition(decomposition)
    results['decomposition_viz'] = decomp_viz

    report.add_subsection("Seasonal Decomposition")
    report.add_line("Time series decomposed into:")
    report.add_line("- **Trend**: Long-term progression")
    report.add_line("- **Seasonal**: Daily cyclical pattern (24-hour)")
    report.add_line("- **Residual**: Random noise")
    report.add_line("")

    # Prophet forecast
    if PROPHET_AVAILABLE:
        print("  • Forecasting with Prophet model...")
        prophet_model, prophet_forecast, prophet_metrics, test_data, test_forecast = forecast_with_prophet(hourly_data, periods=168)

        # Check if Prophet actually worked
        if prophet_model is not None:
            results['prophet'] = {
                'model': prophet_model,
                'forecast': prophet_forecast,
                'metrics': prophet_metrics
            }

            report.add_subsection("Prophet Model Forecast")
            report.add_line(f"**Forecast Horizon**: 168 hours (1 week)")
            report.add_line(f"**MAE**: {prophet_metrics['mae']:.2f} trips")
            report.add_line(f"**RMSE**: {prophet_metrics['rmse']:.2f} trips")
            report.add_line(f"**R² Score**: {prophet_metrics['r2']:.3f}")
            report.add_line(f"**MAPE**: {prophet_metrics['mape']:.2f}%")
            report.add_line("")
        else:
            # Prophet import worked but initialization failed
            results['prophet'] = {
                'model': None,
                'forecast': None,
                'metrics': None
            }
            report.add_subsection("Prophet Model")
            report.add_line("*Prophet initialization failed - may need cmdstan backend*")
            report.add_line("")
    else:
        print("  ⚠ Skipping Prophet forecast (not installed)")
        prophet_model, prophet_forecast, prophet_metrics, test_data, test_forecast = None, None, None, None, None
        results['prophet'] = {
            'model': None,
            'forecast': None,
            'metrics': None
        }
        report.add_subsection("Prophet Model")
        report.add_line("*Prophet not available - install with: pip install prophet*")
        report.add_line("")

    # SARIMA forecast
    print("  • Forecasting with SARIMA model...")
    sarima_model, sarima_forecast, sarima_metrics, sarima_test = forecast_with_sarima(hourly_data)

    if sarima_model is not None:
        results['sarima'] = {
            'model': sarima_model,
            'forecast': sarima_forecast,
            'metrics': sarima_metrics
        }

        report.add_subsection("SARIMA Model Forecast")
        report.add_line(f"**Model Order**: SARIMA(1,1,1)(1,1,1,24)")
        report.add_line(f"**MAE**: {sarima_metrics['mae']:.2f} trips")
        report.add_line(f"**RMSE**: {sarima_metrics['rmse']:.2f} trips")
        report.add_line(f"**AIC**: {sarima_metrics['aic']:.0f}")
        report.add_line(f"**BIC**: {sarima_metrics['bic']:.0f}")
        report.add_line("")
    else:
        report.add_subsection("SARIMA Model")
        report.add_line("*Model fitting was unsuccessful*")
        report.add_line("")

    # Visualizations
    print("  • Creating forecast visualizations...")
    viz_files = []
    if prophet_model is not None and prophet_forecast is not None:
        viz_files = visualize_forecasts(
            hourly_data, prophet_forecast, sarima_forecast,
            prophet_metrics, sarima_metrics, test_data
        )
    results['visualizations'] = viz_files + [decomp_viz]

    # Model comparison
    report.add_subsection("Model Comparison")
    if prophet_model is not None and prophet_metrics is not None and sarima_model is not None:
        best_model = "Prophet" if prophet_metrics['mae'] < sarima_metrics['mae'] else "SARIMA"
        report.add_line(f"**Best Model (by MAE)**: {best_model}")
        report.add_line("")
        report.add_line("| Metric | Prophet | SARIMA |")
        report.add_line("|--------|---------|--------|")
        report.add_line(f"| MAE | {prophet_metrics['mae']:.2f} | {sarima_metrics['mae']:.2f} |")
        report.add_line(f"| RMSE | {prophet_metrics['rmse']:.2f} | {sarima_metrics['rmse']:.2f} |")
        report.add_line(f"| R² | {prophet_metrics['r2']:.3f} | {sarima_metrics['r2']:.3f} |")
    elif prophet_model is not None and prophet_metrics is not None:
        report.add_line("Only Prophet model available for comparison")
    elif sarima_model is not None:
        report.add_line("Only SARIMA model available for comparison")
    else:
        report.add_line("No models available for comparison")
    report.add_line("")

    print(f"  ✓ Time series forecasting complete")
    if prophet_model is not None and prophet_metrics is not None:
        print(f"  ✓ Prophet MAE: {prophet_metrics['mae']:.2f} trips")
    if sarima_metrics is not None:
        print(f"  ✓ SARIMA MAE: {sarima_metrics['mae']:.2f} trips")

    return results
