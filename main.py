import sys
from PyQt6.QtWidgets import QApplication 
from views.main_window import MainWindow
from controllers.lexico_controller import LexicoController

def main():
    app = QApplication(sys.argv)
    
    with open("assets/style.qss", "r") as f:
        app.setStyleSheet(f.read())
        
    window = MainWindow()
    controller = LexicoController(window)
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == '__main__':
    main()
