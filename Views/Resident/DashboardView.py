from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy

from Views.Common.StyledWidgets import StyledWidgets


class DashboardView(QWidget):
    """Dashboard page view - displays statistics and charts"""

    # Accent colors for each card: (top border, number text, card background)
    CARD_STYLES = {
        "total":  ("#e8bb41", "#ffffff", "#2a2a2a"),   # gold  — matches dashboard title
        "unpaid": ("#e8bb41", "#ffffff", "#2a2a2a"),   # red   — draws attention to unpaid
        "paid":   ("#e8bb41", "#ffffff", "#2a2a2a"),   # green — positive / completed
    }

    def __init__(self):
        super().__init__()
        self._setup_ui()

    # ------------------------------------------------------------------
    # card factory
    # ------------------------------------------------------------------
    @staticmethod
    def _create_stat_card(title: str, value: str, style_key: str) -> QWidget:
        border_color, number_color, bg_color = DashboardView.CARD_STYLES[style_key]

        card = QWidget()
        card.setMinimumHeight(140)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 12px;
                border: 1px solid #3d3d3d;
                border-top: 4px solid {border_color};
            }}
            QWidget:hover {{
                background-color: #333333;
                border: 1px solid {border_color};
                border-top: 4px solid {border_color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        layout.setAlignment(card.layout().alignment())

        # --- value (big number) ---
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {number_color}; border: none; background: transparent;")
        layout.addWidget(value_label)

        # --- title label ---
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12))
        title_label.setStyleSheet("color: #aaaaaa; border: none; background: transparent;")
        layout.addWidget(title_label)

        layout.addStretch()
        return card

    # ------------------------------------------------------------------
    # UI setup
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # public update helpers
    # ------------------------------------------------------------------
    def update_statistics(self, stats: dict):
        """Update statistics cards"""
        # Clear existing cards
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total_card  = self._create_stat_card("Total Violations",  str(stats["total_violations"]),  "total")
        unpaid_card = self._create_stat_card("Unpaid Violations", str(stats["unpaid_violations"]), "unpaid")
        paid_card   = self._create_stat_card("Paid Violations",   str(stats["paid_violations"]),   "paid")

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