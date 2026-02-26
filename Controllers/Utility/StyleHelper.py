from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
class StyleHelper:
    """Helper class for consistent styling across admin pages"""

    @staticmethod
    def style_search_input(widget):
        """Style search input"""
        widget.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
            }
        """)

    @staticmethod
    def style_action_button(widget, color):
        """Style action button"""
        widget.setStyleSheet(f"""
            QPushButton {{
                padding: 12px 25px;
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """)

    @staticmethod
    def style_table(table):
        """Style table widget"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: #363636;
                border: none;
                border-radius: 8px;
                color: #ffffff;
                gridline-color: #4a4a4a;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #4a4a4a;
            }
            QTableWidget::item:selected {
                background-color: #e8bb41;
                color: #1e1e1e;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #e8bb41;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11pt;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #5a5a5a;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #e8bb41;
            }
        """)

        header = table.horizontalHeader()
        for i in range(table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(50)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)