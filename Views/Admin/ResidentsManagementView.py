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
        self.residents_search = StyledWidgets.create_search_input("Search residents...")
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

        # Set column resize modes
        header_widget = self.residents_table.horizontalHeader()
        header_widget.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.residents_table.setColumnWidth(6, 100)

        # Lock row height
        v_header = self.residents_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        v_header.setDefaultSectionSize(50)

        # Enable sorting
        self.residents_table.setSortingEnabled(True)

        layout.addWidget(self.residents_table)

    def _get_full_name(self, resident: dict) -> str:
        """Build full name from separate fields, falling back to full_name if present"""
        if 'full_name' in resident and resident['full_name']:
            return resident['full_name']
        first = resident.get('first_name', '') or ''
        middle = resident.get('middle_name', '') or ''
        last = resident.get('last_name', '') or ''
        parts = [first, middle, last] if middle else [first, last]
        return ' '.join(p for p in parts if p).strip()

    def populate_table(self, residents: list):
        """Populate table with resident data"""
        self.residents_table.setSortingEnabled(False)
        self.residents_table.setRowCount(len(residents))

        for row, resident in enumerate(residents):
            # Resident ID
            id_item = QTableWidgetItem(str(resident.get('ResidentID', '')))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 0, id_item)

            # Full Name — built from separate fields
            name_item = QTableWidgetItem(self._get_full_name(resident))
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 1, name_item)

            # Sex
            sex_item = QTableWidgetItem(str(resident.get('Sex', '')))
            sex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            sex_item.setFlags(sex_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 2, sex_item)

            # Contact No
            contact_item = QTableWidgetItem(str(resident.get('ContactNo', '')))
            contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            contact_item.setFlags(contact_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 3, contact_item)

            # Address
            address_item = QTableWidgetItem(str(resident.get('Address', 'N/A')))
            address_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            address_item.setFlags(address_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 4, address_item)

            # Total Violations
            violations_item = QTableWidgetItem(str(resident.get('total_violations', 0)))
            violations_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            violations_item.setFlags(violations_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.residents_table.setItem(row, 5, violations_item)

            # Action button
            view_btn = QPushButton("View")
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
                lambda checked, r_id=str(resident.get('ResidentID', '')): self.view_resident_requested.emit(r_id)
            )
            self.residents_table.setCellWidget(row, 6, view_btn)

        self.residents_table.setSortingEnabled(True)