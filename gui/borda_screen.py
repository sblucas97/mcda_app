from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class BordaScreen(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.method_name = ""
        self.alternatives = []
        self.criteria = []
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
        content_layout = QVBoxLayout(content_widget)

        # Alternatives input section
        alt_label = QLabel("Alternatives:")
        alt_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        content_layout.addWidget(alt_label)

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

        content_layout.addLayout(alt_input_layout)

        # Alternatives list
        self.alt_list_label = QLabel("No alternatives added yet")
        self.alt_list_label.setStyleSheet("color: #666; margin: 5px 0 15px 0;")
        content_layout.addWidget(self.alt_list_label)

        # Criteria input section
        crit_label = QLabel("Criteria:")
        crit_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        content_layout.addWidget(crit_label)

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

        content_layout.addLayout(crit_input_layout)

        # Criteria list
        self.crit_list_label = QLabel("No criteria added yet")
        self.crit_list_label.setStyleSheet("color: #666; margin: 5px 0 15px 0;")
        content_layout.addWidget(self.crit_list_label)

        # Decision matrix table
        matrix_label = QLabel("Decision Matrix:")
        matrix_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 20px;")
        content_layout.addWidget(matrix_label)

        self.matrix_table = QTableWidget()
        self.matrix_table.setMinimumHeight(300)
        content_layout.addWidget(self.matrix_table)

        #Result sum table
        matrix_sum_table_label = QLabel("Result sum:")
        matrix_sum_table_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 20px;")
        content_layout.addWidget(matrix_sum_table_label)

        self.matrix_sum_table = QTableWidget()
        self.matrix_sum_table.setMinimumHeight(300)
        self.matrix_sum_table.setRowCount(0)
        self.matrix_sum_table.setColumnCount(0)
        content_layout.addWidget(self.matrix_sum_table)


        # Calculate button
        calculate_button = QPushButton("Calculate Results")
        calculate_button.setMinimumHeight(40)
        calculate_button.clicked.connect(self.calculate_results)
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
        content_layout.addWidget(calculate_button)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def set_method(self, method_name):
        self.method_name = method_name
        self.title_label.setText(method_name)
        self.reset_data()

    def reset_data(self):
        self.alternatives = []
        self.criteria = []
        self.alt_input.clear()
        self.crit_input.clear()
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
                item = QTableWidgetItem("0.0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.matrix_table.setItem(i, j, item)

        # Adjust column widths
        header = self.matrix_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def generate_matrix_sum_table(self, ranking):
        self.matrix_sum_table.clear()

        self.matrix_sum_table.setRowCount(len(self.alternatives))
        self.matrix_sum_table.setColumnCount(2)

        self.matrix_sum_table.setHorizontalHeaderLabels(['Sum', 'Ranking'])
        self.matrix_sum_table.setVerticalHeaderLabels(self.alternatives)

        ## Fill
        for i, alt in enumerate(self.alternatives):
            for j in range(2):
                v = ''
                if j == 0:
                    v = str(ranking[alt]['sum'])
                else:
                    v = str(ranking[alt]['ranking'])

                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.matrix_sum_table.setItem(i, j, item)


    def calculate_results(self):
        if not self.alternatives or not self.criteria:
            QMessageBox.warning(self, "Incomplete Data",
                              "Please add at least one alternative and one criterion!")
            return

        # Collect matrix values
        try:
            sum_result = {}
            for i, alt in enumerate(self.alternatives):
                total = 0
                for j in range(len(self.criteria)):
                    item = self.matrix_table.item(i, j)
                    value = float(item.text())
                    total += value
                sum_result[alt] = total

             # Sort the items by value (descending order)
            sorted_items = sorted(sum_result.items(), key=lambda x: x[1], reverse=True)

            # Create result dict with ranking
            ranked = {}
            for rank, (key, value) in enumerate(sorted_items, start=1):
                ranked[key] = {"sum": value, "ranking": rank}

            self.generate_matrix_sum_table(ranked)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                              "Please enter valid numeric values in all cells!")
