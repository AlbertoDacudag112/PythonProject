"""
Utility/ChartGenerator.py
Chart generation utilities
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class ChartGenerator:
    """Helper class for generating charts"""

    @staticmethod
    def create_monthly_violations_chart(
            monthly_data: dict,
            title: str = "Monthly Violations Overview"
    ):
        # Create DataFrame
        df = pd.DataFrame(
            list(monthly_data.items()),
            columns=["Month", "Violations"]
        )

        # Create matplotlib figure (slightly taller)
        fig = Figure(figsize=(12, 6.5), facecolor="#363636")
        ax = fig.add_subplot(111)

        # Background colors
        ax.set_facecolor("#363636")
        fig.patch.set_facecolor("#363636")

        # Bar chart
        bars = ax.bar(
            df["Month"],
            df["Violations"],
            color="#e8bb41",
            edgecolor="#d4a838",
            linewidth=1.5
        )

        # Value labels
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    str(int(height)),
                    ha="center",
                    va="bottom",
                    color="#ffffff",
                    fontweight="bold",
                    fontsize=10
                )

        # Labels and title
        ax.set_xlabel(
            "Month",
            color="#ffffff",
            fontsize=13,
            fontweight="bold",
            labelpad=14
        )
        ax.set_ylabel(
            "Number of Violations",
            color="#ffffff",
            fontsize=13,
            fontweight="bold",
            labelpad=14
        )
        if title:
            ax.set_title(
                title,
                color="#e8bb41",
                fontsize=16,
                fontweight="bold",
                pad=18
            )
        # Ticks and spines
        ax.tick_params(colors="#ffffff", labelsize=11)
        plt.setp(ax.get_xticklabels(), rotation=0)

        for spine in ax.spines.values():
            spine.set_color("#5a5a5a")

        # Grid
        ax.grid(
            True,
            alpha=0.2,
            color="#ffffff",
            linestyle="--",
            linewidth=0.5
        )
        ax.set_axisbelow(True)

        # 🔥 FIX FOR CLIPPED MONTH LABEL
        fig.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.88,
        bottom=0.22)

        # Canvas for PyQt6
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet(
            "background-color: #363636; border-radius: 12px;"
        )

        return canvas

    @staticmethod
    def create_admin_dashboard_chart(monthly_data: dict):
        return ChartGenerator.create_monthly_violations_chart(
            monthly_data,
            title=""
        )

    @staticmethod
    def create_resident_dashboard_chart(monthly_data: dict):
        return ChartGenerator.create_monthly_violations_chart(
            monthly_data,
            title=""
        )
