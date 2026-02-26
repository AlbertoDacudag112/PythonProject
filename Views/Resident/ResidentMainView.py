from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Controllers.Utility.ResourceHelper import ResourceHelper
from Views.Common.StyledWidgets import StyledWidgets


class ResidentMainView(QMainWindow):
    logout_requested = pyqtSignal()
    page_changed = pyqtSignal(int)

    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data or {}

        self.setWindowTitle("RoadEye - Resident Dashboard")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("background-color: #1e1e1e;")

        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._create_sidebar()
        main_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #2d2d2d;")
        main_layout.addWidget(self.stacked_widget, 1)

    def _create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-right: 1px solid #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # User info with larger logo
        first = self.user_data.get("RFirstName", "")
        last = self.user_data.get("RLastName", "")
        rid = self.user_data.get("ResidentID", "N/A")

        # Create header container with proper spacing
        header_container = QWidget()
        header_container.setStyleSheet("background-color: #252525;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 30, 20, 20)
        header_layout.setSpacing(15)

        # Logo - increased size
        logo_label = QLabel()
        logo = ResourceHelper.load_pixmap("RoadEyeLogo.png", 120, 120)
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedHeight(120)
        header_layout.addWidget(logo_label)

        # App name
        app_name = QLabel("RoadEye")
        app_name.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        app_name.setStyleSheet("color: #e8bb41;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(app_name)

        # User name
        user_name = QLabel(f"{first} {last}".strip())
        user_name.setFont(QFont("Segoe UI", 12))
        user_name.setStyleSheet("color: #ffffff;")
        user_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(user_name)

        # User ID
        user_id = QLabel(f"ID: {rid}")
        user_id.setFont(QFont("Segoe UI", 10))
        user_id.setStyleSheet("color: #999999;")
        user_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(user_id)

        layout.addWidget(header_container)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #3a3a3a;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Navigation buttons
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(10, 20, 10, 10)
        nav_layout.setSpacing(8)

        self.dashboard_btn = StyledWidgets.create_nav_button("Dashboard", True)
        self.violations_btn = StyledWidgets.create_nav_button("My Violations")
        self.violation_history_btn = StyledWidgets.create_nav_button("Violation History")
        self.payment_history_btn = StyledWidgets.create_nav_button("Payment History")

        self.dashboard_btn.clicked.connect(lambda: self._on_nav_clicked(0, self.dashboard_btn))
        self.violations_btn.clicked.connect(lambda: self._on_nav_clicked(1, self.violations_btn))
        self.violation_history_btn.clicked.connect(lambda: self._on_nav_clicked(2, self.violation_history_btn))
        self.payment_history_btn.clicked.connect(lambda: self._on_nav_clicked(3, self.payment_history_btn))

        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.violations_btn)
        nav_layout.addWidget(self.violation_history_btn)
        nav_layout.addWidget(self.payment_history_btn)
        nav_layout.addStretch()

        layout.addWidget(nav_container, 1)

        # Logout button at bottom
        logout_btn = StyledWidgets.create_logout_button()
        logout_btn.clicked.connect(self._handle_logout)
        layout.addWidget(logout_btn)

        self._update_nav_buttons(self.dashboard_btn)

    def _on_nav_clicked(self, index: int, button: QPushButton):
        if index >= self.stacked_widget.count():
            return

        self._update_nav_buttons(button)
        self.page_changed.emit(index)
        self.stacked_widget.setCurrentIndex(index)

    def _update_nav_buttons(self, active_btn: QPushButton):
        buttons = [self.dashboard_btn, self.violations_btn, self.violation_history_btn, self.payment_history_btn]

        for btn in buttons:
            is_active = btn is active_btn
            btn.setChecked(is_active)

            if is_active:
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 15px 20px;
                        background-color: #e8bb41;
                        color: #1e1e1e;
                        border-radius: 8px;
                        font-weight: bold;
                        text-align: left;
                        font-size: 13px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 15px 20px;
                        background-color: transparent;
                        color: white;
                        border-radius: 8px;
                        text-align: left;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #3a3a3a;
                    }
                """)

    def _handle_logout(self):
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def add_page(self, page: QWidget):
        self.stacked_widget.addWidget(page)

    def show_page(self, index: int):
        if 0 <= index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)
            buttons = [self.dashboard_btn, self.violations_btn, self.violation_history_btn, self.payment_history_btn]
            if index < len(buttons):
                self._update_nav_buttons(buttons[index])