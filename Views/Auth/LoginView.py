"""
Views/Auth/LoginView.py
Login window - UI only (extracted from RoadEyeMain.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Controllers.Utility.ResourceHelper import ResourceHelper


class LoginView(QMainWindow):
    """Login window view - Pure UI, no business logic"""

    # Signals for controller communication
    login_requested = pyqtSignal(str, str)  # username, password
    signup_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RoadEye - Vehicle Violation Monitoring System")
        self.setFixedSize(450, 620)
        self.setStyleSheet("background-color: #2d2d2d;")

        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 15, 20, 15)
        self.main_layout.setSpacing(0)

        # Create login container
        self.create_login_container()

    def create_login_container(self):
        """Create the main login form container"""
        # Main container frame
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: #454953;
                border-radius: 15px;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(20)

        # Logo/Title Section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        # Logo Image using ResourceHelper
        logo_label = QLabel()
        logo_pixmap = ResourceHelper.load_pixmap("RoadEyeLogo.png", 80, 80)

        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
        else:
            # Fallback to emoji if logo not found
            logo_label.setText("🚗")
            logo_label.setFont(QFont("Segoe UI", 36))
            print("Warning: RoadEyeLogo.png not found. Using emoji fallback.")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")

        # Title
        self.title = QLabel("RoadEye")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #e8bb41; background: transparent;")

        # Subtitle
        self.subtitle = QLabel("Vehicle Violation Monitoring System")
        self.subtitle.setFont(QFont("Segoe UI", 10))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet("color: #ffffff; background: transparent;")

        title_layout.addWidget(logo_label)
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)

        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #ffffff; background: transparent;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Segoe UI", 11))
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
                background-color: #2d2d2d;
            }
        """)

        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #ffffff; background: transparent;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
                background-color: #2d2d2d;
            }
        """)
        self.password_input.returnPressed.connect(self._handle_login)

        # Login button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #e8bb41;
                color: #2d2d2d;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0c855;
            }
            QPushButton:pressed {
                background-color: #d4a838;
            }
        """)
        self.login_button.clicked.connect(self._handle_login)

        # Sign up link
        signup_link_layout = QHBoxLayout()
        signup_link_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        signup_text = QLabel("No account?")
        signup_text.setFont(QFont("Segoe UI", 9))
        signup_text.setStyleSheet("color: #cccccc; background: transparent;")

        signup_link_btn = QPushButton("Sign up here")
        signup_link_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        signup_link_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        signup_link_btn.setFlat(True)
        signup_link_btn.setStyleSheet("""
            QPushButton {
                color: #e8bb41;
                background: transparent;
                border: none;
                text-decoration: underline;
                padding: 0px;
            }
            QPushButton:hover {
                color: #f0c855;
            }
        """)
        signup_link_btn.clicked.connect(lambda: self.signup_requested.emit())

        signup_link_layout.addWidget(signup_text)
        signup_link_layout.addWidget(signup_link_btn)

        # Add widgets to container
        container_layout.addLayout(title_layout)
        container_layout.addSpacing(15)
        container_layout.addWidget(username_label)
        container_layout.addWidget(self.username_input)
        container_layout.addWidget(password_label)
        container_layout.addWidget(self.password_input)
        container_layout.addSpacing(8)
        container_layout.addWidget(self.login_button)
        container_layout.addSpacing(12)
        container_layout.addLayout(signup_link_layout)
        container_layout.addStretch()

        # Add container to parent
        self.main_layout.addWidget(self.container)

    def _handle_login(self):
        """Emit login signal with credentials"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        self.login_requested.emit(username, password)

    def clear_password(self):
        """Clear password field (called after failed login)"""
        self.password_input.clear()

    def show_error(self, message: str):
        """Display error message"""
        QMessageBox.warning(self, "Login Failed", message)

    def show_info(self, title: str, message: str):
        """Display info message"""
        QMessageBox.information(self, title, message)