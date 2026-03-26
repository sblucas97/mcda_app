from PyQt6.QtWidgets import (
    QPushButton
)

from gui.widgets.styles import (
    STYLE_CALCULATE_BUTTON
)

def create_calculate_button(text: str = "Calculate Results") -> QPushButton:
    btn = QPushButton(text)
    btn.setMinimumHeight(40)
    btn.setStyleSheet(STYLE_CALCULATE_BUTTON)
    return btn