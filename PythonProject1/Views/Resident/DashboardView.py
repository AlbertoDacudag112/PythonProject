from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from Views.Common import StyledWidgets


class DashboardView(QWidget):
    """Dashboard page view - displays statistics and charts"""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header = QLabel("Dashboard")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        self.layout.addWidget(header)

        # Statistics cards container
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        self.layout.addLayout(self.stats_layout)

        # Chart section
        chart_label = QLabel("Monthly Violations")
        chart_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        chart_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(chart_label)

        # Chart container (will hold matplotlib canvas)
        self.chart_container = QVBoxLayout()
        self.layout.addLayout(self.chart_container, 1)

    def update_statistics(self, stats: dict):
        """Update statistics cards"""
        # Clear existing cards
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create new cards
        total_card = StyledWidgets.create_stat_card(
            "Total Violations",
            str(stats['total_violations']),
            "#e8bb41",
            "📊"
        )
        unpaid_card = StyledWidgets.create_stat_card(
            "Unpaid Violations",
            str(stats['unpaid_violations']),
            "#f44336",
            "💰"
        )
        paid_card = StyledWidgets.create_stat_card(
            "Paid Violations",
            str(stats['paid_violations']),
            "#4caf50",
            "✓"
        )

        self.stats_layout.addWidget(total_card)
        self.stats_layout.addWidget(unpaid_card)
        self.stats_layout.addWidget(paid_card)

    def update_chart(self, chart_widget):
        """Update chart display"""
        # Clear existing chart
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new chart
        self.chart_container.addWidget(chart_widget)