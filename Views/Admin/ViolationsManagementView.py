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

        add_violation_btn = StyledWidgets.create_action_button("Add Violation")
        add_violation_btn.clicked.connect(lambda: self.add_violation_requested.emit())

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(add_violation_btn)

        layout.addLayout(header_layout)

        # Search and filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        self.violations_search = StyledWidgets.create_search_input("Search violations...")
        self.violations_search.textChanged.connect(lambda text: self.search_changed.emit(text))

        refresh_btn = StyledWidgets.create_action_button("Refresh")
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

        # Set column resize modes
        header_widget = self.violations_table.horizontalHeader()
        header_widget.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.violations_table.setColumnWidth(7, 100)

        # Lock row height
        v_header = self.violations_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        v_header.setDefaultSectionSize(50)

        # Enable sorting
        self.violations_table.setSortingEnabled(True)

        layout.addWidget(self.violations_table)

    def populate_table(self, violations: list):
        """Populate table with violation data"""
        # Disable sorting while populating
        self.violations_table.setSortingEnabled(False)

        self.violations_table.setRowCount(len(violations))

        for row, violation in enumerate(violations):
            # Violation ID
            id_item = QTableWidgetItem(str(violation.get('ViolationID', '')))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.violations_table.setItem(row, 0, id_item)

            # Resident Name
            resident_name = str(violation.get('resident_name', 'Unknown'))
            resident_item = QTableWidgetItem(resident_name)
            resident_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            resident_item.setFlags(resident_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.violations_table.setItem(row, 1, resident_item)

            # Vehicle Plate
            plate_item = QTableWidgetItem(str(violation.get('PlateNo', '')))
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            plate_item.setFlags(plate_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.violations_table.setItem(row, 2, plate_item)

            # Violation Type
            type_item = QTableWidgetItem(str(violation.get('ViolationName', '')))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.violations_table.setItem(row, 3, type_item)

            # Date
            date_item = QTableWidgetItem(str(violation.get('date', '')))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.violations_table.setItem(row, 4, date_item)

            # Fine Amount
            fine_amount = violation.get('FineAmount', 0)
            try:
                fine_amount = float(fine_amount)
            except (ValueError, TypeError):
                fine_amount = 0.0
            amount_item = QTableWidgetItem(f"₱{fine_amount:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            amount_item.setFlags(amount_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            amount_item.setData(Qt.ItemDataRole.UserRole, fine_amount)
            self.violations_table.setItem(row, 5, amount_item)

            # Status with color
            status = str(violation.get('status', 'UNPAID'))
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if status == 'PAID':
                status_item.setForeground(QColor("#4caf50"))
            else:
                status_item.setForeground(QColor("#f44336"))
            self.violations_table.setItem(row, 6, status_item)

            # Action button - fits inside cell
            view_btn = QPushButton("View")
            view_btn.setToolTip("View Details")
            view_btn.setFixedHeight(32)
            view_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            view_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            view_btn.setStyleSheet("""
                QPushButton {
                    padding: 6px 10px;
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #42a5f5;
                }
                QPushButton:pressed {
                    background-color: #1976d2;
                }
            """)
            view_btn.clicked.connect(
                lambda checked, v_id=str(violation.get('ViolationID', '')): self.view_violation_requested.emit(v_id)
            )

            self.violations_table.setCellWidget(row, 7, view_btn)

        # Re-enable sorting after population
        self.violations_table.setSortingEnabled(True)