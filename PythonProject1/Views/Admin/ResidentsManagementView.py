from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Views.Common.StyledWidgets import StyledWidgets


class ResidentsManagementView(QWidget):
    """Residents management view for admin"""

    # Signals
    search_changed = pyqtSignal(str)
    view_resident_requested = pyqtSignal(str)  # resident_id

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Residents Management")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Search bar
        self.residents_search = StyledWidgets.create_search_input("🔍 Search residents...")
        self.residents_search.textChanged.connect(lambda text: self.search_changed.emit(text))
        layout.addWidget(self.residents_search)

        # Residents table
        self.residents_table = QTableWidget()
        self.residents_table.setColumnCount(7)
        self.residents_table.setHorizontalHeaderLabels([
            "Resident ID", "Full Name", "Sex", "Contact No",
            "Address", "Total Violations", "Actions"
        ])

        StyledWidgets.style_table(self.residents_table)

        layout.addWidget(self.residents_table)

    def populate_table(self, residents: list):
        """Populate table with resident data"""
        self.residents_table.setRowCount(len(residents))

        for row, resident in enumerate(residents):
            # Resident ID
            id_item = QTableWidgetItem(resident['ResidentID'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 0, id_item)

            # Full Name
            name_item = QTableWidgetItem(resident['full_name'])
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 1, name_item)

            # Sex
            sex_item = QTableWidgetItem(resident['Sex'])
            sex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 2, sex_item)

            # Contact No
            contact_item = QTableWidgetItem(resident['ContactNo'])
            contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 3, contact_item)

            # Address
            address_item = QTableWidgetItem(resident['Address'] or 'N/A')
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 4, address_item)

            # Total Violations
            violations_item = QTableWidgetItem(str(resident['total_violations']))
            violations_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.residents_table.setItem(row, 5, violations_item)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)

            view_btn = QPushButton("👁 View")
            view_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            view_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #42a5f5;
                }
            """)
            view_btn.clicked.connect(
                lambda checked, r_id=resident['ResidentID']: self.view_resident_requested.emit(r_id)
            )

            action_layout.addWidget(view_btn)
            action_layout.addStretch()

            self.residents_table.setCellWidget(row, 6, action_widget)