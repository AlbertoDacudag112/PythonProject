"""
Views/Admin/AdminDashboardView.py
Admin dashboard page content with year filter (extracted from DashboardPage.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Controllers.Utility.ResourceHelper import ResourceHelper


class AdminDashboardView(QWidget):
    """Admin dashboard page view - displays statistics and charts with year filter"""

    # Signal emitted when year filter changes
    year_filter_changed = pyqtSignal(int)  # Emits the selected year

    def __init__(self):
        super().__init__()
        self.current_year = QDate.currentDate().year()
        self._setup_ui()

    # ------------------------------------------------------------------
    # card factory
    # ------------------------------------------------------------------
    @staticmethod
    def _create_stat_card(title: str, value: str) -> QWidget:
        card = QWidget()
        card.setMinimumHeight(140)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 12px;
                border: 1px solid #3d3d3d;
                border-top: 4px solid #e8bb41;
            }
            QWidget:hover {
                background-color: #333333;
                border: 1px solid #e8bb41;
                border-top: 4px solid #e8bb41;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        # --- value (big number) ---
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #ffffff; border: none; background: transparent;")
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

        # Header container with title and filter
        header_container = QWidget()
        header_container.setStyleSheet("background-color: transparent;")
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(20)

        # Header title
        header = QLabel("Admin Dashboard")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Year filter section
        filter_container = self._create_year_filter()
        header_layout.addWidget(filter_container)

        self.layout.addWidget(header_container)

        # Statistics cards container
        stats_container = QWidget()
        stats_container.setStyleSheet("background-color: transparent;")
        self.stats_grid = QGridLayout(stats_container)
        self.stats_grid.setSpacing(20)
        self.stats_grid.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(stats_container)

        # Chart section
        chart_label = QLabel("Monthly Violations Overview")
        chart_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        chart_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(chart_label)

        # Chart container (will hold matplotlib canvas)
        self.chart_container = QVBoxLayout()
        self.layout.addLayout(self.chart_container, 1)

    def _create_year_filter(self) -> QWidget:
        """Create year filter dropdown with custom styling"""
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)

        # Filter label
        filter_label = QLabel("Year:")
        filter_label.setFont(QFont("Segoe UI", 12))
        filter_label.setStyleSheet("color: #ffffff;")
        container_layout.addWidget(filter_label)

        # Year dropdown
        self.year_combo = QComboBox()
        self.year_combo.setFixedWidth(120)
        self.year_combo.setFixedHeight(40)

        # Populate years (current year and previous 5 years)
        current_year = QDate.currentDate().year()
        years = [str(year) for year in range(current_year, current_year - 6, -1)]
        self.year_combo.addItems(years)

        # Style the combobox with custom arrow icon
        self.year_combo.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                padding: 8px 35px 8px 15px;
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
            }
            QComboBox:hover {
                background-color: #333333;
                border: 1px solid #e8bb41;
            }
            QComboBox:focus {
                border: 1px solid #e8bb41;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(/mnt/user-data/uploads/down-chevron.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                border: 1px solid #e8bb41;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
                color: #ffffff;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px;
                min-height: 30px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #3a3a3a;
            }
        """)

        # Connect signal
        self.year_combo.currentTextChanged.connect(self._on_year_changed)

        container_layout.addWidget(self.year_combo)

        return container

    def _on_year_changed(self, year_text: str):
        """Handle year filter change"""
        if year_text:
            try:
                year = int(year_text)
                self.current_year = year
                self.year_filter_changed.emit(year)
            except ValueError:
                pass

    # ------------------------------------------------------------------
    # public update helpers
    # ------------------------------------------------------------------
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
        self._clear_grid_layout(self.stats_grid)

        # Row 0
        self.stats_grid.addWidget(self._create_stat_card("Total Violations",  str(stats.get("total_violations", 0))),  0, 0)
        self.stats_grid.addWidget(self._create_stat_card("Paid Violations",   str(stats.get("paid_violations", 0))),   0, 1)
        self.stats_grid.addWidget(self._create_stat_card("Unpaid Violations", str(stats.get("unpaid_violations", 0))), 0, 2)

        # Row 1
        self.stats_grid.addWidget(self._create_stat_card("Total Residents", str(stats.get("total_residents", 0))),            1, 0)
        self.stats_grid.addWidget(self._create_stat_card("Total Vehicles",  str(stats.get("total_vehicles", 0))),             1, 1)
        self.stats_grid.addWidget(self._create_stat_card("Total Revenue",   f"₱{stats.get('total_revenue', 0):,.2f}"),       1, 2)

        for col in range(3):
            self.stats_grid.setColumnStretch(col, 1)

    def update_chart(self, chart_widget):
        """Update chart display"""
        self._clear_layout(self.chart_container)
        self.chart_container.addWidget(chart_widget)

    def get_selected_year(self) -> int:
        """Get the currently selected year"""
        return self.current_year

    def set_year(self, year: int):
        """Programmatically set the year filter"""
        year_str = str(year)
        index = self.year_combo.findText(year_str)
        if index >= 0:
            self.year_combo.setCurrentIndex(index)

    # ------------------------------------------------------------------
    # layout helpers
    # ------------------------------------------------------------------
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_grid_layout(self, grid_layout):
        while grid_layout.count():
            item = grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()