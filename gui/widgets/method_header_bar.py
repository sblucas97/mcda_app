from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from gui.widgets.styles import (
    STYLE_BACK_BUTTON
)

class MethodHeaderBar(QWidget):
    """Back button, centered title, and balanced spacing for method screens."""

    back_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self._back_button = QPushButton("← Back")
        self._back_button.setMaximumWidth(100)
        self._back_button.setStyleSheet(STYLE_BACK_BUTTON)
        self._back_button.clicked.connect(self.back_clicked.emit)
        layout.addWidget(self._back_button)

        self.title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label, 1)

        layout.addSpacing(100)

    def set_title(self, text: str) -> None:
        self.title_label.setText(text)