from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QComboBox, QDateEdit, QHBoxLayout, QPushButton, \
    QMessageBox


class AddViolationDialog(QDialog):
    """Dialog for adding new violations - UI only"""

    # Signal
    violation_submitted = pyqtSignal(dict)  # form_data

    def __init__(self, vehicles_list: list, violation_types_list: list, parent=None):
        super().__init__(parent)
        self.vehicles_list = vehicles_list
        self.violation_types_list = violation_types_list
        self.setWindowTitle("Add New Violation")
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #2d2d2d;")
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Add New Violation")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Vehicle selection
        self.vehicle_combo = QComboBox()
        self._style_combo(self.vehicle_combo)
        self._populate_vehicles()
        form_layout.addRow(self._create_label("Vehicle:"), self.vehicle_combo)

        # Violation Type selection
        self.violation_type_combo = QComboBox()
        self._style_combo(self.violation_type_combo)
        self._populate_violation_types()
        form_layout.addRow(self._create_label("Violation Type:"), self.violation_type_combo)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self._style_date(self.date_edit)
        form_layout.addRow(self._create_label("Date:"), self.date_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #f44336;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ef5350;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Add Violation")
        save_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #66bb6a;
            }
        """)
        save_btn.clicked.connect(self._handle_submit)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addStretch()
        layout.addLayout(button_layout)

    def _populate_vehicles(self):
        """Populate vehicles dropdown - FIXED to handle various owner name fields"""
        self.vehicle_combo.clear()

        if not self.vehicles_list:
            self.vehicle_combo.addItem("No vehicles available", None)
            return

        for vehicle in self.vehicles_list:
            # Try multiple possible field names for owner
            owner_name = (
                    vehicle.get('owner_name') or
                    vehicle.get('OwnerName') or
                    vehicle.get('resident_name') or
                    vehicle.get('full_name') or
                    f"{vehicle.get('RFirstName', '')} {vehicle.get('RLastName', '')}".strip() or
                    'Unknown Owner'
            )

            plate_no = vehicle.get('PlateNo', 'N/A')
            vehicle_id = vehicle.get('VehicleID')

            # Debug print to see what data we're getting
            print(f"Vehicle data: PlateNo={plate_no}, Owner={owner_name}, VehicleID={vehicle_id}")

            display_text = f"{plate_no} - {owner_name}"
            self.vehicle_combo.addItem(display_text, vehicle_id)

    def _populate_violation_types(self):
        """Populate violation types dropdown"""
        self.violation_type_combo.clear()

        if not self.violation_types_list:
            self.violation_type_combo.addItem("No violation types available", None)
            return

        for vtype in self.violation_types_list:
            violation_name = vtype.get('ViolationName', 'Unknown')
            fine_amount = vtype.get('FineAmount', 0)
            violation_type_id = vtype.get('ViolationTypeID')

            try:
                fine_amount = float(fine_amount)
            except (ValueError, TypeError):
                fine_amount = 0.0

            display_text = f"{violation_name} - ₱{fine_amount:.2f}"
            self.violation_type_combo.addItem(display_text, violation_type_id)

    def _create_label(self, text: str):
        """Create styled label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 11))
        label.setStyleSheet("color: #ffffff;")
        return label

    def _style_combo(self, widget):
        """Style combo box"""
        widget.setMinimumHeight(40)
        widget.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                font-size: 11pt;
            }
            QComboBox:focus {
                border: 2px solid #e8bb41;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
                border: 1px solid #5a5a5a;
            }
        """)

    def _style_date(self, widget):
        """Style date edit"""
        widget.setMinimumHeight(40)
        widget.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                font-size: 11pt;
            }
            QDateEdit:focus {
                border: 2px solid #e8bb41;
            }
            QDateEdit::drop-down {
                border: none;
            }
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 10px;
            }
        """)

    def _handle_submit(self):
        """Emit submission signal"""
        vehicle_id = self.vehicle_combo.currentData()
        violation_type_id = self.violation_type_combo.currentData()

        # Validation
        if not vehicle_id:
            self.show_error("Please select a vehicle")
            return

        if not violation_type_id:
            self.show_error("Please select a violation type")
            return

        form_data = {
            'vehicle_id': vehicle_id,
            'violation_type_id': violation_type_id,
            'violation_date': self.date_edit.date().toString("yyyy-MM-dd")
        }

        print(f"Submitting violation: {form_data}")
        self.violation_submitted.emit(form_data)

    def show_error(self, message: str):
        """Show error message"""
        QMessageBox.warning(self, "Validation Error", message)