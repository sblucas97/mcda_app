from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class MenuScreen(QWidget):
    method_selected = pyqtSignal(str)
    condorcet_selected = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("MCDA Decision Tool")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Select a decision-making method")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Method buttons container
        methods_frame = QFrame()
        methods_frame.setMaximumWidth(400)
        methods_layout = QVBoxLayout(methods_frame)
        
        # Borda Method button
        borda_button = QPushButton("Borda Method")
        borda_button.setMinimumHeight(60)
        borda_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        borda_button.clicked.connect(lambda: self.select_method("Borda Method"))

        #Condorcet Method button
        condorcet_method_button = QPushButton("Condorcet Method")
        condorcet_method_button.setMinimumHeight(60)
        condorcet_method_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        condorcet_method_button.clicked.connect(self.select_condorcet_method)

        methods_layout.addWidget(borda_button)
        methods_layout.addWidget(condorcet_method_button)
        
        # Add more method buttons here in the future
        # Example:
        # ahp_button = QPushButton("Analytic Hierarchy Process (AHP)")
        # methods_layout.addWidget(ahp_button)
        
        layout.addWidget(methods_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def select_condorcet_method(self):
        self.condorcet_selected.emit()
    
    def select_method(self, method_name):
        self.method_selected.emit(method_name)