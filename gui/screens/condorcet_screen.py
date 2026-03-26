from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

from gui.widgets.decision_matrix_section import DecisionMatrixSection
from gui.widgets.configure_decision_matrix_table import configure_decision_matrix_table
from gui.widgets.calculate_button import create_calculate_button
from gui.widgets.method_header_bar import MethodHeaderBar
from gui.widgets.scrollable_content_area import ScrollableContentArea
from gui.widgets.named_list_section import NamedListSection
from gui.widgets.styles import STYLE_RESULT_SECTION_LABEL


class CondorcetScreen(QWidget):
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

        self._results_panel = CondorcetResultsPanel()
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

    def calculate_pair_and_pair(self, x, y):
        alt_1 = self.alternatives[x]
        alt_2 = self.alternatives[y]

        row_x_values = []
        for col in range(self._matrix.table.columnCount()):
            item = self._matrix.table.item(x, col)
            if item and item.text():
                try:
                    row_x_values.append(int(item.text()))
                except ValueError:
                    row_x_values.append(0)
            else:
                row_x_values.append(0)

        row_y_values = []
        for col in range(self._matrix.table.columnCount()):
            item = self._matrix.table.item(y, col)
            if item and item.text():
                try:
                    row_y_values.append(int(item.text()))
                except ValueError:
                    row_y_values.append(0)
            else:
                row_y_values.append(0)

        result_matrix = []
        for i in row_x_values:
            intermediary_matrix = []
            for j in row_y_values:
                if i > j:
                    intermediary_matrix.append({"v": i, "alt": alt_1})
                else:
                    intermediary_matrix.append({"v": j, "alt": alt_2})
            result_matrix.append(intermediary_matrix)

        return {"alt_1": alt_1, "alt_2": alt_2, "matrix": result_matrix}

    def calculate_results(self):
        if not self.alternatives or not self.criteria:
            QMessageBox.warning(self, "Incomplete Data",
                                "Please add at least one alternative and one criterion!")
            return
        try:
            n = len(self.alternatives)
            results = [
                self.calculate_pair_and_pair(x, y)
                for x in range(n - 1)
                for y in range(x + 1, n)
            ]
            self._results_panel.populate(results, self.alternatives)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "Please enter valid numeric values in all cells!")

class CondorcetResultsPanel(QWidget):
    """
    Renders all pairwise comparison cards and a final winner banner.
    Call .populate(results, alternatives, color_map) to render.
    Call .clear() to reset between calculations.
    """

    _DEFAULT_COLORS = [
        "#FF0000", "#8A2BE2", "#FFD700", "#FF8C00", "#008000",
        "#4682B4", "#ADFF2F", "#8FBC8F", "#9370DB", "#762B2B",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._cards: list[QWidget] = []

    def populate(
        self,
        results: list[dict],
        alternatives: list[str],
        color_map: dict[str, str] | None = None,
    ) -> None:
        self.clear()
        if not results:
            return

        if color_map is None:
            color_map = {
                alt: self._DEFAULT_COLORS[i % len(self._DEFAULT_COLORS)]
                for i, alt in enumerate(alternatives)
            }

        header = QLabel("Pairwise Comparison Results:")
        header.setStyleSheet(STYLE_RESULT_SECTION_LABEL)
        self._add(header)

        ranking = {alt: 0 for alt in alternatives}

        for r in results:
            card = PairwiseComparisonCard(
                r["alt_1"], r["alt_2"], r["matrix"], color_map
            )
            ranking[card.winner] += 1
            self._add(card)

        self._add(self._build_winner_banner(ranking))

    def clear(self) -> None:
        for widget in self._cards:
            widget.setParent(None)
            widget.deleteLater()
        self._cards.clear()

    def _add(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)
        self._cards.append(widget)

    @staticmethod
    def _build_winner_banner(ranking: dict[str, int]) -> QWidget:
        winner = max(ranking, key=ranking.get)

        container = QWidget()
        grid = QGridLayout(container)

        label = QLabel(f"Result: {winner}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "border: 2px solid #cccccc; padding: 20px; font-weight: bold;"
        )
        grid.addWidget(label, 0, 0, 1, 2)
        return container

class PairwiseComparisonCard(QWidget):
    """
    Displays the detailed comparison matrix and summary for one alt_1 vs alt_2 pair.
    Returns the winner via .winner property after construction.
    """

    def __init__(
        self,
        alt_1: str,
        alt_2: str,
        matrix_data: list[list[dict]],
        color_map: dict[str, str],
        parent=None,
    ):
        super().__init__(parent)
        self._alt_1 = alt_1
        self._alt_2 = alt_2
        self._winner: str = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        layout.addWidget(self._build_matrix_grid(matrix_data, color_map))
        layout.addWidget(self._build_summary_footer(matrix_data, color_map))

    @property
    def winner(self) -> str:
        return self._winner

    def _build_matrix_grid(
        self, matrix_data: list[list[dict]], color_map: dict[str, str]
    ) -> QWidget:
        rows = len(matrix_data)
        cols = len(matrix_data[0]) if rows > 0 else 0

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(2)

        header = self._make_label(
            f"Detailed Matrix: {self._alt_1} X {self._alt_2}",
            bold=True,
        )
        grid.addWidget(header, 0, 0, 1, cols)

        for i in range(rows):
            for j in range(cols):
                cell = matrix_data[i][j]
                label = self._make_label(
                    str(cell["v"]),
                    bg_color=color_map[cell["alt"]],
                )
                grid.addWidget(label, i + 1, j)

        return container

    def _build_summary_footer(
        self, matrix_data: list[list[dict]], color_map: dict[str, str]
    ) -> QWidget:
        rows = len(matrix_data)
        cols = len(matrix_data[0]) if rows > 0 else 0

        sum_1 = sum(
            matrix_data[i][j]["v"]
            for i in range(rows)
            for j in range(cols)
            if matrix_data[i][j]["alt"] == self._alt_1
        )
        sum_2 = sum(
            matrix_data[i][j]["v"]
            for i in range(rows)
            for j in range(cols)
            if matrix_data[i][j]["alt"] == self._alt_2
        )

        self._winner = self._alt_1 if sum_1 > sum_2 else self._alt_2
        loser = self._alt_2 if self._winner == self._alt_1 else self._alt_1
        result_text = f"Result: {self._winner} > {loser}"

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(2)

        grid.addWidget(self._make_label("Summary", bold=True), 0, 0, 1, 2)
        grid.addWidget(self._make_label(self._alt_1, bg_color=color_map[self._alt_1]), 1, 0)
        grid.addWidget(self._make_label(str(sum_1)), 1, 1)
        grid.addWidget(self._make_label(self._alt_2, bg_color=color_map[self._alt_2]), 2, 0)
        grid.addWidget(self._make_label(str(sum_2)), 2, 1)
        grid.addWidget(self._make_label(result_text, bold=True), 3, 0, 1, 2)

        return container

    @staticmethod
    def _make_label(text: str, *, bold: bool = False, bg_color: str = "") -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        style = "border: 1px solid #cccccc; padding: 5px;"
        if bold:
            style += " font-weight: bold;"
        if bg_color:
            style += f" background-color: {bg_color};"

        label.setStyleSheet(style)
        return label