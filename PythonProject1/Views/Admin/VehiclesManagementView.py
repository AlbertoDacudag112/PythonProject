from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from Views.Common.StyledWidgets import StyledWidgets
class VehiclesManagementView(QWidget):
    """Vehicles management view for admin"""

    # Signals
    search_changed = pyqtSignal(str)
    add_vehicle_requested = pyqtSignal()
    edit_vehicle_requested = pyqtSignal(str)  # vehicle_id

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header with action button
        header_layout = QHBoxLayout()

        header = QLabel("Vehicles Management")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")

        add_vehicle_btn = StyledWidgets.create_action_button("➕ Register Vehicle", "#4caf50")
        add_vehicle_btn.clicked.connect(lambda: self.add_vehicle_requested.emit())

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(add_vehicle_btn)

        layout.addLayout(header_layout)

        # Search bar
        self.vehicles_search = StyledWidgets.create_search_input("🔍 Search vehicles...")
        self.vehicles_search.textChanged.connect(lambda text: self.search_changed.emit(text))
        layout.addWidget(self.vehicles_search)

        # Vehicles table
        self.vehicles_table = QTableWidget()
        self.vehicles_table.setColumnCount(7)
        self.vehicles_table.setHorizontalHeaderLabels([
            "Vehicle ID", "Plate No", "Owner", "Brand", "Model",
            "Violations", "Actions"
        ])

        StyledWidgets.style_table(self.vehicles_table)

        layout.addWidget(self.vehicles_table)

    def populate_table(self, vehicles: list):
        """Populate table with vehicle data"""
        self.vehicles_table.setRowCount(len(vehicles))

        for row, vehicle in enumerate(vehicles):
            # Vehicle ID
            id_item = QTableWidgetItem(vehicle['VehicleID'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 0, id_item)

            # Plate No
            plate_item = QTableWidgetItem(vehicle['PlateNo'])
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 1, plate_item)

            # Owner
            owner_item = QTableWidgetItem(vehicle['owner_name'])
            owner_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 2, owner_item)

            # Brand
            brand_item = QTableWidgetItem(vehicle['Brand'])
            brand_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 3, brand_item)

            # Model
            model_item = QTableWidgetItem(vehicle['Model'])
            model_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 4, model_item)

            # Violations
            violations_item = QTableWidgetItem(str(vehicle['violations']))
            violations_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vehicles_table.setItem(row, 5, violations_item)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)

            edit_btn = QPushButton("✏ Edit")
            edit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #ffa726;
                }
            """)
            edit_btn.clicked.connect(
                lambda checked, v_id=vehicle['VehicleID']: self.edit_vehicle_requested.emit(v_id)
            )

            action_layout.addWidget(edit_btn)
            action_layout.addStretch()

            self.vehicles_table.setCellWidget(row, 6, action_widget)