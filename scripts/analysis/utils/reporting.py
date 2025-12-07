"""
Reporting Utilities
===================

Functions for generating analysis reports.
"""

from datetime import datetime


class MarkdownReport:
    """Class for building markdown reports."""

    def __init__(self, title):
        """
        Initialize report.

        Args:
            title (str): Report title
        """
        self.lines = []
        self.add_title(title)
        self.add_line(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.add_separator()

    def add_title(self, title, level=1):
        """Add a title."""
        self.lines.append(f"{'#' * level} {title}\n")

    def add_section(self, title, level=2):
        """Add a section header."""
        self.lines.append(f"\n{'#' * level} {title}\n")

    def add_subsection(self, title, level=3):
        """Add a subsection header."""
        self.lines.append(f"\n{'#' * level} {title}\n")

    def add_line(self, text):
        """Add a line of text."""
        self.lines.append(f"{text}\n")

    def add_bullet(self, text):
        """Add a bullet point."""
        self.lines.append(f"- {text}\n")

    def add_numbered(self, text, number):
        """Add a numbered item."""
        self.lines.append(f"{number}. {text}\n")

    def add_separator(self):
        """Add a horizontal line."""
        self.lines.append("---\n")

    def add_code_block(self, text):
        """Add a code block."""
        self.lines.append("```\n")
        self.lines.append(f"{text}\n")
        self.lines.append("```\n")

    def add_table(self, dataframe, caption=None):
        """
        Add a pandas DataFrame as a table.

        Args:
            dataframe: Pandas DataFrame
            caption (str): Optional table caption
        """
        if caption:
            self.add_line(f"**{caption}**\n")

        self.add_code_block(dataframe.to_string())

    def add_stat(self, label, value, unit=''):
        """
        Add a statistic line.

        Args:
            label (str): Statistic label
            value: Statistic value
            unit (str): Unit of measurement
        """
        if isinstance(value, float):
            formatted_value = f"{value:,.2f}"
        elif isinstance(value, int):
            formatted_value = f"{value:,}"
        else:
            formatted_value = str(value)

        if unit:
            self.add_bullet(f"**{label}**: {formatted_value} {unit}")
        else:
            self.add_bullet(f"**{label}**: {formatted_value}")

    def get_content(self):
        """Get report content as string."""
        return '\n'.join(self.lines)

    def save(self, filepath):
        """
        Save report to file.

        Args:
            filepath (str): Output file path
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.get_content())

        return filepath


def format_number(value, decimals=2):
    """
    Format a number for display.

    Args:
        value: Number to format
        decimals (int): Decimal places

    Returns:
        str: Formatted number
    """
    if isinstance(value, float):
        return f"{value:,.{decimals}f}"
    elif isinstance(value, int):
        return f"{value:,}"
    else:
        return str(value)


def create_summary_dict(routes_df):
    """
    Create a summary dictionary from routes data.

    Args:
        routes_df (pd.DataFrame): Routes dataframe

    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_trips': len(routes_df),
        'avg_duration': routes_df['duration_minutes_calculated'].mean(),
        'median_duration': routes_df['duration_minutes_calculated'].median(),
        'avg_distance': routes_df['length'].mean(),
        'median_distance': routes_df['length'].median(),
        'total_bikes': routes_df['cyclenumber'].nunique(),
        'total_stations': routes_df['startstationname'].nunique(),
        'total_memberships': routes_df['Membership'].nunique()
    }

    return summary
