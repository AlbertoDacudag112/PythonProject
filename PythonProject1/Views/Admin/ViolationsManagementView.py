"""
Views/Admin/ViolationsManagementView.py
Violations management page (extracted from ViolationsPage.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Views.Common.StyledWidgets import StyledWidgets


class ViolationsManagementView(QWidget):
    """Violations management view for admin"""

    # Signals
    search_changed = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    add_violation_requested = pyqtSignal()
    view_violation_requested = pyqtSignal(str)  # violation_id

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header with action buttons
        header_layout = QHBoxLayout()

        header = QLabel("Violations Management")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")

        add_violation_btn = StyledWidgets.create_action_button("➕ Add Violation", "#4caf50")
        add_violation_btn.clicked.connect(lambda: self.add_violation_requested.emit())

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(add_violation_btn)

        layout.addLayout(header_layout)

        # Search and filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        self.violations_search = StyledWidgets.create_search_input("🔍 Search violations...")
        self.violations_search.textChanged.connect(lambda text: self.search_changed.emit(text))

        refresh_btn = StyledWidgets.create_action_button("🔄 Refresh", "#2196f3")
        refresh_btn.clicked.connect(lambda: self.refresh_requested.emit())

        filter_layout.addWidget(self.violations_search, 1)
        filter_layout.addWidget(refresh_btn)

        layout.addLayout(filter_layout)

        # Violations table
        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(8)
        self.violations_table.setHorizontalHeaderLabels([
            "Violation ID", "Resident Name", "Vehicle Plate", "Violation Type",
            "Date", "Fine Amount", "Status", "Actions"
        ])

        StyledWidgets.style_table(self.violations_table)

        layout.addWidget(self.violations_table)

    def populate_table(self, violations: list):
        """Populate table with violation data"""
        self.violations_table.setRowCount(len(violations))

        for row, violation in enumerate(violations):
            # Violation ID
            id_item = QTableWidgetItem(str(violation['ViolationID']))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 0, id_item)

            # Resident Name
            resident_item = QTableWidgetItem(violation['resident_name'])
            resident_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 1, resident_item)

            # Vehicle Plate
            plate_item = QTableWidgetItem(violation['PlateNo'])
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 2, plate_item)

            # Violation Type
            type_item = QTableWidgetItem(violation['ViolationName'])
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 3, type_item)

            # Date
            date_item = QTableWidgetItem(violation['date'])
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 4, date_item)

            # Fine Amount
            amount_item = QTableWidgetItem(f"₱{violation['FineAmount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.violations_table.setItem(row, 5, amount_item)

            # Status with color
            status_item = QTableWidgetItem(violation['status'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if violation['status'] == 'PAID':
                status_item.setForeground(QColor("#4caf50"))
            else:
                status_item.setForeground(QColor("#f44336"))
            self.violations_table.setItem(row, 6, status_item)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            action_layout.setSpacing(5)

            view_btn = QPushButton("👁 View")
            view_btn.setToolTip("View Details")
            view_btn.setMaximumWidth(80)
            view_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            view_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #42a5f5;
                }
            """)
            view_btn.clicked.connect(
                lambda checked, v_id=violation['ViolationID']: self.view_violation_requested.emit(v_id)
            )

            action_layout.addWidget(view_btn)
            action_layout.addStretch()

            self.violations_table.setCellWidget(row, 7, action_widget)