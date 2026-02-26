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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)

        logo_label = QLabel()
        logo_pixmap = ResourceHelper.load_pixmap("RoadEyeLogo.png", 60, 60)

        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🚗")
            logo_label.setFont(QFont("Segoe UI", 28))
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
        # Username
        layout.addWidget(self._field_label("Username *"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username (min. 4 characters)")
        self._style_input(self.username_input)
        layout.addWidget(self.username_input)
        self.username_error = QLabel()
        self.username_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.username_error.hide()
        layout.addWidget(self.username_error)

        # Password
        layout.addWidget(self._field_label("Password *"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password (min. 8 characters)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.password_input)
        layout.addWidget(self.password_input)
        self.password_error = QLabel()
        self.password_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.password_error.hide()
        layout.addWidget(self.password_error)

        # Confirm Password
        layout.addWidget(self._field_label("Confirm Password *"))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.confirm_password_input)
        layout.addWidget(self.confirm_password_input)
        self.confirm_password_error = QLabel()
        self.confirm_password_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.confirm_password_error.hide()
        layout.addWidget(self.confirm_password_error)

        # First Name
        layout.addWidget(self._field_label("First Name *"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        self._style_input(self.first_name_input)
        layout.addWidget(self.first_name_input)
        self.first_name_error = QLabel()
        self.first_name_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.first_name_error.hide()
        layout.addWidget(self.first_name_error)

        # Middle Name (optional)
        layout.addWidget(self._field_label("Middle Name (optional)"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Enter middle name (optional)")
        self._style_input(self.middle_name_input)
        layout.addWidget(self.middle_name_input)

        # Last Name
        layout.addWidget(self._field_label("Last Name *"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        self._style_input(self.last_name_input)
        layout.addWidget(self.last_name_input)
        self.last_name_error = QLabel()
        self.last_name_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.last_name_error.hide()
        layout.addWidget(self.last_name_error)

        # Sex
        layout.addWidget(self._field_label("Sex *"))
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
        layout.addWidget(self.sex_combo)

        # Contact Number
        layout.addWidget(self._field_label("Contact Number *"))
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact number (e.g., 09123456789)")
        self._style_input(self.contact_input)
        layout.addWidget(self.contact_input)
        self.contact_error = QLabel()
        self.contact_error.setStyleSheet("color: #f44336; font-size: 9pt;")
        self.contact_error.hide()
        layout.addWidget(self.contact_error)

        # Address (optional)
        layout.addWidget(self._field_label("Address (optional)"))
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
        layout.addWidget(self.address_input)

    def _field_label(self, text: str) -> QLabel:
        """Create a styled field label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        label.setStyleSheet("color: #ffffff;")
        return label

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

    def _clear_all_errors(self):
        """Hide all error labels"""
        for label in [
            self.username_error, self.password_error,
            self.confirm_password_error, self.first_name_error,
            self.last_name_error, self.contact_error
        ]:
            label.hide()

    def _validate(self) -> bool:
        """Validate all fields and show inline errors. Returns True if all valid."""
        self._clear_all_errors()
        valid = True

        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        contact = self.contact_input.text().strip()

        if not username:
            self.show_error('username', 'Username is required.')
            valid = False
        elif len(username) < 4:
            self.show_error('username', 'Username must be at least 4 characters.')
            valid = False

        if not password:
            self.show_error('password', 'Password is required.')
            valid = False
        elif len(password) < 8:
            self.show_error('password', 'Password must be at least 8 characters.')
            valid = False

        if not confirm:
            self.show_error('confirm_password', 'Please confirm your password.')
            valid = False
        elif password and confirm != password:
            self.show_error('confirm_password', 'Passwords do not match.')
            valid = False

        if not first_name:
            self.show_error('first_name', 'First name is required.')
            valid = False

        if not last_name:
            self.show_error('last_name', 'Last name is required.')
            valid = False

        if not contact:
            self.show_error('contact', 'Contact number is required.')
            valid = False
        elif not contact.startswith('09') or len(contact) != 11 or not contact.isdigit():
            self.show_error('contact', 'Contact number must be 11 digits starting with 09.')
            valid = False

        return valid

    def _handle_signup(self):
        """Validate then emit signup signal with form data"""
        if not self._validate():
            return

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