from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from gui.menu_screen import MenuScreen
from gui.borda_screen import BordaScreen
from gui.condorcet_screen import CondorcetScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCDA Decision Tool")
        self.setGeometry(100, 100, 900, 700)
        
        # Create stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create screens
        self.menu_screen = MenuScreen()
        self.borda_screen = BordaScreen()
        self.condorcet_screen = CondorcetScreen()

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.borda_screen)
        self.stacked_widget.addWidget(self.condorcet_screen)
        
        # Connect signals
        self.menu_screen.method_selected.connect(self.show_borda_screen)
        self.menu_screen.condorcet_selected.connect(self.show_condorcet_screen)
        self.condorcet_screen.back_clicked.connect(self.show_menu_screen)
        self.borda_screen.back_clicked.connect(self.show_menu_screen)
        
        # Start with menu screen
        self.show_menu_screen()
    
    def show_menu_screen(self):
        self.stacked_widget.setCurrentWidget(self.menu_screen)
    
    def show_condorcet_screen(self):
        self.stacked_widget.setCurrentWidget(self.condorcet_screen)
        
    def show_borda_screen(self, method_name):
        self.borda_screen.set_method(method_name)
        self.stacked_widget.setCurrentWidget(self.borda_screen)