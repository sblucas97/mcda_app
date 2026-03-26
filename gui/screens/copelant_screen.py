from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui.widgets.method_header_bar import MethodHeaderBar
from gui.widgets.scrollable_content_area import ScrollableContentArea
from gui.widgets.named_list_section import NamedListSection
from gui.widgets.decision_matrix_section import DecisionMatrixSection
from gui.widgets.configure_decision_matrix_table import configure_decision_matrix_table
from gui.widgets.calculate_button import create_calculate_button


class CopelantScreen(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.alternatives = []
        self.criteria = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self._header = MethodHeaderBar()
        self._header.back_clicked.connect(self.back_clicked.emit)
        layout.addWidget(self._header)

        scroll = ScrollableContentArea()
        c = scroll.content_layout
        layout.addWidget(scroll)

        self._alt_section = NamedListSection(
            "Alternatives:", "Enter alternative name",
            "Add Alternative", "No alternatives added yet",
        )
        self._alt_section.input.returnPressed.connect(self._add_alternative)
        self._alt_section.add_button.clicked.connect(self._add_alternative)
        c.addWidget(self._alt_section)

        self._crit_section = NamedListSection(
            "Criteria:", "Enter criterion name",
            "Add Criterion", "No criteria added yet",
        )
        self._crit_section.input.returnPressed.connect(self._add_criterion)
        self._crit_section.add_button.clicked.connect(self._add_criterion)
        c.addWidget(self._crit_section)

        self._matrix = DecisionMatrixSection(min_height=100)
        c.addWidget(self._matrix)

        btn = create_calculate_button()
        btn.clicked.connect(self.calculate_results)
        c.addWidget(btn)

        self._results_panel = CopelantResultsPanel()
        c.addWidget(self._results_panel)

    def set_method(self, method_name: str) -> None:
        self._header.set_title(method_name)
        self._reset_data()

    def _add_alternative(self):
        name = self._alt_section.input.text().strip()
        if not name:
            return
        if name in self.alternatives:
            QMessageBox.warning(self, "Duplicate", "This alternative already exists!")
            return
        self.alternatives.append(name)
        self._alt_section.input.clear()
        self._refresh_lists()
        self._refresh_matrix()

    def _add_criterion(self):
        name = self._crit_section.input.text().strip()
        if not name:
            return
        if name in self.criteria:
            QMessageBox.warning(self, "Duplicate", "This criterion already exists!")
            return
        self.criteria.append(name)
        self._crit_section.input.clear()
        self._refresh_lists()
        self._refresh_matrix()

    def _reset_data(self):
        self.alternatives = []
        self.criteria = []
        self._alt_section.input.clear()
        self._crit_section.input.clear()
        self._results_panel.clear()
        self._refresh_lists()
        self._refresh_matrix()

    def _refresh_lists(self):
        self._alt_section.summary_label.setText(
            f"Alternatives: {', '.join(self.alternatives)}"
            if self.alternatives else "No alternatives added yet"
        )
        self._crit_section.summary_label.setText(
            f"Criteria: {', '.join(self.criteria)}"
            if self.criteria else "No criteria added yet"
        )

    def _refresh_matrix(self):
        configure_decision_matrix_table(
            self._matrix.table, self.alternatives, self.criteria, default_cell_text="0"
        )

    def calculate_results(self):
        if not self.alternatives or not self.criteria:
            QMessageBox.warning(self, "Incomplete Data",
                                "Please add at least one alternative and one criterion!")
            return

        try:
            alt_len = len(self.alternatives)
            crit_len = len(self.criteria)

            criteria_matrix_results = []
            for x in range(crit_len):
                crit_label = self.criteria[x]
                result_m = []
                for i in range(alt_len):
                    inner_matrix = []
                    for j in range(alt_len):
                        v = None
                        if i != j and j > i:
                            value_i_x = float(self._matrix.table.item(i, x).text())
                            value_j_x = float(self._matrix.table.item(j, x).text())
                            if value_i_x > value_j_x:
                                v = 1
                            elif value_i_x < value_j_x:
                                v = -1
                            else:
                                v = 0
                        inner_matrix.append(v)
                    result_m.append(inner_matrix)

                criteria_matrix_results.append({
                    "title": f"Criterion: {crit_label}",
                    "rows": self.alternatives,
                    "columns": self.alternatives,
                    "table": result_m,
                })

            decision_matrix_table = []
            for i in range(alt_len):
                inner_matrix = []
                for j in range(alt_len):
                    v = None
                    if i != j and j > i:
                        t = sum(criteria_matrix_results[x]["table"][i][j] for x in range(crit_len))
                        v = 1 if t > 0 else (-1 if t < 0 else 0)
                    inner_matrix.append(v)
                decision_matrix_table.append(inner_matrix)

            for i in range(alt_len):
                for j in range(alt_len):
                    if i > j and i != j:
                        decision_matrix_table[i][j] = decision_matrix_table[j][i] * -1

            decision_matrix = [{
                "title": "Decision Matrix",
                "rows": self.alternatives,
                "columns": self.alternatives,
                "table": decision_matrix_table,
            }]

            t_s = [
                sum(decision_matrix_table[i][j] for j in range(alt_len) if i != j)
                for i in range(alt_len)
            ]
            total_sum = [{
                "title": "Total Sum Matrix",
                "rows": self.alternatives,
                "columns": ["Sum"],
                "table": [t_s],
            }]

            indexed = list(enumerate(t_s))
            sorted_indexed = sorted(indexed, key=lambda x: x[1], reverse=True)
            r = [0] * alt_len
            for rank, (original_index, _) in enumerate(sorted_indexed):
                r[original_index] = rank + 1

            ranking = [{
                "title": "Final Result",
                "rows": self.alternatives,
                "columns": ["Ranking"],
                "table": [r],
            }]

            self._results_panel.clear()
            self._results_panel.populate(criteria_matrix_results)
            self._results_panel.populate(decision_matrix)
            self._results_panel.populate(total_sum)
            self._results_panel.populate(ranking)

        except (ValueError, AttributeError):
            QMessageBox.warning(self, "Invalid Input",
                                "Please enter valid numeric values in all cells!")

class CopelantResultsPanel(QWidget):
    """
    Renders a sequence of titled result matrices.
    Call .populate(matrices) with a list of matrix dicts, or .clear() to reset.

    Each matrix dict shape:
        {"title": str, "rows": list[str], "columns": list[str], "table": list[list]}
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widgets: list[QWidget] = []

    def populate(self, matrices: list[dict]) -> None:
        for m in matrices:
            self._add(MatrixResultTable(
                title=m["title"],
                table=m["table"],
                rows=m["rows"],
                columns=m["columns"],
            ))

    def clear(self) -> None:
        for w in self._widgets:
            w.setParent(None)
            w.deleteLater()
        self._widgets.clear()

    def _add(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)
        self._widgets.append(widget)

class MatrixResultTable(QWidget):
    """
    A titled, fixed-size, read-only table for displaying a 2D result matrix.

    Usage:
        widget = MatrixResultTable(
            title="Criterion: Cost",
            table=[[1, None, -1], ...],
            rows=["A", "B", "C"],
            columns=["A", "B", "C"],
        )
    """

    _CELL_SIZE = 60

    def __init__(
        self,
        title: str,
        table: list[list],
        rows: list[str],
        columns: list[str],
        parent=None,
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addSpacing(10)
        layout.addWidget(self._build_title(title))
        layout.addLayout(self._build_centered_table(table, rows, columns))
        layout.addSpacing(20)

    def _build_title(self, text: str) -> QLabel:
        label = QLabel(text)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _build_centered_table(
        self,
        table: list[list],
        rows: list[str],
        columns: list[str],
    ) -> QHBoxLayout:
        row_layout = QHBoxLayout()
        row_layout.addStretch()
        row_layout.addWidget(self._build_table(table, rows, columns))
        row_layout.addStretch()
        return row_layout

    def _build_table(
        self,
        table: list[list],
        rows: list[str],
        columns: list[str],
    ) -> QTableWidget:
        num_rows = len(table)
        num_cols = len(table[0]) if table else 0
        cs = self._CELL_SIZE

        t = QTableWidget(num_rows, num_cols)
        t.setHorizontalHeaderLabels(rows)
        t.setVerticalHeaderLabels(columns)

        for i in range(num_cols):
            t.setColumnWidth(i, cs)
        for i in range(num_rows):
            t.setRowHeight(i, cs)

        for i in range(num_rows):
            for j in range(num_cols):
                value = table[i][j]
                item = QTableWidgetItem("-" if value is None else str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                t.setItem(i, j, item)

        table_width = t.verticalHeader().width() + (cs * num_cols) + 2
        table_height = t.horizontalHeader().height() + (cs * num_rows) + 2
        t.setFixedSize(table_width, table_height)
        t.setMaximumWidth(table_width)

        return t