"""
Plotting Utilities
==================

Reusable plotting functions for visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from .. import config


def setup_plot_style():
    """Set up matplotlib and seaborn style."""
    plt.style.use(config.PLOT_STYLE)
    sns.set_palette(config.PLOT_PALETTE)


def save_figure(fig, filename, subdirectory=''):
    """
    Save figure to file.

    Args:
        fig: Matplotlib figure object
        filename (str): Output filename
        subdirectory (str): Subdirectory within visualizations folder
    """
    import os

    if subdirectory:
        output_dir = getattr(config, f'VIZ_{subdirectory.upper()}', config.VIZ_DIR)
    else:
        output_dir = config.VIZ_DIR

    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=config.PLOT_DPI, bbox_inches='tight')
    plt.close(fig)

    return filepath


def create_bar_chart(data, title, xlabel, ylabel, color=None, figsize=(12, 6)):
    """
    Create a standard bar chart.

    Args:
        data: Series or DataFrame for plotting
        title (str): Chart title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        color (str): Bar color
        figsize (tuple): Figure size

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    color = color or config.COLORS['primary']

    data.plot(kind='bar', ax=ax, color=color, edgecolor='black')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


def create_line_chart(data, title, xlabel, ylabel, color=None, figsize=(12, 6)):
    """
    Create a standard line chart.

    Args:
        data: Series for plotting
        title (str): Chart title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        color (str): Line color
        figsize (tuple): Figure size

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    color = color or config.COLORS['primary']

    data.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=6, color=color)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def create_horizontal_bar_chart(data, title, xlabel, figsize=(12, 8)):
    """
    Create a horizontal bar chart (good for long labels).

    Args:
        data: Series for plotting
        title (str): Chart title
        xlabel (str): X-axis label
        figsize (tuple): Figure size

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    data.plot(kind='barh', ax=ax, color=config.COLORS['primary'], edgecolor='black')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    return fig


def create_histogram(data, title, xlabel, ylabel='Frequency', bins=50, color=None, figsize=(10, 6)):
    """
    Create a histogram with mean and median lines.

    Args:
        data: Array-like data
        title (str): Chart title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        bins (int): Number of bins
        color (str): Histogram color
        figsize (tuple): Figure size

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    color = color or config.COLORS['primary']

    ax.hist(data, bins=bins, color=color, edgecolor='black', alpha=0.7)
    ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    ax.axvline(data.median(), color='green', linestyle='--', linewidth=2, label='Median')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    return fig


def create_scatter_plot(x, y, title, xlabel, ylabel, figsize=(10, 8)):
    """
    Create a scatter plot with correlation.

    Args:
        x: X-axis data
        y: Y-axis data
        title (str): Chart title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        figsize (tuple): Figure size

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(x, y, alpha=0.3, s=20, c=config.COLORS['primary'], edgecolors='none')

    # Add correlation
    correlation = x.corr(y)
    ax.text(0.05, 0.95, f'Correlation: {correlation:.3f}',
            transform=ax.transAxes, fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    return fig


def create_heatmap(data, title, figsize=(10, 8), annot=True):
    """
    Create a correlation heatmap.

    Args:
        data: Correlation matrix
        title (str): Chart title
        figsize (tuple): Figure size
        annot (bool): Show annotations

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.heatmap(data, annot=annot, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)

    ax.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig
