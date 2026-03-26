from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.styles import (
    STYLE_EMPTY_LIST_HINT,
    STYLE_PRIMARY_ACTION_BUTTON,
    STYLE_SECTION_LABEL,
)


class NamedListSection(QWidget):
    """
    Section title, line edit + primary add button, and summary line
    (e.g. alternatives or criteria lists).
    """

    def __init__(
        self,
        section_title: str,
        placeholder: str,
        add_button_text: str,
        empty_summary_text: str,
        parent=None,
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        section_label = QLabel(section_title)
        section_label.setStyleSheet(STYLE_SECTION_LABEL)
        layout.addWidget(section_label)

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        row.addWidget(self.input)

        self.add_button = QPushButton(add_button_text)
        self.add_button.setStyleSheet(STYLE_PRIMARY_ACTION_BUTTON)
        row.addWidget(self.add_button)
        layout.addLayout(row)

        self.summary_label = QLabel(empty_summary_text)
        self.summary_label.setStyleSheet(STYLE_EMPTY_LIST_HINT)
        layout.addWidget(self.summary_label)