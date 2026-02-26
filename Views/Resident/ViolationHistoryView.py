import os

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QTableWidget, QHeaderView, \
    QTableWidgetItem

from Views.Common.StyledWidgets import StyledWidgets

# Resolve the icon path once at module level
CHEVRON_ICON = os.path.join(
    os.path.dirname(__file__), "..", "..", "Controllers", "Icons", "down-chevron.png"
).replace("\\", "/")


class ViolationHistoryView(QWidget):
    """Violation history table view - displays all violations including paid ones"""

    # Signals
    search_changed = pyqtSignal(str)
    year_filter_changed = pyqtSignal(str)
    status_filter_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Violation History")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        # Search bar
        self.search_input = StyledWidgets.create_search_input(
            "Search by Violation ID, Vehicle Plate, or Type..."
        )
        self.search_input.textChanged.connect(lambda text: self.search_changed.emit(text))

        # Shared combobox stylesheet using the chevron icon
        combobox_style = f"""
            QComboBox {{
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                min-width: 150px;
            }}
            QComboBox:focus {{
                border: 2px solid #e8bb41;
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: url({CHEVRON_ICON});
                width: 14px;
                height: 14px;
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
                border: 1px solid #5a5a5a;
            }}
        """

        # Year filter
        year_label = QLabel("Year:")
        year_label.setFont(QFont("Segoe UI", 11))
        year_label.setStyleSheet("color: #ffffff;")

        self.year_filter = QComboBox()
        self.year_filter.addItems(["All Years", "2026", "2025", "2024", "2023", "2022"])
        self.year_filter.setFont(QFont("Segoe UI", 11))
        self.year_filter.setStyleSheet(combobox_style)
        self.year_filter.currentTextChanged.connect(lambda text: self.year_filter_changed.emit(text))

        # Status filter
        status_label = QLabel("Status:")
        status_label.setFont(QFont("Segoe UI", 11))
        status_label.setStyleSheet("color: #ffffff;")

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Paid", "Unpaid"])
        self.status_filter.setFont(QFont("Segoe UI", 11))
        self.status_filter.setStyleSheet(combobox_style)
        self.status_filter.currentTextChanged.connect(lambda text: self.status_filter_changed.emit(text))

        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter)

        layout.addLayout(filter_layout)

        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "Violation ID", "Date", "Vehicle Plate", "Violation Type",
            "Fine Amount", "Status", "Payment Date"
        ])

        StyledWidgets.style_table(self.history_table)

        # Set column resize modes
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Violation ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Vehicle Plate
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Violation Type
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Fine Amount
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Payment Date

        # Enable selection and interaction
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Enable sorting
        self.history_table.setSortingEnabled(True)

        layout.addWidget(self.history_table)

    def populate_table(self, violations: list):
        """Populate table with violation history data"""
        # Disable sorting while populating
        self.history_table.setSortingEnabled(False)

        self.history_table.setRowCount(len(violations))

        for row, violation in enumerate(violations):
            # Violation ID
            id_item = QTableWidgetItem(str(violation.get('violation_id', '')))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.history_table.setItem(row, 0, id_item)

            # Date
            date_item = QTableWidgetItem(str(violation.get('date', '')))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.history_table.setItem(row, 1, date_item)

            # Vehicle Plate
            plate_item = QTableWidgetItem(str(violation.get('plate_no', '')))
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            plate_item.setFlags(plate_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.history_table.setItem(row, 2, plate_item)

            # Violation Type
            type_item = QTableWidgetItem(str(violation.get('violation_type', '')))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.history_table.setItem(row, 3, type_item)

            # Fine Amount
            fine_amount = violation.get('fine_amount', 0)
            try:
                fine_amount = float(fine_amount)
            except (ValueError, TypeError):
                fine_amount = 0.0
            amount_item = QTableWidgetItem(f"₱{fine_amount:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            amount_item.setFlags(amount_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            # Store numeric value for sorting
            amount_item.setData(Qt.ItemDataRole.UserRole, fine_amount)
            self.history_table.setItem(row, 4, amount_item)

            # Status
            status = str(violation.get('status', 'Unknown'))
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if status == 'Paid':
                status_item.setForeground(QColor("#4caf50"))
            elif status == 'Unpaid':
                status_item.setForeground(QColor("#f44336"))
            self.history_table.setItem(row, 5, status_item)

            # Payment Date
            payment_date = violation.get('payment_date', 'N/A')
            if not payment_date or payment_date == '':
                payment_date = 'N/A'
            payment_date_item = QTableWidgetItem(str(payment_date))
            payment_date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            payment_date_item.setFlags(payment_date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if payment_date == 'N/A':
                payment_date_item.setForeground(QColor("#757575"))
            self.history_table.setItem(row, 6, payment_date_item)

        # Re-enable sorting after population
        self.history_table.setSortingEnabled(True)