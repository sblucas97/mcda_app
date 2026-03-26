from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
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


class BordaScreen(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.method_name = ""
        self.alternatives = []
        self.criteria = []
        self._alt_empty_text = "No alternatives added yet"
        self._crit_empty_text = "No criteria added yet"
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.header = MethodHeaderBar()
        self.header.back_clicked.connect(self.back_clicked.emit)
        main_layout.addWidget(self.header)

        scroll = ScrollableContentArea()
        content_layout = scroll.content_layout
        main_layout.addWidget(scroll)

        self.alt_section = NamedListSection(
            "Alternatives:",
            "Enter alternative name",
            "Add Alternative",
            self._alt_empty_text,
        )
        self.alt_section.input.returnPressed.connect(self.add_alternative)
        self.alt_section.add_button.clicked.connect(self.add_alternative)
        content_layout.addWidget(self.alt_section)

        self.crit_section = NamedListSection(
            "Criteria:",
            "Enter criterion name",
            "Add Criterion",
            self._crit_empty_text,
        )
        self.crit_section.input.returnPressed.connect(self.add_criterion)
        self.crit_section.add_button.clicked.connect(self.add_criterion)
        content_layout.addWidget(self.crit_section)

        self.matrix_section = DecisionMatrixSection(min_height=300)
        content_layout.addWidget(self.matrix_section)

        matrix_sum_table_label = QLabel("Result sum:")
        matrix_sum_table_label.setStyleSheet(STYLE_RESULT_SECTION_LABEL)
        content_layout.addWidget(matrix_sum_table_label)

        self.matrix_sum_table = QTableWidget()
        self.matrix_sum_table.setMinimumHeight(300)
        self.matrix_sum_table.setRowCount(0)
        self.matrix_sum_table.setColumnCount(0)
        content_layout.addWidget(self.matrix_sum_table)

        calculate_button = create_calculate_button()
        calculate_button.clicked.connect(self.calculate_results)
        content_layout.addWidget(calculate_button)

        self.setLayout(main_layout)

    def set_method(self, method_name):
        self.method_name = method_name
        self.header.set_title(method_name)
        self.reset_data()

    def reset_data(self):
        self.alternatives = []
        self.criteria = []
        self.alt_section.input.clear()
        self.crit_section.input.clear()
        self.update_lists()
        self.update_matrix()

    def _add_unique_named_item(self, name: str, items: list[str], *, kind: str) -> bool:
        name = name.strip()
        if not name:
            return False
        if name in items:
            QMessageBox.warning(self, "Duplicate", f"This {kind} already exists!")
            return False
        items.append(name)
        return True

    def _update_named_list_summary(self, section: NamedListSection, items: list[str], *, label: str, empty_text: str) -> None:
        section.summary_label.setText(f"{label}: {', '.join(items)}" if items else empty_text)

    def _read_matrix_float(self, row: int, col: int) -> float:
        item = self.matrix_section.table.item(row, col)
        if item is None:
            raise ValueError("Missing cell")
        return float(item.text())

    def add_alternative(self):
        name = self.alt_section.input.text()
        if self._add_unique_named_item(name, self.alternatives, kind="alternative"):
            self.alt_section.input.clear()
            self.update_lists()
            self.update_matrix()

    def add_criterion(self):
        name = self.crit_section.input.text()
        if self._add_unique_named_item(name, self.criteria, kind="criterion"):
            self.crit_section.input.clear()
            self.update_lists()
            self.update_matrix()

    def update_lists(self):
        self._update_named_list_summary(
            self.alt_section,
            self.alternatives,
            label="Alternatives",
            empty_text=self._alt_empty_text,
        )
        self._update_named_list_summary(
            self.crit_section,
            self.criteria,
            label="Criteria",
            empty_text=self._crit_empty_text,
        )

    def update_matrix(self):
        configure_decision_matrix_table(
            self.matrix_section.table,
            self.alternatives,
            self.criteria,
            default_cell_text="0.0",
        )

    def generate_matrix_sum_table(self, ranking):
        self.matrix_sum_table.clear()

        self.matrix_sum_table.setRowCount(len(self.alternatives))
        self.matrix_sum_table.setColumnCount(2)

        self.matrix_sum_table.setHorizontalHeaderLabels(["Sum", "Ranking"])
        self.matrix_sum_table.setVerticalHeaderLabels(self.alternatives)

        for row, alt in enumerate(self.alternatives):
            sum_item = QTableWidgetItem(str(ranking[alt]["sum"]))
            sum_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.matrix_sum_table.setItem(row, 0, sum_item)

            rank_item = QTableWidgetItem(str(ranking[alt]["ranking"]))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.matrix_sum_table.setItem(row, 1, rank_item)


    def calculate_results(self):
        if not self.alternatives or not self.criteria:
            QMessageBox.warning(self, "Incomplete Data",
                              "Please add at least one alternative and one criterion!")
            return

        try:
            sums = {
                alt: sum(self._read_matrix_float(i, j) for j in range(len(self.criteria)))
                for i, alt in enumerate(self.alternatives)
            }

            ranked = {
                alt: {"sum": total, "ranking": rank}
                for rank, (alt, total) in enumerate(
                    sorted(sums.items(), key=lambda kv: kv[1], reverse=True),
                    start=1,
                )
            }
            self.generate_matrix_sum_table(ranked)
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Invalid Input",
                              "Please enter valid numeric values in all cells!")
