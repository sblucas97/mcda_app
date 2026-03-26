from PyQt6.QtWidgets import (
    QLabel,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from gui.widgets.styles import (
    STYLE_SECTION_LABEL_MATRIX,
)

class DecisionMatrixSection(QWidget):
    """Bold section label and decision matrix table."""

    def __init__(
        self,
        title: str = "Decision Matrix:",
        min_height: int = 200,
        parent=None,
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        matrix_label = QLabel(title)
        matrix_label.setStyleSheet(STYLE_SECTION_LABEL_MATRIX)
        layout.addWidget(matrix_label)

        self.table = QTableWidget()
        self.table.setMinimumHeight(min_height)
        layout.addWidget(self.table)
