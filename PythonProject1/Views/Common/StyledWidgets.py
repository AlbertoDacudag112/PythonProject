from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class StyledWidgets:
    """Factory class for creating consistently styled widgets"""

    @staticmethod
    def create_nav_button(text: str, active: bool = False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI Emoji", 11))
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setCheckable(True)
        btn.setChecked(active)
        return btn

    @staticmethod
    def create_sidebar_header(logo_pixmap, title: str, user_name: str, user_info: str) -> QFrame:
        header = QFrame()
        header.setStyleSheet("background-color: #2d2d2d; padding: 20px;")

        layout = QVBoxLayout(header)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo_label = QLabel()
        if logo_pixmap:
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🚗")
            logo_label.setFont(QFont("Segoe UI Emoji", 30))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #e8bb41;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name_label = QLabel(user_name)
        name_label.setFont(QFont("Segoe UI", 12))
        name_label.setStyleSheet("color: #ffffff;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_label = QLabel(user_info)
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setStyleSheet("color: #999999;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addSpacing(8)
        layout.addWidget(name_label)
        layout.addWidget(info_label)

        return header

    @staticmethod
    def create_logout_button() -> QPushButton:
        btn = QPushButton("🚪 Logout")
        btn.setFont(QFont("Segoe UI Emoji", 11, QFont.Weight.Bold))
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                background-color: #d32f2f;
                color: white;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #f44336;
            }
        """)
        return btn
