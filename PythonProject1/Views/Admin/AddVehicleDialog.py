from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AddVehicleDialog(QDialog):
    """Dialog for registering new vehicles - UI only"""

    # Signal
    vehicle_submitted = pyqtSignal(dict)  # form_data

    def __init__(self, residents_list: list, parent=None):
        super().__init__(parent)
        self.residents_list = residents_list
        self.setWindowTitle("Register New Vehicle")
        self.setFixedSize(500, 550)
        self.setStyleSheet("background-color: #2d2d2d;")
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Register New Vehicle")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Owner selection
        self.owner_combo = QComboBox()
        self._style_combo(self.owner_combo)
        self._populate_owners()
        form_layout.addRow(self._create_label("Owner:"), self.owner_combo)

        # Plate Number
        self.plate_edit = QLineEdit()
        self.plate_edit.setPlaceholderText("Enter plate number (e.g., ABC1234)")
        self._style_input(self.plate_edit)
        form_layout.addRow(self._create_label("Plate Number:"), self.plate_edit)

        # Brand
        self.brand_edit = QLineEdit()
        self.brand_edit.setPlaceholderText("Enter vehicle brand (e.g., Toyota)")
        self._style_input(self.brand_edit)
        form_layout.addRow(self._create_label("Brand:"), self.brand_edit)

        # Model
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("Enter vehicle model (e.g., Camry)")
        self._style_input(self.model_edit)
        form_layout.addRow(self._create_label("Model:"), self.model_edit)

        # Color
        self.color_edit = QLineEdit()
        self.color_edit.setPlaceholderText("Enter vehicle color")
        self._style_input(self.color_edit)
        form_layout.addRow(self._create_label("Color:"), self.color_edit)

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

        save_btn = QPushButton("Register Vehicle")
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

    def _populate_owners(self):
        """Populate owner dropdown"""
        self.owner_combo.clear()
        for resident in self.residents_list:
            self.owner_combo.addItem(resident['full_name'], resident['ResidentID'])

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
        """)

    def _handle_submit(self):
        """Emit submission signal"""
        form_data = {
            'resident_id': self.owner_combo.currentData(),
            'plate_no': self.plate_edit.text().strip(),
            'brand': self.brand_edit.text().strip(),
            'model': self.model_edit.text().strip(),
            'color': self.color_edit.text().strip()
        }
        self.vehicle_submitted.emit(form_data)

    def show_error(self, message: str):
        """Show error message"""
        QMessageBox.warning(self, "Validation Error", message)