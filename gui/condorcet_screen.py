from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class CondorcetScreen(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.method_name = ""
        self.alternatives = []
        self.criteria = []
        self.results = []
        self.result_widgets = []  # Track widgets to remove them later
        self.color_codes = [
            "#FF0000",  # Bright Red
            "#8A2BE2",  # Blue Violet
            "#FFD700",  # Gold (Yellowish)
            "#FF8C00",  # Dark Orange
            "#008000",  # Green
            "#4682B4",  # Steel Blue
            "#ADFF2F"   # Green Yellow
            "#8FBC8F",  # Dark Sea Green
            "#9370DB",  # Medium Purple
            "#762B2B",  # Bright Red
        ]
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header with back button and title
        header_layout = QHBoxLayout()

        back_button = QPushButton("← Back")
        back_button.setMaximumWidth(100)
        back_button.clicked.connect(self.back_clicked.emit)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        header_layout.addWidget(back_button)

        self.title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label, 1)

        header_layout.addSpacing(100)  # Balance the back button

        main_layout.addLayout(header_layout)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)

        # Alternatives input section
        alt_label = QLabel("Alternatives:")
        alt_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.content_layout.addWidget(alt_label)

        alt_input_layout = QHBoxLayout()
        self.alt_input = QLineEdit()
        self.alt_input.setPlaceholderText("Enter alternative name")
        self.alt_input.returnPressed.connect(self.add_alternative)
        alt_input_layout.addWidget(self.alt_input)

        add_alt_button = QPushButton("Add Alternative")
        add_alt_button.clicked.connect(self.add_alternative)
        add_alt_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        alt_input_layout.addWidget(add_alt_button)

        self.content_layout.addLayout(alt_input_layout)

        # Alternatives list
        self.alt_list_label = QLabel("No alternatives added yet")
        self.alt_list_label.setStyleSheet("color: #666; margin: 5px 0 15px 0;")
        self.content_layout.addWidget(self.alt_list_label)

        # Criteria input section
        crit_label = QLabel("Criteria:")
        crit_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.content_layout.addWidget(crit_label)

        crit_input_layout = QHBoxLayout()
        self.crit_input = QLineEdit()
        self.crit_input.setPlaceholderText("Enter criterion name")
        self.crit_input.returnPressed.connect(self.add_criterion)
        crit_input_layout.addWidget(self.crit_input)

        add_crit_button = QPushButton("Add Criterion")
        add_crit_button.clicked.connect(self.add_criterion)
        add_crit_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        crit_input_layout.addWidget(add_crit_button)

        self.content_layout.addLayout(crit_input_layout)

        # Criteria list
        self.crit_list_label = QLabel("No criteria added yet")
        self.crit_list_label.setStyleSheet("color: #666; margin: 5px 0 15px 0;")
        self.content_layout.addWidget(self.crit_list_label)

        # Decision matrix table
        matrix_label = QLabel("Decision Matrix:")
        matrix_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 20px;")
        self.content_layout.addWidget(matrix_label)

        self.matrix_table = QTableWidget()
        self.matrix_table.setMinimumHeight(100)
        self.content_layout.addWidget(self.matrix_table)

        # Calculate button
        calculate_button = QPushButton("Calculate Results")
        calculate_button.setMinimumHeight(40)
        calculate_button.clicked.connect(self.calculate_results)  # Fixed: removed ()
        calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.content_layout.addWidget(calculate_button)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def clear_result_widgets(self):
        """Remove all previously drawn result widgets"""
        for widget in self.result_widgets:
            widget.setParent(None)
            widget.deleteLater()
        self.result_widgets.clear()

    def draw_results_tables(self):
        # Clear previous results
        self.clear_result_widgets()
        if len(self.results) == 0:
            return

        # Add header label
        matrix_sum_table_label = QLabel("Pairwise Comparison Results:")
        matrix_sum_table_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 20px;")
        self.content_layout.addWidget(matrix_sum_table_label)
        self.result_widgets.append(matrix_sum_table_label)

        ranking = {}
        for alt_name in self.alternatives:
            ranking[alt_name] = 0

        alternatives_n_colors = {}
        for i in range(len(self.alternatives)):
            alternatives_n_colors[self.alternatives[i]] = self.color_codes[i]

        # Draw each result
        for r in self.results:
            alt_1 = r['alt_1']
            alt_2 = r['alt_2']
            matrix_data = r['matrix']

            row_count_grid_content = len(matrix_data)
            col_count_grid_content = len(matrix_data[0]) if row_count_grid_content > 0 else 0

            comparison_grid_container = QWidget()
            comparison_grid_layout = QGridLayout(comparison_grid_container)
            comparison_grid_layout.setSpacing(2)

            header_label = QLabel(f"Detailed Matrix: {alt_1} X {alt_2}")
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_label.setStyleSheet(
                "border: 1px solid #cccccc; "
                "padding: 5px; "
                "font-weight: bold;"
            )
            comparison_grid_layout.addWidget(header_label, 0, 0, 1, col_count_grid_content)

            for i in range(row_count_grid_content):
                for j in range(col_count_grid_content):
                    cell_data = matrix_data[i][j]
                    value = cell_data['v']
                    display_text = f"{value}"
                    cell_label = QLabel(display_text)
                    cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell_label_template = (
                        "border: 1px solid #cccccc; "
                        "background-color: {alt_color}; "
                        "padding: 5px; "
                    )
                    final_cell_label_template = cell_label_template.format(alt_color=alternatives_n_colors[cell_data['alt']])
                    cell_label.setStyleSheet(final_cell_label_template)
                    comparison_grid_layout.addWidget(cell_label, i+1, j)

            self.content_layout.addWidget(comparison_grid_container)
            self.result_widgets.append(comparison_grid_container)

            footer_container = QWidget()
            footer_layout = QGridLayout(footer_container)
            footer_layout.setSpacing(2)

            summary_title = QLabel("Summary")
            summary_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            summary_title.setStyleSheet(
                "border: 1px solid #cccccc; "
                "padding: 5px; "
                "font-weight: bold;"
            )
            footer_layout.addWidget(summary_title, 0, 0, 1, 2)  # Row 0, col 0, span 1 row and 2 cols

            sum_alt_1 = sum(matrix_data[i][j]['v'] for i in range(row_count_grid_content)
                            for j in range(col_count_grid_content)
                            if matrix_data[i][j]['alt'] == alt_1)
            sum_alt_2 = sum(matrix_data[i][j]['v'] for i in range(row_count_grid_content)
                            for j in range(col_count_grid_content)
                            if matrix_data[i][j]['alt'] == alt_2)

            # Row 1: Alternative 1 name and sum
            alt1_name_label = QLabel(alt_1)
            alt1_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            atl1_label_template = (
                "border: 1px solid #cccccc; "
                "background-color: {alt_color}; "
                "padding: 5px; "
            )
            final_atl1_label_template = atl1_label_template.format(alt_color=alternatives_n_colors[alt_1])
            alt1_name_label.setStyleSheet(final_atl1_label_template)
            footer_layout.addWidget(alt1_name_label, 1, 0)

            alt1_sum_label = QLabel(str(sum_alt_1))
            alt1_sum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            alt1_sum_label.setStyleSheet(
                "border: 1px solid #cccccc; "
                "padding: 5px; "
            )
            footer_layout.addWidget(alt1_sum_label, 1, 1)

            # Row 2: Alternative 2 name and sum
            alt2_name_label = QLabel(alt_2)
            alt2_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            atl2_label_template = (
                "border: 1px solid #cccccc; "
                "background-color: {alt_color}; "
                "padding: 5px; "
            )
            final_atl2_label_template = atl2_label_template.format(alt_color=alternatives_n_colors[alt_2])
            alt2_name_label.setStyleSheet(final_atl2_label_template)
            footer_layout.addWidget(alt2_name_label, 2, 0)

            alt2_sum_label = QLabel(str(sum_alt_2))
            alt2_sum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            alt2_sum_label.setStyleSheet(
                "border: 1px solid #cccccc; "
                "padding: 5px; "
            )
            footer_layout.addWidget(alt2_sum_label, 2, 1)

            # Summary result cell
            summary_result_content = ""
            if sum_alt_1 > sum_alt_2:
                ranking[alt_1] += 1
                summary_result_content = f"Result: {alt_1} > {alt_2}"
            else:
                ranking[alt_2] += 1
                summary_result_content = f"Result: {alt_2} > {alt_1}"

            summary_result_label= QLabel(summary_result_content)
            summary_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            summary_result_label.setStyleSheet(
                "border: 1px solid #cccccc; "
                "padding: 5px; "
                "font-weight: bold;"
            )
            footer_layout.addWidget(summary_result_label, 3, 0, 1, 2)

            self.content_layout.addWidget(footer_container)
            self.result_widgets.append(footer_container)

        final_result_container = QWidget()
        final_result_layout = QGridLayout(final_result_container)
        final_result_label = f"Result: {max(ranking, key=ranking.get)}"
        final_result_title = QLabel(final_result_label)
        final_result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        final_result_title.setStyleSheet(
            "border: 2px solid #cccccc; "
            "padding: 20px; "
            "font-weight: bold;"
        )
        final_result_layout.addWidget(final_result_title, 0, 0, 1, 2)
        self.content_layout.addWidget(final_result_container)
        self.result_widgets.append(final_result_container)


    def set_method(self, method_name):
        self.method_name = method_name
        self.title_label.setText(method_name)
        self.reset_data()

    def reset_data(self):
        self.alternatives = []
        self.criteria = []
        self.results = []
        self.alt_input.clear()
        self.crit_input.clear()
        self.clear_result_widgets()
        self.update_lists()
        self.update_matrix()

    def add_alternative(self):
        name = self.alt_input.text().strip()
        if name and name not in self.alternatives:
            self.alternatives.append(name)
            self.alt_input.clear()
            self.update_lists()
            self.update_matrix()
        elif name in self.alternatives:
            QMessageBox.warning(self, "Duplicate", "This alternative already exists!")

    def add_criterion(self):
        name = self.crit_input.text().strip()
        if name and name not in self.criteria:
            self.criteria.append(name)
            self.crit_input.clear()
            self.update_lists()
            self.update_matrix()
        elif name in self.criteria:
            QMessageBox.warning(self, "Duplicate", "This criterion already exists!")

    def update_lists(self):
        if self.alternatives:
            self.alt_list_label.setText("Alternatives: " + ", ".join(self.alternatives))
        else:
            self.alt_list_label.setText("No alternatives added yet")

        if self.criteria:
            self.crit_list_label.setText("Criteria: " + ", ".join(self.criteria))
        else:
            self.crit_list_label.setText("No criteria added yet")

    def update_matrix(self):
        self.matrix_table.clear()

        if not self.alternatives or not self.criteria:
            self.matrix_table.setRowCount(0)
            self.matrix_table.setColumnCount(0)
            return

        self.matrix_table.setRowCount(len(self.alternatives))
        self.matrix_table.setColumnCount(len(self.criteria))

        self.matrix_table.setHorizontalHeaderLabels(self.criteria)
        self.matrix_table.setVerticalHeaderLabels(self.alternatives)

        # Fill with default values or existing values
        for i in range(len(self.alternatives)):
            for j in range(len(self.criteria)):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.matrix_table.setItem(i, j, item)

        # Adjust column widths
        header = self.matrix_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def calculate_pair_and_pair(self, x, y):
        alt_1 = self.alternatives[x]
        alt_2 = self.alternatives[y]

        # Fetch row x values
        row_x_values = []
        for col in range(self.matrix_table.columnCount()):
            item = self.matrix_table.item(x, col)
            if item and item.text():
                try:
                    row_x_values.append(int(item.text()))
                except ValueError:
                    row_x_values.append(0)
            else:
                row_x_values.append(0)

        # Fetch row y values
        row_y_values = []
        for col in range(self.matrix_table.columnCount()):
            item = self.matrix_table.item(y, col)
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
            results = []
            n = len(self.alternatives)
            for x in range(0, n-1):
                for y in range(x+1, n):
                    r = self.calculate_pair_and_pair(x, y)
                    results.append(r)

            self.results = results
            self.draw_results_tables()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                              "Please enter valid numeric values in all cells!")
