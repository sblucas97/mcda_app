"""Reusable UI building blocks for MCDA method screens."""

from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt

def configure_decision_matrix_table(
    table: QTableWidget,
    alternatives: list,
    criteria: list,
    *,
    default_cell_text: str = "0",
) -> None:
    """Resize headers and fill numeric default cells; clears when inputs are empty."""
    table.clear()
    if not alternatives or not criteria:
        table.setRowCount(0)
        table.setColumnCount(0)
        return

    table.setRowCount(len(alternatives))
    table.setColumnCount(len(criteria))
    table.setHorizontalHeaderLabels(criteria)
    table.setVerticalHeaderLabels(alternatives)

    for i in range(len(alternatives)):
        for j in range(len(criteria)):
            item = QTableWidgetItem(default_cell_text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, j, item)

    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
