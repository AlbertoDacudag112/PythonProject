from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QTableWidget, QHeaderView, \
    QTableWidgetItem, QPushButton

from Views.Common import StyledWidgets


class ViolationsView(QWidget):
    """Violations table view"""

    # Signals
    search_changed = pyqtSignal(str)
    filter_changed = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    payment_requested = pyqtSignal(dict)  # violation data

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("My Violations")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Search and filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        # Search bar
        self.search_input = StyledWidgets.create_search_input(
            "🔍 Search by Violation ID, Vehicle Plate, or Type..."
        )
        self.search_input.textChanged.connect(lambda text: self.search_changed.emit(text))

        # Status filter
        status_label = QLabel("Status:")
        status_label.setFont(QFont("Segoe UI", 11))
        status_label.setStyleSheet("color: #ffffff;")

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Paid", "Unpaid"])
        self.status_filter.setFont(QFont("Segoe UI", 11))
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #e8bb41;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
                border: 1px solid #5a5a5a;
            }
        """)
        self.status_filter.currentTextChanged.connect(lambda text: self.filter_changed.emit(text))

        # Refresh button
        refresh_btn = StyledWidgets.create_action_button("🔄 Refresh", "#4caf50")
        refresh_btn.clicked.connect(lambda: self.refresh_requested.emit())

        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(refresh_btn)

        layout.addLayout(filter_layout)

        # Violations table
        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(7)
        self.violations_table.setHorizontalHeaderLabels([
            "Violation ID", "Vehicle Plate", "Violation Type",
            "Date", "Fine Amount", "Status", "Action"
        ])

        StyledWidgets.style_table(self.violations_table)

        # Set last column to fixed width for action buttons
        header = self.violations_table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.violations_table.setColumnWidth(6, 130)

        layout.addWidget(self.violations_table)

    def populate_table(self, violations: list):
        """Populate table with violation data"""
        self.violations_table.setRowCount(len(violations))

        for row, violation in enumerate(violations):
            # Violation ID
            id_item = QTableWidgetItem(violation['violation_id'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 0, id_item)

            # Vehicle Plate
            plate_item = QTableWidgetItem(violation['plate_no'])
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 1, plate_item)

            # Violation Type
            type_item = QTableWidgetItem(violation['violation_type'])
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 2, type_item)

            # Date
            date_item = QTableWidgetItem(violation['date'])
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 3, date_item)

            # Fine Amount
            amount_item = QTableWidgetItem(f"₱{violation['fine_amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 4, amount_item)

            # Status
            status_item = QTableWidgetItem(violation['status'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if violation['status'] == 'Paid':
                status_item.setForeground(QColor("#4caf50"))
            else:
                status_item.setForeground(QColor("#f44336"))
            self.violations_table.setItem(row, 5, status_item)

            # Action button
            if violation['status'] == 'Unpaid':
                pay_btn = QPushButton("💳 Pay")
                pay_btn.setFixedSize(90, 32)
                pay_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                pay_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e8bb41;
                        color: #1e1e1e;
                        border-radius: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #f0c855;
                    }
                    QPushButton:pressed {
                        background-color: #d4a838;
                    }
                """)
                pay_btn.clicked.connect(lambda checked, v=violation: self.payment_requested.emit(v))

                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.addWidget(pay_btn)
                container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.setContentsMargins(5, 5, 5, 5)
                self.violations_table.setCellWidget(row, 6, container)
            else:
                paid_label = QLabel("✓ Paid")
                paid_label.setFixedSize(90, 32)
                paid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                paid_label.setStyleSheet("""
                    QLabel {
                        background-color: #2e7d32;
                        color: #ffffff;
                        border-radius: 16px;
                        font-weight: bold;
                    }
                """)

                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.addWidget(paid_label)
                container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_layout.setContentsMargins(5, 5, 5, 5)
                self.violations_table.setCellWidget(row, 6, container)