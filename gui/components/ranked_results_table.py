from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from gui.widgets.styles import STYLE_RESULT_SECTION_LABEL


class RankedResultsTable(QWidget):
    """
    Displays a ranked results table given a dict of
    {alt_name: {"sum": float, "ranking": int}}.
    Fully self-contained — just call .populate(alternatives, ranking).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Result sum:")
        label.setStyleSheet(STYLE_RESULT_SECTION_LABEL)
        layout.addWidget(label)

        self._table = QTableWidget()
        self._table.setMinimumHeight(300)
        layout.addWidget(self._table)

    def populate(self, alternatives: list[str], ranking: dict) -> None:
        self._table.clear()
        self._table.setRowCount(len(alternatives))
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(["Sum", "Ranking"])
        self._table.setVerticalHeaderLabels(alternatives)

        for row, alt in enumerate(alternatives):
            for col, key in enumerate(("sum", "ranking")):
                item = QTableWidgetItem(str(ranking[alt][key]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self._table.setItem(row, col, item)