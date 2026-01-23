"""
Views/Auth/SignUpView.py
Sign up window - UI only (extracted from SignUpWindow.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Controllers.Utility.ResourceHelper import ResourceHelper


class SignUpView(QDialog):
    """Sign up window view - Pure UI, validation handled by controller"""

    # Signals for controller communication
    signup_submitted = pyqtSignal(dict)  # form_data dictionary
    username_changed = pyqtSignal(str)  # for real-time username check

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RoadEye - Sign Up")
        self.setFixedSize(550, 750)
        self.setModal(True)
        self.setStyleSheet("background-color: #2d2d2d;")

        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)

        # Logo using ResourceHelper
        logo_label = QLabel()
        logo_pixmap = ResourceHelper.load_pixmap("RoadEyeLogo.png", 60, 60)

        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🚗")
            logo_label.setFont(QFont("Segoe UI", 28))
            print("Warning: RoadEyeLogo.png not found in SignUpWindow. Using emoji fallback.")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Register as a new resident")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #cccccc;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)

        # Scroll area for form fields
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #3a3a3a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #5a5a5a;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #e8bb41;
            }
        """)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        # Create all form fields
        self._create_form_fields(form_layout)

        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll, 1)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: #999999; font-size: 9pt; font-style: italic;")
        main_layout.addWidget(required_note)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #5a5a5a;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.signup_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.signup_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #e8bb41;
                color: #2d2d2d;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f0c855;
            }
            QPushButton:disabled {
                background-color: #5a5a5a;
                color: #999999;
            }
        """)
        self.signup_btn.clicked.connect(self._handle_signup)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.signup_btn)

        main_layout.addLayout(button_layout)

    def _create_form_fields(self, layout):
        """Create all form input fields"""
        # Username field
        username_label = QLabel("Username *")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #ffffff;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username (min. 4 characters)")
        self._style_input(self.username_input)

        self.username_error = QLabel()
        self.username_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.username_error.hide()

        # Password field
        password_label = QLabel("Password *")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #ffffff;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password (min. 6 characters)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.password_input)

        self.password_error = QLabel()
        self.password_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.password_error.hide()

        # Confirm Password field
        confirm_password_label = QLabel("Confirm Password *")
        confirm_password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        confirm_password_label.setStyleSheet("color: #ffffff;")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.confirm_password_input)

        self.confirm_password_error = QLabel()
        self.confirm_password_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.confirm_password_error.hide()

        # First Name field
        first_name_label = QLabel("First Name *")
        first_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        first_name_label.setStyleSheet("color: #ffffff;")

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        self._style_input(self.first_name_input)

        self.first_name_error = QLabel()
        self.first_name_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.first_name_error.hide()

        # Middle Name field (optional)
        middle_name_label = QLabel("Middle Name")
        middle_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        middle_name_label.setStyleSheet("color: #ffffff;")

        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Enter middle name (optional)")
        self._style_input(self.middle_name_input)

        # Last Name field
        last_name_label = QLabel("Last Name *")
        last_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        last_name_label.setStyleSheet("color: #ffffff;")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        self._style_input(self.last_name_input)

        self.last_name_error = QLabel()
        self.last_name_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.last_name_error.hide()

        # Sex field
        sex_label = QLabel("Sex *")
        sex_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        sex_label.setStyleSheet("color: #ffffff;")

        self.sex_combo = QComboBox()
        self.sex_combo.addItems(["Male", "Female"])
        self.sex_combo.setFont(QFont("Segoe UI", 11))
        self.sex_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
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

        # Contact Number field
        contact_label = QLabel("Contact Number *")
        contact_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        contact_label.setStyleSheet("color: #ffffff;")

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact number (e.g., 09123456789)")
        self._style_input(self.contact_input)

        self.contact_error = QLabel()
        self.contact_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.contact_error.hide()

        # Address field
        address_label = QLabel("Address")
        address_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        address_label.setStyleSheet("color: #ffffff;")

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter complete address (optional)")
        self.address_input.setMaximumHeight(80)
        self.address_input.setFont(QFont("Segoe UI", 11))
        self.address_input.setStyleSheet("""
            QTextEdit {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QTextEdit:focus {
                border: 2px solid #e8bb41;
            }
        """)

        # Add all fields to layout
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.username_error)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_error)

        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.confirm_password_error)

        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.first_name_error)

        layout.addWidget(middle_name_label)
        layout.addWidget(self.middle_name_input)

        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.last_name_error)

        layout.addWidget(sex_label)
        layout.addWidget(self.sex_combo)

        layout.addWidget(contact_label)
        layout.addWidget(self.contact_input)
        layout.addWidget(self.contact_error)

        layout.addWidget(address_label)
        layout.addWidget(self.address_input)

    def _style_input(self, widget):
        """Apply consistent styling to input fields"""
        widget.setFont(QFont("Segoe UI", 11))
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
            }
        """)

    def _handle_signup(self):
        """Emit signup signal with form data"""
        form_data = {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text(),
            'confirm_password': self.confirm_password_input.text(),
            'first_name': self.first_name_input.text().strip(),
            'middle_name': self.middle_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'sex': self.sex_combo.currentText(),
            'contact_no': self.contact_input.text().strip(),
            'address': self.address_input.toPlainText().strip()
        }
        self.signup_submitted.emit(form_data)

    def show_error(self, field: str, message: str):
        """Show validation error for specific field"""
        error_labels = {
            'username': self.username_error,
            'password': self.password_error,
            'confirm_password': self.confirm_password_error,
            'first_name': self.first_name_error,
            'last_name': self.last_name_error,
            'contact': self.contact_error
        }

        if field in error_labels:
            error_labels[field].setText(message)
            error_labels[field].show()

    def clear_error(self, field: str):
        """Clear validation error for specific field"""
        error_labels = {
            'username': self.username_error,
            'password': self.password_error,
            'confirm_password': self.confirm_password_error,
            'first_name': self.first_name_error,
            'last_name': self.last_name_error,
            'contact': self.contact_error
        }

        if field in error_labels:
            error_labels[field].hide()

    def show_message(self, title: str, message: str, is_error: bool = False):
        """Show message dialog"""
        if is_error:
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)