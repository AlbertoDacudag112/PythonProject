"""
Views/Admin/AdminMainView.py
Main admin window with sidebar navigation (extracted from AdminWindow.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Controllers.Utility.ResourceHelper import ResourceHelper
from Views.Common.StyledWidgets import StyledWidgets


class AdminMainView(QMainWindow):
    """Main window for admin users - UI only"""

    # Signals
    logout_requested = pyqtSignal()
    page_changed = pyqtSignal(int)  # Page index

    def __init__(self, admin_data: dict):
        super().__init__()
        self.admin_data = admin_data
        self.setWindowTitle("RoadEye - Admin Dashboard")
        self.setMinimumSize(1400, 800)
        self.setStyleSheet("background-color: #1e1e1e;")

        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self._create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #2d2d2d;")
        main_layout.addWidget(self.stacked_widget, 1)

    def _create_sidebar(self):
        """Create navigation sidebar"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(280)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-right: 1px solid #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header section with larger logo
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
        app_name = QLabel("RoadEye Admin")
        app_name.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        app_name.setStyleSheet("color: #e8bb41;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(app_name)

        # Admin name
        admin_name = f"{self.admin_data.get('AFirstName', '')} {self.admin_data.get('ALastName', '')}"
        admin_name_label = QLabel(admin_name.strip())
        admin_name_label.setFont(QFont("Segoe UI", 12))
        admin_name_label.setStyleSheet("color: #ffffff;")
        admin_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(admin_name_label)

        # Role
        role_label = QLabel(f"Role: {self.admin_data.get('Role', 'Admin')}")
        role_label.setFont(QFont("Segoe UI", 10))
        role_label.setStyleSheet("color: #999999;")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(role_label)

        layout.addWidget(header_container)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #3a3a3a;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Navigation buttons (removed emojis)
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        # nav_layout.setContentsMargins(10, 20, 10, 10)
        # nav_layout.setSpacing(20)

        self.dashboard_btn = StyledWidgets.create_nav_button("Dashboard", True)
        self.violations_btn = StyledWidgets.create_nav_button("Violations", False)
        self.residents_btn = StyledWidgets.create_nav_button("Residents", False)
        self.vehicles_btn = StyledWidgets.create_nav_button("Vehicles", False)
        self.reports_btn = StyledWidgets.create_nav_button("Reports", False)



        self.dashboard_btn.clicked.connect(lambda: self._on_nav_clicked(0, self.dashboard_btn))
        self.violations_btn.clicked.connect(lambda: self._on_nav_clicked(1, self.violations_btn))
        self.residents_btn.clicked.connect(lambda: self._on_nav_clicked(2, self.residents_btn))
        self.vehicles_btn.clicked.connect(lambda: self._on_nav_clicked(3, self.vehicles_btn))
        self.reports_btn.clicked.connect(lambda: self._on_nav_clicked(4, self.reports_btn))

        # Button Design(Dont touch)


        btnD = """
            QPushButton {
                                padding: 15px 20px;
                                background-color: transparent;
                                color: #ffffff;
                                border: none;
                                border-radius: 8px;
                                text-align: left;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: #3a3a3a;
                            }
                        """
        btnDs = """
            QPushButton {
                        padding: 15px 20px;
                        background-color: #e8bb41;
                        color: #1e1e1e;
                        border: none;
                        border-radius: 8px;
                        text-align: left;
                        font-weight: bold;
                        font-size: 13px;
                    }
                        """

        self.dashboard_btn.setStyleSheet(btnDs)
        self.violations_btn.setStyleSheet(btnD)
        self.residents_btn.setStyleSheet(btnD)
        self.vehicles_btn.setStyleSheet(btnD)
        self.reports_btn.setStyleSheet(btnD)


        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.violations_btn)
        nav_layout.addWidget(self.residents_btn)
        nav_layout.addWidget(self.vehicles_btn)
        nav_layout.addWidget(self.reports_btn)
        nav_layout.addStretch()

        layout.addWidget(nav_container, 1)

        # Logout button
        logout_btn = StyledWidgets.create_logout_button()
        logout_btn.clicked.connect(self._handle_logout)
        layout.addWidget(logout_btn)

    def _on_nav_clicked(self, page_index: int, button: QPushButton):
        """Handle navigation button click"""
        self._update_nav_buttons(button)
        self.page_changed.emit(page_index)
        self.stacked_widget.setCurrentIndex(page_index)

    def _update_nav_buttons(self, active_btn: QPushButton):
        """Update navigation button styles"""
        buttons = [
            self.dashboard_btn,
            self.violations_btn,
            self.residents_btn,
            self.vehicles_btn,
            self.reports_btn
        ]

        for btn in buttons:
            if btn == active_btn:
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 15px 20px;
                        background-color: #e8bb41;
                        color: #1e1e1e;
                        border: none;
                        border-radius: 8px;
                        text-align: left;
                        font-weight: bold;
                        font-size: 13px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 15px 20px;
                        background-color: transparent;
                        color: #ffffff;
                        border: none;
                        border-radius: 8px;
                        text-align: left;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #3a3a3a;
                    }
                """)

    def _handle_logout(self):
        """Handle logout button click"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def add_page(self, page: QWidget):
        """Add a page to the stacked widget"""
        self.stacked_widget.addWidget(page)

    def show_page(self, index: int):
        """Show specific page"""
        self.stacked_widget.setCurrentIndex(index)
        # Update nav button highlighting
        buttons = [
            self.dashboard_btn,
            self.violations_btn,
            self.residents_btn,
            self.vehicles_btn,
            self.reports_btn
        ]
        if 0 <= index < len(buttons):
            self._update_nav_buttons(buttons[index])