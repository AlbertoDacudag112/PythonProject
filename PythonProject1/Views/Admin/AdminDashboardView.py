"""
Views/Admin/AdminDashboardView.py
Admin dashboard page content (extracted from DashboardPage.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Views.Common.StyledWidgets import StyledWidgets


class AdminDashboardView(QWidget):
    """Admin dashboard page view - displays statistics and charts"""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # Header
        header = QLabel("Admin Dashboard")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        self.layout.addWidget(header)

        # Statistics cards row 1
        self.stats_layout1 = QHBoxLayout()
        self.stats_layout1.setSpacing(15)
        self.layout.addLayout(self.stats_layout1)

        # Statistics cards row 2
        self.stats_layout2 = QHBoxLayout()
        self.stats_layout2.setSpacing(15)
        self.layout.addLayout(self.stats_layout2)

        # Chart section
        chart_label = QLabel("Monthly Violations Overview")
        chart_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        chart_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(chart_label)

        # Chart container (will hold matplotlib canvas)
        self.chart_container = QVBoxLayout()
        self.layout.addLayout(self.chart_container, 1)

    def update_statistics(self, stats: dict):
        """
        Update statistics cards
        Expected stats keys:
        - total_violations
        - paid_violations
        - unpaid_violations
        - total_revenue
        - total_residents
        - total_vehicles
        """
        # Clear existing cards
        self._clear_layout(self.stats_layout1)
        self._clear_layout(self.stats_layout2)

        # Create stat cards - Row 1
        total_card = StyledWidgets.create_stat_card(
            "Total Violations",
            str(stats.get('total_violations', 0)),
            "#e8bb41",
            "🚨"
        )
        paid_card = StyledWidgets.create_stat_card(
            "Paid Violations",
            str(stats.get('paid_violations', 0)),
            "#4caf50",
            "✓"
        )
        unpaid_card = StyledWidgets.create_stat_card(
            "Unpaid Violations",
            str(stats.get('unpaid_violations', 0)),
            "#f44336",
            "💰"
        )

        self.stats_layout1.addWidget(total_card)
        self.stats_layout1.addWidget(paid_card)
        self.stats_layout1.addWidget(unpaid_card)

        # Create stat cards - Row 2
        residents_card = StyledWidgets.create_stat_card(
            "Total Residents",
            str(stats.get('total_residents', 0)),
            "#2196f3",
            "👥"
        )
        vehicles_card = StyledWidgets.create_stat_card(
            "Total Vehicles",
            str(stats.get('total_vehicles', 0)),
            "#9c27b0",
            "🚗"
        )
        revenue_card = StyledWidgets.create_stat_card(
            "Total Revenue",
            f"₱{stats.get('total_revenue', 0):,.2f}",
            "#ff9800",
            "💵"
        )

        self.stats_layout2.addWidget(residents_card)
        self.stats_layout2.addWidget(vehicles_card)
        self.stats_layout2.addWidget(revenue_card)

    def update_chart(self, chart_widget):
        """Update chart display"""
        # Clear existing chart
        self._clear_layout(self.chart_container)

        # Add new chart
        self.chart_container.addWidget(chart_widget)

    def _clear_layout(self, layout):
        """Clear all widgets from layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())