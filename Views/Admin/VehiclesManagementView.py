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
    view_vehicle_requested = pyqtSignal(str)  # vehicle_id

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

        add_vehicle_btn = StyledWidgets.create_action_button("Register Vehicle")
        add_vehicle_btn.clicked.connect(lambda: self.add_vehicle_requested.emit())

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(add_vehicle_btn)

        layout.addLayout(header_layout)

        # Search bar
        self.vehicles_search = StyledWidgets.create_search_input("Search vehicles...")
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

        # Set column resize modes
        header_widget = self.vehicles_table.horizontalHeader()
        header_widget.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header_widget.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_widget.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.vehicles_table.setColumnWidth(6, 170)  # Wide enough for two buttons

        # Lock row height
        v_header = self.vehicles_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        v_header.setDefaultSectionSize(50)

        # Enable sorting
        self.vehicles_table.setSortingEnabled(True)

        layout.addWidget(self.vehicles_table)

    def populate_table(self, vehicles: list):
        """Populate table with vehicle data"""
        # Disable sorting while populating
        self.vehicles_table.setSortingEnabled(False)

        self.vehicles_table.setRowCount(len(vehicles))

        for row, vehicle in enumerate(vehicles):
            # Vehicle ID
            id_item = QTableWidgetItem(str(vehicle.get('VehicleID', '')))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 0, id_item)

            # Plate No
            plate_item = QTableWidgetItem(str(vehicle.get('PlateNo', '')))
            plate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            plate_item.setFlags(plate_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 1, plate_item)

            # Owner
            owner_name = str(vehicle.get('owner_name', 'Unknown'))
            owner_item = QTableWidgetItem(owner_name)
            owner_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            owner_item.setFlags(owner_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 2, owner_item)

            # Brand
            brand_item = QTableWidgetItem(str(vehicle.get('Brand', '')))
            brand_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            brand_item.setFlags(brand_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 3, brand_item)

            # Model
            model_item = QTableWidgetItem(str(vehicle.get('Model', '')))
            model_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            model_item.setFlags(model_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 4, model_item)

            # Violations
            violations_item = QTableWidgetItem(str(vehicle.get('violations', 0)))
            violations_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            violations_item.setFlags(violations_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vehicles_table.setItem(row, 5, violations_item)

            # Action buttons container
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)

            # View button
            view_btn = QPushButton("View")
            view_btn.setFixedHeight(32)
            view_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            view_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            view_btn.setStyleSheet("""
                QPushButton {
                    padding: 6px 8px;
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
                lambda checked, v_id=str(vehicle.get('VehicleID', '')): self.view_vehicle_requested.emit(v_id)
            )

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setFixedHeight(32)
            edit_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            edit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 6px 8px;
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #ffa726;
                }
                QPushButton:pressed {
                    background-color: #f57c00;
                }
            """)
            edit_btn.clicked.connect(
                lambda checked, v_id=str(vehicle.get('VehicleID', '')): self.edit_vehicle_requested.emit(v_id)
            )

            action_layout.addWidget(view_btn)
            action_layout.addWidget(edit_btn)

            self.vehicles_table.setCellWidget(row, 6, action_widget)

        # Re-enable sorting after population
        self.vehicles_table.setSortingEnabled(True)