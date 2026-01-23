from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class EditVehicleDialog(QDialog):
    """Dialog for editing vehicle details - UI only"""

    # Signal
    vehicle_updated = pyqtSignal(dict)  # form_data

    def __init__(self, vehicle_data: dict, parent=None):
        super().__init__(parent)
        self.vehicle_data = vehicle_data
        self.setWindowTitle("Edit Vehicle")
        self.setFixedSize(500, 550)
        self.setStyleSheet("background-color: #2d2d2d;")
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Edit Vehicle")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Vehicle ID (read-only)
        self.vehicle_id_label = QLabel(self.vehicle_data['VehicleID'])
        self.vehicle_id_label.setStyleSheet("color: #999999; font-size: 11pt; padding: 10px;")
        form_layout.addRow(self._create_label("Vehicle ID:"), self.vehicle_id_label)

        # Owner (read-only)
        self.owner_label = QLabel(self.vehicle_data['owner_name'])
        self.owner_label.setStyleSheet("color: #999999; font-size: 11pt; padding: 10px;")
        form_layout.addRow(self._create_label("Owner:"), self.owner_label)

        # Plate Number (read-only)
        self.plate_label = QLabel(self.vehicle_data['PlateNo'])
        self.plate_label.setStyleSheet("color: #999999; font-size: 11pt; padding: 10px;")
        form_layout.addRow(self._create_label("Plate Number:"), self.plate_label)

        # Brand
        self.brand_edit = QLineEdit()
        self.brand_edit.setText(self.vehicle_data['Brand'])
        self.brand_edit.setPlaceholderText("Enter vehicle brand")
        self._style_input(self.brand_edit)
        form_layout.addRow(self._create_label("Brand:"), self.brand_edit)

        # Model
        self.model_edit = QLineEdit()
        self.model_edit.setText(self.vehicle_data['Model'])
        self.model_edit.setPlaceholderText("Enter vehicle model")
        self._style_input(self.model_edit)
        form_layout.addRow(self._create_label("Model:"), self.model_edit)

        # Color
        self.color_edit = QLineEdit()
        self.color_edit.setText(self.vehicle_data.get('Color', ''))
        self.color_edit.setPlaceholderText("Enter vehicle color")
        self._style_input(self.color_edit)
        form_layout.addRow(self._create_label("Color:"), self.color_edit)

        layout.addLayout(form_layout)

        # Note
        note = QLabel("Note: Plate number cannot be changed after registration")
        note.setStyleSheet("color: #ff9800; font-size: 9pt; font-style: italic;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note)

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

        save_btn = QPushButton("Save Changes")
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

    def _create_label(self, text: str):
        """Create styled label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 11))
        label.setStyleSheet("color: #ffffff;")
        return label

    def _style_input(self, widget):
        """Style input field"""
        widget.setMinimumHeight(40)
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
            }
        """)

    def _handle_submit(self):
        """Emit update signal"""
        form_data = {
            'vehicle_id': self.vehicle_data['VehicleID'],
            'brand': self.brand_edit.text().strip(),
            'model': self.model_edit.text().strip(),
            'color': self.color_edit.text().strip()
        }
        self.vehicle_updated.emit(form_data)

    def show_error(self, message: str):
        """Show error message"""
        QMessageBox.warning(self, "Validation Error", message)