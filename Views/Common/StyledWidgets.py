"""
Views/Common/StyledWidgets.py
Factory class for creating consistently styled widgets
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class StyledWidgets:
    """Factory class for creating consistently styled widgets"""

    @staticmethod
    def create_nav_button(text: str, active: bool = False) -> QPushButton:
        """Create a navigation button for sidebar"""
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setCheckable(True)
        btn.setChecked(active)
        return btn

    @staticmethod
    def create_sidebar_header(logo_pixmap, title: str, user_name: str, user_info: str) -> QFrame:
        """Create sidebar header with logo and user info"""
        header = QFrame()
        header.setStyleSheet("background-color: #2d2d2d; padding: 20px;")

        layout = QVBoxLayout(header)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo_label = QLabel()
        if logo_pixmap and not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🚗")
            logo_label.setFont(QFont("Segoe UI", 30))
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
        """Create logout button"""
        btn = QPushButton("🚪 Logout")
        btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
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

    @staticmethod
    def create_search_input(placeholder: str = "Search...") -> QLineEdit:
        """Create a styled search input field"""
        search_input = QLineEdit()
        search_input.setPlaceholderText(placeholder)
        search_input.setFont(QFont("Segoe UI", 11))
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px 10px 40px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
            }
        """)
        return search_input

    @staticmethod
    def create_filter_combo(items: list) -> QComboBox:
        """Create a styled filter combo box"""
        combo = QComboBox()
        combo.addItems(items)
        combo.setFont(QFont("Segoe UI", 11))
        combo.setStyleSheet("""
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
        return combo

    @staticmethod
    def create_action_button(text: str, icon: str = "", primary: bool = True) -> QPushButton:
        """Create an action button (primary or secondary)"""
        btn = QPushButton(f"{icon} {text}" if icon else text)
        btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        if primary:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #e8bb41;
                    color: #1e1e1e;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #f0c855;
                }
                QPushButton:pressed {
                    background-color: #d4a838;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #5a5a5a;
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #6a6a6a;
                }
                QPushButton:pressed {
                    background-color: #4a4a4a;
                }
            """)
        return btn

    @staticmethod
    def create_table_widget() -> QTableWidget:
        """Create a styled table widget"""
        table = QTableWidget()
        table.setFont(QFont("Segoe UI", 10))
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                gridline-color: #3a3a3a;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #e8bb41;
                color: #1e1e1e;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #5a5a5a;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6a6a6a;
            }
        """)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        return table

    @staticmethod
    def create_stat_card(title: str, value: str, icon: str = "") -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # Icon (if provided)
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI", 24))
            icon_label.setStyleSheet("color: #e8bb41;")
            layout.addWidget(icon_label)

        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(value_label)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: #999999;")
        layout.addWidget(title_label)

        return card

    @staticmethod
    def create_section_header(text: str) -> QLabel:
        """Create a section header label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        label.setStyleSheet("color: #ffffff; padding: 10px 0;")
        return label

    @staticmethod
    def create_label(text: str, bold: bool = False) -> QLabel:
        """Create a styled label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold if bold else QFont.Weight.Normal))
        label.setStyleSheet("color: #ffffff;")
        return label

    @staticmethod
    def create_form_input(placeholder: str = "") -> QLineEdit:
        """Create a styled form input field"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFont(QFont("Segoe UI", 11))
        input_field.setStyleSheet("""
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
        return input_field

    @staticmethod
    def create_date_edit() -> QDateEdit:
        """Create a styled date edit widget"""
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setFont(QFont("Segoe UI", 11))
        date_edit.setStyleSheet("""
            QDateEdit {
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QDateEdit:focus {
                border: 2px solid #e8bb41;
            }
            QDateEdit::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        return date_edit

    @staticmethod
    def style_table(table: QTableWidget):
        """Apply styling to a table widget"""
        table.setFont(QFont("Segoe UI", 10))
        table.setStyleSheet("""
                QTableWidget {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    gridline-color: #3a3a3a;
                    border: none;
                }
                QTableWidget::item {
                    padding: 10px;
                }
                QTableWidget::item:selected {
                    background-color: #e8bb41;
                    color: #1e1e1e;
                }
                QHeaderView::section {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 12px;
                    border: none;
                    font-weight: bold;
                }
                QScrollBar:vertical {
                    background-color: #2d2d2d;
                    width: 12px;
                }
                QScrollBar::handle:vertical {
                    background-color: #5a5a5a;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #6a6a6a;
                }
            """)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)