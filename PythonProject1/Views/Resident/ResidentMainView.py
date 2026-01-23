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

        # User info (SAFE)
        first = self.user_data.get("RFirstName", "")
        last = self.user_data.get("RLastName", "")
        rid = self.user_data.get("ResidentID", "N/A")

        logo = ResourceHelper.load_pixmap("RoadEyeLogo.png", 60, 60)

        header = StyledWidgets.create_sidebar_header(
            logo, "RoadEye", f"{first} {last}".strip(), f"ID: {rid}"
        )
        layout.addWidget(header)

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(10, 20, 10, 10)

        self.dashboard_btn = StyledWidgets.create_nav_button("Dashboard", True)
        self.violations_btn = StyledWidgets.create_nav_button("My Violations")
        self.payment_history_btn = StyledWidgets.create_nav_button("Payment History")

        self.dashboard_btn.clicked.connect(lambda: self._on_nav_clicked(0, self.dashboard_btn))
        self.violations_btn.clicked.connect(lambda: self._on_nav_clicked(1, self.violations_btn))
        self.payment_history_btn.clicked.connect(lambda: self._on_nav_clicked(2, self.payment_history_btn))

        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.violations_btn)
        nav_layout.addWidget(self.payment_history_btn)
        nav_layout.addStretch()

        layout.addWidget(nav_container, 1)

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
        buttons = [self.dashboard_btn, self.violations_btn, self.payment_history_btn]

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
            self._update_nav_buttons(
                [self.dashboard_btn, self.violations_btn, self.payment_history_btn][index]
            )
