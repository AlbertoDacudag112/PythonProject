"""
Utility/ChartGenerator.py
Chart generation utilities (extracted from DashboardPage and ResidentWindow)
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartGenerator:
    """Helper class for generating charts"""

    @staticmethod
    def create_monthly_violations_chart(monthly_data: dict, title: str = "Monthly Violations Overview"):
        """
        Create bar chart for monthly violations using pandas and matplotlib

        Args:
            monthly_data: Dictionary with months as keys and violation counts as values
            title: Chart title

        Returns:
            FigureCanvas widget for PyQt
        """
        # Create DataFrame
        df = pd.DataFrame(list(monthly_data.items()), columns=['Month', 'Violations'])

        # Create matplotlib figure
        fig = Figure(figsize=(10, 5), facecolor='#363636')
        ax = fig.add_subplot(111)

        # Set background color
        ax.set_facecolor('#363636')
        fig.patch.set_facecolor('#363636')

        # Create bar chart
        bars = ax.bar(df['Month'], df['Violations'], color='#e8bb41', edgecolor='#d4a838', linewidth=1.5)

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color='#ffffff', fontweight='bold', fontsize=10)

        # Customize chart
        ax.set_xlabel('Month', color='#ffffff', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Violations', color='#ffffff', fontsize=12, fontweight='bold')
        ax.set_title(title, color='#e8bb41', fontsize=14, fontweight='bold', pad=20)

        # Customize ticks
        ax.tick_params(colors='#ffffff', labelsize=10)
        ax.spines['bottom'].set_color('#5a5a5a')
        ax.spines['top'].set_color('#5a5a5a')
        ax.spines['right'].set_color('#5a5a5a')
        ax.spines['left'].set_color('#5a5a5a')

        # Add grid
        ax.grid(True, alpha=0.2, color='#ffffff', linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)

        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

        # Adjust layout
        fig.tight_layout()

        # Create canvas
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: #363636; border-radius: 12px;")

        return canvas

    @staticmethod
    def create_admin_dashboard_chart(monthly_data: dict):
        """
        Create chart specifically for admin dashboard

        Args:
            monthly_data: Dictionary with months as keys and violation counts as values

        Returns:
            FigureCanvas widget for PyQt
        """
        return ChartGenerator.create_monthly_violations_chart(
            monthly_data,
            title="Monthly Violations - All Residents"
        )

    @staticmethod
    def create_resident_dashboard_chart(monthly_data: dict):
        """
        Create chart specifically for resident dashboard

        Args:
            monthly_data: Dictionary with months as keys and violation counts as values

        Returns:
            FigureCanvas widget for PyQt
        """
        return ChartGenerator.create_monthly_violations_chart(
            monthly_data,
            title="Monthly Violations Overview"
        )